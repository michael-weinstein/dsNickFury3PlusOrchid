#!/usr/bin/env python3

global pythonInterpreterAbsolutePath
pythonInterpreterAbsolutePath = "/u/local/apps/python/3.4.3/bin/python3 "

class CheckArgs():  #class that checks arguments and ultimately returns a validated set of arguments to the main program
    
    def __init__(self):
        import argparse
        import os
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--altStartRange", help = "Percent of protein to exclude for an alternative start site", default = 25, type = int)
        parser.add_argument("-p", "--cutPoint", help = "The point where the system cuts, relative to the end of the PAM", default = -6, type = int)
        parser.add_argument("-d", "--cutPadding", help = "Number of bases on either side of the cut that need to be in a coding region.", default = 6, type = int)
        parser.add_argument("-s", "--geneSymbol", help = "Enter a gene symbol to analyze")
        parser.add_argument("-g", "--ensg", help = "Enter an ensembl gene ID to analyze")
        parser.add_argument("-m", "--mock", help = "Run a mock submission without sending to queue or writing files.", action = 'store_true')
        rawArgs = parser.parse_args()
        altStartRange = rawArgs.altStartRange
        if altStartRange > 100 or altStartRange < 0:
            raise RuntimeError("Alternative start check range must be between 0 and 100 percent of the protein.")
        self.altStartRange = rawArgs.altStartRange
        self.cutPoint = rawArgs.cutPoint
        self.cutPadding = rawArgs.cutPadding
        if rawArgs.ensg and rawArgs.geneSymbol:
            raise RuntimeError("Either a gene symbol or an ensembl gene ID must be passed.")
        elif not rawArgs.ensg and not rawArgs.geneSymbol:
            raise RuntimeError("You must pass either a gene symbol or an ensembl ID.  Nothing to analyze here.")
        elif rawArgs.ensg:
            ensg = rawArgs.ensg
            ensg = ensg.upper()
            if not ensg.startswith("ENSG") and len(ensg) == 15:
                raise RuntimeError("Malformed ensembl gene ID passed: %s" %(ensg))
            ensgNumber = ensg.replace("ENSG","")
            if not len(ensgNumber) == 11:
                raise RuntimeError("Malformed ensembl gene ID passed: %s" %(ensg))
            try:
                int(ensgNumber)
            except ValueError:
                raise RuntimeError("Malformed ensembl gene ID passed: %s" %(ensg))
            self.ensg = ensg
        elif rawArgs.geneSymbol:
            self.geneSymbol = rawArgs.geneSymbol.upper()
            self.ensg = False
        self.mock = rawArgs.mock
        #self.sequence = self.getSequence()


class SequenceWindow(object):
    
    def __init__(self, sequence, windowSize):
        if len(sequence) < windowSize:
            raise RuntimeError("Error: Window size cannot be longer than the submitted sequence.")
        self.sequence = sequence
        self.windowStart = 0
        self.windowSize = windowSize
        self.windowEnd = windowSize
        self.windowSeq = self.getSequence()
        
    def __eq__(self, other):
        if self.getSequence():
            return self.getSequence.upper() == other.upper()
        else:
            return False
    
    def getSequence(self):
        try:
            return self.sequence[self.windowStart : self.windowEnd]
        except IndexError:
            return ""
    
    def advance(self, length = 1):
        self.windowStart += length
        self.windowEnd += length
        self.windowSeq = self.getSequence()
        return self.windowSeq
        
    def jumpCodon(self):
        self.advance(self.windowSize)
        

class TranscriptAnalysis(object):
    
    def __init__(self, enst):
        self.windowSize = 3
        self.enst = enst
        self.exons, self.introns = self.getExonsAndIntrons()
        self.chromosome, self.startPosition, self.strand = self.getStartAndStrand()
        if self.strand == "+":
            self.exonIntervals = self.senseExonIntervals()
        if self.strand == "-":
            self.exonIntervals = self.antisenseExonIntervals()
        self.proteinLength = self.getProteinLength()
        if self.proteinLength:
            self.startExon, self.startExonBase = self.findStartSite()
            self.lastAltStartExon, self.lastAltStartExonBase = self.checkAltStartSites()
            self.stopExon, self.stopPosition = self.findStopSite()
            self.maskedSequence = self.sequenceForAnalysis()
        
    def getExonsAndIntrons(self):
        import urllib.request
        urlStart  = "http://rest.ensembl.org/sequence/id/"
        urlEnd = "?content-type=text/plain;mask_feature=1"
        fullUrl = urlStart + self.enst + urlEnd
        ensembl = urllib.request.urlopen(fullUrl)
        rawSeq = ensembl.read().decode('utf-8')
        rawSeq = self.reviseSoftMaskForTranslationStart(rawSeq)
        exons, introns = self.splitExonsAndIntrons(rawSeq)
        #print(rawSeq)
        #print(exons)
        return (exons, introns)
    
    def reviseSoftMaskForTranslationStart(self, sequence):
        translationStart = translationStartDict[self.enst]
        beforeStart = sequence[:translationStart].lower()
        afterStart = sequence[translationStart:]
        return beforeStart + afterStart
        
    def splitExonsAndIntrons(self, rawSeq):
        firstLetter = True
        exonList = []
        intronList = []
        exonBufferString = ""
        intronBufferString = ""
        for letter in rawSeq:
            if firstLetter:  #This will catch the first letter and ensure that we are starting on an exon (this should be the case).  This will report back if we are not.
                if not letter.isupper:
                    self.startsOnExon = False
                    firstLetter = False
                else:
                    self.startsOnExon = True
                    firstLetter = False
            if letter.isupper():  #iterate over the whole sequence, purging the "buffer" to the appropriate array whenever we hit a letter of the opposite kind
                exonBufferString += letter
                if intronBufferString:
                    intronList.append(intronBufferString)
                    intronBufferString = ""
            elif letter.islower:
                intronBufferString += letter
                if exonBufferString:
                    exonList.append(exonBufferString)
                    exonBufferString = ""
        if exonBufferString:  #this will flush any remaining exon (which will usually be there) to the collection
            exonList.append(exonBufferString)
        if intronBufferString: #this will flush any remaining intron sequence.  There should only be one or the other, and it should be exon, I believe.
            intronList.append(intronBufferString)
        return (exonList, intronList)
    
    def getStartAndStrand(self):
        import urllib.request
        import json
        urlStart  = "http://rest.ensembl.org/map/cdna/"
        urlEnd = "/1..1?content-type=application/json"
        fullUrl = urlStart + self.enst + urlEnd
        try:
            ensembl = urllib.request.urlopen(fullUrl)
            failure = False
        except urllib.error.HTTPError as errorMessage:
            failure = str(errorMessage)
        if failure:
            raise RuntimeError("Position request from Ensembl returned '" + failure + "'\nFull URL for debug: " + fullUrl)
        intervalData = json.loads(ensembl.read().decode('utf-8'))['mappings'][0]  #there should only be a single item at each level here, this will strip them off
        chromosome = intervalData["seq_region_name"]
        startPosition = int(intervalData["start"]) #This should come in as an int anyway, but just to be sure...
        strand = intervalData["strand"]
        if strand == -1:  #This comes in as an int value
            strand = "-"
        else:
            strand = "+"
        return (chromosome, startPosition, strand)

    def senseExonIntervals(self):
        exonIntervalList = []
        currentIntron = 0
        currentPosition = self.startPosition  #This should be the first base of the first exon of a gene in the sense orientation
        if not self.startsOnExon:  #I don't expect this should ever happen.  I have also encountered bigger surprises before
            currentPosition += len(self.introns[0])
            currentIntron += 1
        for currentExon in range(0,len(self.exons)):  #I am guessing they will need these values to be inclusive ranges.  This will not be valid BED format.
            exonStart = currentPosition
            exonEnd = currentPosition + len(self.exons[currentExon]) - 1  #the minus 1 is to make the end inclusive.  Removing the minus 1 would turn this into BED standard numbers
            currentPosition = exonEnd + 1  #we only need the plus 1 if we are not doing BED standard
            exonIntervalList.append((exonStart, exonEnd))
            if not currentExon == len(self.exons) - 1:
                currentPosition += len(self.introns[currentIntron])
                currentIntron += 1
        return exonIntervalList
    
    def antisenseExonIntervals(self):
        exonIntervalList = []
        currentIntron = 0
        currentPosition = self.startPosition
        if not self.startsOnExon:
            currentPosition -= len(self.introns[0])
            currentIntron += 1
        for currentExon in range(0,len(self.exons)):
            exonEnd = currentPosition  #this will need to be + 1 if we are doing BED standard
            exonStart = currentPosition - len(self.exons[currentExon]) + 1  #This will not change regardless of format
            currentPosition = exonStart - 1  #This will also not change, regardless of format.  It should point to the first letter (the ending, with regard to sense strand) of the intron
            exonIntervalList.append((exonStart, exonEnd))
            if not currentExon == len(self.exons) - 1:
                currentPosition -= len(self.introns[currentIntron])
                currentIntron += 1
        return exonIntervalList
    
    def getProteinLength(self):
        self.mRNAseq = ""
        startCodons = ["ATG"]
        stopCodons = ["TAA", "TAG", "TGA"]
        for exon in self.exons:
            self.mRNAseq += exon
        window = SequenceWindow(self.mRNAseq, 3)
        while window.windowSeq and window.windowSeq not in startCodons:
            window.advance()
        if not window.windowSeq in startCodons:  #because we ran off the end of the sequence and returned an empty string
            return False
        self.codingSequence = ""
        while window.windowSeq and not window.windowSeq in stopCodons:
            self.codingSequence += window.windowSeq
            window.jumpCodon()
        if not window.windowSeq in stopCodons:
            return False
        return len(self.codingSequence)/3
        
    def findStartSite(self):
        startExon = -1
        startPosition = False
        startCodons = ["ATG"]
        startFound = False
        for currentExon in range(0,len(self.exons)):
            testSeq = self.exons[currentExon]
            if not currentExon == len(self.exons) - 1:
                testSeq += self.exons[currentExon + 1][0:self.windowSize -1] #adding on the first two bases from the next exon to detect a start formed by a junction.  These are usually pretty rare.
            window = SequenceWindow(testSeq, self.windowSize)
            position = 0
            while window.windowSeq and not window.windowSeq in startCodons:
                window.advance()
                position += 1
            if not window.windowSeq:  #we didn't find a start codon in this exon
                continue
            startExon = currentExon
            startPosition = position
            startFound = True
            break
        if startFound:
            return (startExon, startPosition)
        else:
            raise RuntimeError("Error: Unable to identify start codon, this should not happen, as we already found it.")
        
    def findStopSite(self):
        stopExon = False
        stopPosition = False
        stopCodons = ["TAA", "TAG", "TGA"]
        stopFound = False
        #codonsToTest = self.proteinLength * (args.altStartRange / 100)
        #codonsTested = 0
        for currentExon in range(self.startExon, len(self.exons)):
            #if codonsTested >= codonsToTest:
                #break
            if currentExon == self.startExon:
                testSeq = self.exons[currentExon][self.startExonBase + self.windowSize:]
                position = self.startExonBase + self.windowSize
                phase = len(testSeq) % self.windowSize
                #print("\t".join([str(currentExon + 1), str(len(testSeq)), str(phase), testSeq]))
            else:
                testSeq = self.exons[currentExon][(self.windowSize - phase) % self.windowSize:]
                position = 0
                #previousPhase = phase
                #phase = (len(testSeq) + previousPhase) % 3
                phase = len(testSeq) % self.windowSize
                #print("\t".join([str(currentExon + 1), str(len(testSeq)), str(phase)]))
            if not currentExon == len(self.exons) - 1:
                testSeq += self.exons[currentExon + 1][0:self.windowSize -1]
            if testSeq:
                if len(testSeq) < self.windowSize:
                    continue
                window = SequenceWindow(testSeq, self.windowSize)
            else:
                continue
            while window.windowSeq:
                if window.windowSeq in stopCodons:
                    return(currentExon, position)
                else:
                    window.jumpCodon()
                    position += self.windowSize
        print("Warning, unable to find stop codon.")
        return (False, False)
    
    def checkAltStartSites(self):
        lastAltStartExon = -1
        lastAltStartExonBase = False
        startCodons = ["ATG"]
        codonsToTest = self.proteinLength * (args.altStartRange / 100)
        codonsTested = 0
        for currentExon in range(self.startExon, len(self.exons)):
            if codonsTested >= codonsToTest:
                break
            if currentExon == self.startExon:
                testSeq = self.exons[currentExon][self.startExonBase + self.windowSize:]
                position = self.startExonBase + self.windowSize
                phase = len(testSeq) % self.windowSize
                #print("\t".join([str(currentExon + 1), str(len(testSeq)), str(phase), testSeq]))
            else:
                testSeq = self.exons[currentExon][(self.windowSize - phase) % self.windowSize:]
                position = 0
                #previousPhase = phase
                #phase = (len(testSeq) + previousPhase) % 3
                phase = len(testSeq) % self.windowSize  #we can skip all the fancy stuff above because it is accounted for when we take in a shorter testSeq
                #print("\t".join([str(currentExon + 1), str(len(testSeq)), str(phase)]))

            if not currentExon == len(self.exons) - 1:
                testSeq += self.exons[currentExon + 1][0:self.windowSize -1]
            if testSeq:
                if len(testSeq) < self.windowSize:
                    continue
                window = SequenceWindow(testSeq, self.windowSize)
            else:
                continue
            while window.windowSeq:
                if window.windowSeq in startCodons:
                    lastAltStartExon = currentExon
                    lastAltStartExonBase = position
                    window.jumpCodon()
                    position += self.windowSize
                    codonsTested += 1
                    if codonsTested >= codonsToTest:
                        break
                else:
                    window.jumpCodon()
                    position += self.windowSize
                    codonsTested += 1
                    if codonsTested >= codonsToTest:
                        break
        return (lastAltStartExon, lastAltStartExonBase)
    
    def sequenceForAnalysis(self):
        self.maskedSeqAltStart = False
        exons = self.exons#.copy()  #making local versions to alter
        introns = self.introns#.copy()
        for i in range(0,self.startExon):
            exons[i] = exons[i].lower()
        if self.stopExon != len(exons) - 1:
            for i in range(self.stopExon + 1, len(exons)):
                self.exons[i] = self.exons[i].lower()
        exonHolder = exons[self.startExon][:self.startExonBase].lower()
        exonHolder += exons[self.startExon][self.startExonBase:]
        exons[self.startExon] = exonHolder
        exonHolder = exons[self.stopExon][:self.stopPosition]
        exonHolder += exons[self.stopExon][self.stopPosition:].lower()
        exons[self.stopExon] = exonHolder
        maskedSequence = ""
        if self.lastAltStartExon != -1:
            for i in range(0,self.lastAltStartExon):
                maskedSequence += exons[i] + introns[i]
            self.maskedSeqAltStart = len(maskedSequence) + self.lastAltStartExonBase
            for i in range(self.lastAltStartExon, self.stopExon):
                maskedSequence += exons[i] + introns[i]
        else:
            for i in range(0, self.stopExon):
                maskedSequence += exons[i] + introns[i]
        self.maskedSeqLastCodon = len(maskedSequence)
        maskedSequence += self.exons[self.stopExon]
        return maskedSequence
            
            
            
                
    def __str__(self):
        output = ""
        output += "Start Coordinates: " + self.chromosome + ":" + str(self.startPosition) + "\n"
        output += "Strand: " + self.strand + "\n"
        output += "mRNA SEQUENCE:\n"
        currentIntron = 0
        if not self.startsOnExon:
            output += "Intron: " + str(len(self.introns[0])) + "\n"
            currentIntron += 1
        for currentExon in range(0,len(self.exons)):
            output += self.exons[currentExon] + "\n"
            if not currentExon == len(self.exons) - 1:
                output += "Intron: " + str(len(self.introns[currentIntron])) + "\n"
                currentIntron += 1
        output += "\nCODING INTERVALS (INCLUSIVE ON BOTH SIDES)\n"
        output += "\t".join(["Exon","Start","End","Length"]) + "\n"
        for currentExon in range(0,len(self.exonIntervals)):
            exonInterval = self.exonIntervals[currentExon]
            if self.strand == "+":
                output += "\t".join([str(currentExon + 1), str(exonInterval[0]), str(exonInterval[1]), str(exonInterval[1]- exonInterval[0])])  #not ending these lines because I may need to mark a start codon
            else:
                output += "\t".join([str(currentExon + 1), str(exonInterval[1]), str(exonInterval[0]), str(exonInterval[1]- exonInterval[0])])
            if currentExon == self.startExon:
                output += "\tStart codon at position " + str(self.startExonBase + 1) + ". Protein length: " + str(self.proteinLength) + ". "
            if currentExon == self.lastAltStartExon:
                output += "\tAlt Start codon at position " + str(self.lastAltStartExonBase + 1) + ". "
            if currentExon == self.stopExon:
                output += "\tStop codon at position " + str(self.stopPosition + 1) + ". "
            output += "\n"
        if self.startExon == -1:
            output += "Warning: Unable to find start codon in mRNA sequence"
        return output

class TargetFinder(object):  #This object is analogous to a FASTA indexer, except designed to deal with smaller sequences and can be extended to collect larger windows for analysis in azimuth
    
    def __init__(self, transcriptData, guideLength, pam):
        import degenerateBaseHandle
        self.target = transcriptData.maskedSequence
        self.maskedSeqAltStart = transcriptData.maskedSeqAltStart
        self.maskedSeqLastCodon = transcriptData.maskedSeqLastCodon
        self.targetGroup = transcriptData.enst
        self.pam = pam.upper()
        self.guideLength = guideLength
        self.longSeq = False
        self.lastGroup = 0
        self.done = False
        self.cutWindow = guideLength + len(pam) #subtract out the underscore
        self.start = 0  #start is inclusive
        self.end = self.cutWindow
        #if args.preferredPAM:
        #    self.pam = args.preferredPAM  #If the user specified an optimal PAM sequence, we will use that instead.  It will still probably be degenerate, but a bit more restricted.
        self.pamList = degenerateBaseHandle.NondegenerateBases(self.pam).permutations()
        self.pamLength = len(self.pam)
        self.matches = []  #initialize an empty list to hold our match sites (which will be TargetSite class instances)
        self.done = False
        self.position = 0
        self.cutPoint = args.cutPoint
        self.cutPadding = args.cutPadding
        self.matches = self.findMatches()
        
    def findMatches(self):  #main running function for this object, actually runs the search, gets azimuth scores if needed, and returns the list of matches
        import degenerateBaseHandle
        while not self.done:
            windowSeq = self.target[self.start:self.end]
            revComp = str(degenerateBaseHandle.ReverseComplement(windowSeq))
            if windowSeq[-self.pamLength:].upper() in self.pamList:
                try:
                    baseAfterCut = self.end + self.cutPoint
                    cutSeq = self.target[baseAfterCut - self.cutPadding : baseAfterCut + self.cutPadding]
                except IndexError:
                    cutSeq = False
                if cutSeq and cutSeq.isupper():
                    guide = windowSeq[:-self.pamLength]
                    pam = windowSeq[-self.pamLength:]
                    longSeq = self.getLongSeq(guide, pam,'+')  #tries to get an extended sequence for azimuth analysis
                    if longSeq:  #leaving out any site we can't get an azimuth extension for, as it would have to be uncomfortably close to the edge of the predicted transcript
                        self.matches.append(TargetSite(guide + "_" + pam, longSeq, self.end < self.maskedSeqAltStart, self.end > self.maskedSeqLastCodon, self.targetGroup))
            if revComp[-self.pamLength:].upper() in self.pamList:
                try:
                    baseAfterCut = self.start - self.cutPoint
                    cutSeq = self.target[baseAfterCut - self.cutPadding : baseAfterCut + self.cutPadding]
                except IndexError:
                    cutSeq = False
                if cutSeq and cutSeq.isupper():
                    guide = revComp[:-self.pamLength]
                    pam = revComp[-self.pamLength:]
                    longSeq = self.getLongSeq(guide, pam,'-')
                    if longSeq:
                        self.matches.append(TargetSite(guide + "_" + pam, longSeq, self.start < self.maskedSeqAltStart, self.start > self.maskedSeqLastCodon, self.targetGroup))
            self.advance()
        # if not args.skipAzimuth:
        #     self.useAzimuth = True
        # else:
        #     self.useAzimuth = False
        # if self.useAzimuth:
        #     self.azimuthAPIkey = self.getAzimuthAPIkey()
        #     if self.azimuthAPIkey:
        #         self.assignAzimuthScores()
        return self.matches
    
    def advance(self):  #moves the window ahead one character, then checks to see if it has reached the end
        self.start += 1
        self.end += 1
        self.position += 1
        self.done = self.end > len(self.target)

    def getLongSeq(self, guide, pam, strand):  #this method gets an extended sequence for azimuth or other analysis if possible
        import degenerateBaseHandle
        pamExtensionLength = 3
        guideExtensionLength = 24 - self.guideLength
        try:  #we need a try/except block for this because it is possible that the extended sequence will run us off the end of the sequence
            if strand == '+':
                pamEnd = self.end + pamExtensionLength
                guideStart = self.start - guideExtensionLength
                if pamEnd > len(self.target) or guideStart < 0:
                    return False
                pamExtension = self.target[self.end : pamEnd]
                guideExtension = self.target[self.start - guideExtensionLength : self.start]
            if strand == '-':
                pamStart = self.start - pamExtensionLength
                guideEnd = self.end + guideExtensionLength
                if pamStart < 0 or guideEnd > len(self.target):
                    return False
                pamExtension = self.target[self.start - pamExtensionLength : self.start]
                guideExtension = self.target[self.end : self.end + guideExtensionLength]
                pamExtension = str(degenerateBaseHandle.ReverseComplement(pamExtension))
                guideExtension = str(degenerateBaseHandle.ReverseComplement(guideExtension))
        except IndexError:  #If we get something near the end of the given sequence where we try to read off the end, we just return False for this value.  Later, this will tell us not try submitting it for analysis.
            return False
        if not len(pam) == 3:  #if we have to force the pam, we will warn the user
            if not self.forceAzimuthPam:
                print("WARNING: Attempting to force conformity of PAM site to the Azimuth model.  Predictions based on forced projections may not be as accurate.")
            self.forceAzimuthPam = True
            pam = pam[:2]
        extendedSeq = guideExtension + guide + pam + pamExtension
        # if not len(guide) == 20 and not args.noForcedBases:
        #     extendedSeq = list(extendedSeq)  #making it a list so that I can change individual characters by their index
        #     if not extendedSeq[4] == guide[0] and not args.noForced1:
        #         extendedSeq[4] = guide[0]
        #         if not self.forceGuide1:
        #             print("Forcing guide base 1 into position 1 for azimuth analysis.  Predictions based on forced projections may not be as accurate.")
        #             self.forceGuide1 = True
        #     if not extendedSeq[6] == guide[2] and not args.noForced3:
        #         extendedSeq[6] = guide[2]
        #         if not self.forceGuide3:
        #             print("Forcing guide base 3 into position 3 for azimuth analysis.  Predictions based on forced projections may not be as accurate.")
        #             self.forceGuide3 = True
        #     extendedSeq = str(extendedSeq)  #return the value back to a string for later submission
        return extendedSeq
    
class TargetSite(object):
    
    def __init__(self, sequence, azimuthSeq, beforeAltStart, lastExon, targetGroup):
        self.sequence = sequence
        self.azimuthSeq = azimuthSeq
        self.beforeAltStart = beforeAltStart
        self.lastExon = lastExon
        self.targetGroup = targetGroup
    
    def __str__(self):
        outputList = [self.sequence, self.azimuthSeq, self.beforeAltStart, self.lastExon, self.targetGroup]
        outputList = [str(item) for item in outputList]        
        return "\t".join(outputList)

class JobList(object):
    
    def __init__(self, targets, jobName, azureAccount, tableName):
        import re
        self.targets = targets
        self.azureAccount = azureAccount
        self.tableName = tableName
        self.jobName = re.sub('\W', "_", jobName)
        self.createJobBashLines()
        
    def createJobBashLines(self):
        import re
        self.bashLines = []
        # lastTargetGroup = ""
        # targetGroupMember = 0
        for i in range(0, len(self.targets)):
        #     flags = " "
        #     if self.targets[i][1]:
        #         flags += "--beforeAltStart "
        #     if self.targets[i][2]:
        #         flags += "--lastExon"
        #     if self.targets[i].targetGroup != lastTargetGroup:
        #         targetGroupMember = 0
        #     lastTargetGroup = self.targets[i].targetGroup
            azureTableInfo = [self.azureAccount, self.tableName, self.jobName, str(self.targets[i][0])]
        #    targetGroupMember += 1
            azureTableInfo = [re.sub('\W',"_",item) for item in azureTableInfo]  #make sure no weird characters like commas and dashes make it in here
            azureTableString = ",".join(azureTableInfo)
            bashLine = pythonInterpreterAbsolutePath + "dsNickFury3.2.py -m search -g hg38 -s " + self.targets[i][0].upper() + " -p NGG --azimuthSequence " + self.targets[i][1] + " --endClip 3 --azureTableOut " + azureTableString # + flags
            self.bashLines.append(bashLine)
        for line in self.bashLines:
            print(line)
    
    def createJobDirectory(self, mock):
        import os
        self.directoryName = "." + self.jobName
        if not mock:
            try:
                os.mkdir(self.directoryName)
            except:
                raise RuntimeError("Unable to create temporary directory " + self.directoryName)
            self.schedulerOutputDir = self.directoryName + os.sep + "schedulerOutput"
            try:
                os.mkdir(self.schedulerOutputDir)
            except:
                raise RuntimeError("Unable to create scheduler output directory " + self.schedulerOutputDir)

    def writeJobPickle(self, mock, jobsPerNode):
        import os
        import pickle
        jobList = [[]]
        jobsInLine = 0
        currentLine = 0
        jobList[currentLine].append("Zeroth job place holder")
        jobList.append([])
        currentLine = 1
        for job in self.bashLines:
            if jobsInLine == jobsPerNode:
                jobList.append([])
                currentLine += 1
                jobsInLine = 0
            jobList[currentLine].append(job)
            jobsInLine += 1
        self.lastJobIndex = len(jobList) - 1
        if not mock:
            file = open(self.directoryName + os.sep + "jobs.pkl", 'wb')
            pickle.dump(jobList, file)
            file.close()
        
    def submitJobs(self, jobsPerNode = 100, mock = False):
        import os
        import time
        self.createJobDirectory(mock)
        self.writeJobPickle(mock, jobsPerNode)
        arrayRunnerFileName = self.jobName + ".arrayRunner.sh"
        if not mock:
            file = open(arrayRunnerFileName, 'w')
            file.write(pythonInterpreterAbsolutePath + "searchWrapper.py -d " + self.directoryName)
            file.close()
        jobRange = " 1-" + str(self.lastJobIndex) + " "
        #stdOutDir = "/u/project/mweinste/mweinste/dsNickFury3/schedulerOutput "
        stdOutDir = "/dev/null "
        #stdErrOut = stdOutDir
        stdErrOut = os.getcwd() + os.sep + self.directoryName +  "/schedulerOutput/ "
        command = "qsub -cwd -V -N " + self.jobName + " -l h_data=8G,time=23:59:00 -M mweinstein@mednet.ucla.edu -m a -e " + stdErrOut + "-o " + stdOutDir + "-t " + jobRange + arrayRunnerFileName
        #command = "qsub -cwd -V -N " + self.jobName + " -l h_data=2G,time=23:59:00 -M mweinste@ucla.edu -m a -e " + os.getcwd() + os.sep + self.directoryName +  "/schedulerOutput/ -o " + os.getcwd() + os.sep + self.directoryName + "/schedulerOutput/ " + "-t " + jobRange + arrayRunnerFileName
        #command = "qsub -cwd -V -N " + self.jobName + " -l h_data=2G,time=23:59:00 -e " + os.getcwd() + os.sep + self.directoryName +  "/schedulerOutput/ -o " + os.getcwd() + os.sep + self.directoryName + "/schedulerOutput/ " + "-t " + jobRange + arrayRunnerFileName
        if not mock:
            success = False
            failed = 0
            while not success and failed <= 20:
                print ("Submitting: " + command)
                result = os.system(command)
                success = result == 0
                if not success:
                    time.sleep(30)
                failed += 1
        else:
            print("MOCK SUBMIT: " + command)
            for line in self.bashLines:
                print(line)
                
def getUniqueTargets(targetList, targetIndex):
    targetHash = {}
    repeatedTargets = set()
    for i in range(0, len(targetList)):
        if not targetList[i][targetIndex] in targetHash:
            targetHash[targetList[i][targetIndex]] = []
        else:
            repeatedTargets.add(targetList[i][targetIndex])
        targetHash[targetList[i][targetIndex]].append(i)
    deleteIndices = []
    for repeatedTarget in repeatedTargets:
        deleteIndices += targetHash[repeatedTarget][1:]
    deleteIndices.sort(reverse = True)
    for index in deleteIndices:
        del targetList[index]
    return targetList
    
class GeneTranscriptData(object):
    
    def __init__(self, transcriptData, ensg):
        self.transcriptData = transcriptData
        self.targetableTranscripts = []
        for transcript in list(self.transcriptData.keys()):
            if self.transcriptData[transcript]:
                self.targetableTranscripts.append(transcript)
        self.ensg = ensg
        
    def submitAzureTable(self, accountName, tableName):
        import json
        import time
        import sys
        if not args.mock:
            print("Connecting to Azure Tables...", end = "")
            import azure.storage.table
            try:
                tableAccountKeyFile = open('azureTable.apikey','r')
            except FileNotFoundError:
                raise RuntimeError("Unable to find the key to the azure table in azureTable.apikey (file was absent)")
            tableAccountkey = tableAccountKeyFile.read().strip()
            tableAccountKeyFile.close()
            tableHandle = False #initializing this so I can check it in the loop.  If the
            failures = 0
            while not tableHandle and failures <= 10:
                try:
                    if not tableHandle:
                        tableHandle = azure.storage.table.TableService(account_name=accountName, account_key=tableAccountkey)
                except Exception as e:  #catching all exceptions here and just retrying
                    print(e)
                    time.sleep(5)
                    failures += 1
            if not tableHandle:
                tableHandle = azure.storage.table.TableService(account_name=accountName, account_key=tableAccountkey)
            print("CONNECTED")
        submissionLists = {}
        maxListSize = 200
        print("Formatting data for Azure")
        for transcript in self.targetableTranscripts:
            submissionLists[transcript] = {0:{}}
            currentList = 0
            currentListSize = 0
            submissionLists[transcript][currentList] = {"PartitionKey":transcript, "RowKey":str(currentList)}
            for target in self.transcriptData[transcript]:
                if currentListSize == maxListSize:
                    currentList += 1
                    currentListSize = 0
                    submissionLists[transcript][currentList] = {"PartitionKey":transcript, "RowKey":str(currentList)}
                currentValuesHash = {"beforeAltStart":target[1],"lastExon":target[2]}
                currentValuesString = json.dumps(currentValuesHash)
                submissionLists[transcript][currentList][target[0]] = currentValuesString
                currentListSize += 1
        #print(submissionLists)
        print("Submitting gene info for %s" %(self.ensg))
        geneInfo = {"PartitionKey" : self.ensg,
                          "RowKey" : "info",
                          "gene" : self.ensg,
                          "transcripts" : json.dumps(self.targetableTranscripts)}
        if not args.mock:
            submitted = False
            failures = 0
            while not submitted and failures <= 10:
                try:
                    submitted = tableHandle.insert_entity(tableName, geneInfo)
                    #self.getBackDataFromAzureTable(tableHandle, tableName, transcriptInfo["PartitionKey"], transcriptInfo["RowKey"])
                except azure.common.AzureConflictHttpError:
                    print("Data already in Azure table.", file = sys.stderr)
                    submitted = True
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    failures += 1
                    continue
            if not submitted:
                submitted = tableHandle.insert_entity(tableName, geneInfo)
                #self.getBackDataFromAzureTable(tableHandle, tableName, transcriptInfo["PartitionKey"], transcriptInfo["RowKey"])
        else:
            print("Mock submission: " + str(geneInfo))
        for transcript in self.targetableTranscripts:
            print("Submitting transcript info for %s" %(transcript))
            transcriptInfo = {"PartitionKey" : transcript,
                              "RowKey" : "info",
                              "gene" : self.ensg,
                              "transcripts" : json.dumps(self.targetableTranscripts)}
            if not args.mock:
                submitted = False
                failures = 0
                while not submitted and failures <= 10:
                    try:
                        submitted = tableHandle.insert_entity(tableName, transcriptInfo)
                        #self.getBackDataFromAzureTable(tableHandle, tableName, transcriptInfo["PartitionKey"], transcriptInfo["RowKey"])
                    except azure.common.AzureConflictHttpError:
                        print("Data already in Azure table.", file = sys.stderr)
                        submitted = True
                    except Exception as e:
                        print(e)
                        time.sleep(5)
                        failures += 1
                        continue
                if not submitted:
                    submitted = tableHandle.insert_entity(tableName, transcriptInfo)
                    #self.getBackDataFromAzureTable(tableHandle, tableName, transcriptInfo["PartitionKey"], transcriptInfo["RowKey"])
            else:
                print("Mock submission: " + str(transcriptInfo))
            #print(submissionLists)
            for targetList in list(submissionLists[transcript].keys()):
                print("Submitting target list %s of %s" %(targetList + 1, len(submissionLists[transcript].keys())), end = "\r")
                if not args.mock:
                    submitted = False
                    failures = 0
                    while not submitted and failures <= 10:
                        try:
                            if not submitted:
                                print("\nSubmitting after %s failures." %(failures))
                                #print(submissionLists[transcript][targetList])
                                submitted = tableHandle.insert_entity(tableName, submissionLists[transcript][targetList])
                                print("SUBMITTED!")
                                #self.getBackDataFromAzureTable(tableHandle, tableName, submissionLists[transcript][targetList]["PartitionKey"], submissionLists[transcript][targetList]["RowKey"])
                        except azure.common.AzureConflictHttpError:
                            print("Data already in Azure table.", file = sys.stderr)
                            submitted = True
                        except Exception as e:
                            print("Hit exception")
                            print(e)
                            time.sleep(5)
                            failures += 1
                            continue
                    if not submitted:
                        submitted = tableHandle.insert_entity(tableName, submissionLists[transcript][targetList])
                        #self.getBackDataFromAzureTable(tableHandle, tableName, submissionLists[transcript][targetList]["PartitionKey"], submissionLists[transcript][targetList]["RowKey"])
                else:
                    print("\nMock submit: " + str(submissionLists[transcript][targetList]))
 
    def getBackDataFromAzureTable(self, tableHandle, azureTableName, partitionKey, rowKey):
        print("Getting results back from Azure")
        results = tableHandle.get_entity(azureTableName, partitionKey, rowKey)
        print(results)                   
        
   
def main():
    import datetime
    import ensemblDataConversion
    import os
    import pickle
    translationStartFile = open("hg38TranslationStarts.pkl",'rb')
    global translationStartDict
    translationStartDict = pickle.load(translationStartFile)
    translationStartFile.close()
    geneSymbolConversion = ensemblDataConversion.SymbolToENSG()
    transcriptIDConversion = ensemblDataConversion.ENSGToENST()
    start = datetime.datetime.now()
    global args
    args = CheckArgs()
    if args.ensg:
        print("Using ensembl gene ID %s" %(args.ensg))
        ensg = args.ensg
    elif args.geneSymbol:
        print("Using gene symbol %s" %(args.geneSymbol))
        ensg = geneSymbolConversion.convert(args.geneSymbol)[0]
    enstList = transcriptIDConversion.convert(ensg, biotypeFilter = "protein_coding")
    targetCollection = []
    for enst in enstList:
        print("Processing %s" %(enst[0]))
        if not enst[0] in translationStartDict:
            print("Transcript %s does not have a canonical start site listed." %(enst[0]))
            continue
        exonData = TranscriptAnalysis(enst[0])
        if exonData.proteinLength:  #if this comes back false, we are probably looking at a bad transcript.
            targetFinder = TargetFinder(exonData, 20, "NGG")
            targetCollection += targetFinder.matches
    targetSiteSet = set()
    transcriptTargetData = {}
    for target in targetCollection:
        targetSiteSet.add((target.sequence.upper(), target.azimuthSeq))
        if not target.targetGroup in transcriptTargetData:
            transcriptTargetData[target.targetGroup] = []
        transcriptTargetData[target.targetGroup].append((target.sequence.upper(), target.beforeAltStart, target.lastExon))
    targetSiteSet = list(targetSiteSet)
    targetSiteSet = getUniqueTargets(targetSiteSet, 0)
    for key in list(transcriptTargetData.keys()):
        transcriptTargetData[key] = getUniqueTargets(transcriptTargetData[key], 0)
    jobList = JobList(targetSiteSet, ensg, "crispr", "hg38")
    geneTranscriptData = GeneTranscriptData(transcriptTargetData, ensg)
    print("Submitting Azure Table")
    geneTranscriptData.submitAzureTable("crispr", "hg38")
    if targetSiteSet:
        jobList.submitJobs(30, mock = args.mock)
    else:
        print("No targets found for " + ensg)
        os.mkdir("." + ensg)
        fileName = "." + ensg + os.sep +"no.targets"
        touchFile = open(fileName, 'w')
        touchFile.close()
    print("Found %s targets in %s transcripts." % (len(targetSiteSet), len(enstList)))
    print("Finished in " + str(datetime.datetime.now() - start))
    
main()
        
