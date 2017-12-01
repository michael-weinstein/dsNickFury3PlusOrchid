#!/usr/bin/env python3

class DataPacker(object):
    
    def __init__(self, compressionScheme = False, pamLength = False, guideLength = False, guideExtendLength = False, pamExtendLength = False):  #compressionScheme should be a string with parts in order, such as B,I,B,IH
        import twoBitDNA
        self.twoBitHandle = twoBitDNA.TwoBitDNA()
        self.byteLength = self.twoBitHandle.byteLength
        self.byteOrder = self.twoBitHandle.byteOrder
        if compressionScheme:
            self.setCompressionScheme(compressionScheme)
        self.pamLength = pamLength
        self.guideLength = guideLength
        self.guideExtendLength = guideExtendLength
        self.pamExtendLength = pamExtendLength
        
    def setCompressionScheme(self, compressionScheme):
        self.contigByteLength, self.strandPositionByteLength, self.pamByteLength, self.pamExtendByteLength, self.guideExtendByteLength, self.guideByteLength = compressionScheme
        self.contigStart = 0
        self.strandPositionStart = self.contigStart + self.contigByteLength
        self.pamStart = self.strandPositionStart + self.strandPositionByteLength
        self.pamExtendStart = self.pamStart + self.pamByteLength
        self.guideExtendStart = self.pamExtendStart + self.pamExtendByteLength
        self.guideStart = self.guideExtendStart + self.guideExtendByteLength
        self.compressionScheme = compressionScheme
        self.siteDataByteLength = sum(self.compressionScheme)

    # def setBytePositionsAndProperties(self):
    #     
    #     self.contigBytes = struct.calcsize(self.contigStruct)
    #     self.strandPositionBytes = struct.calcsize(self.strandPositionStruct)
    #     self.pamBytes = struct.calcsize(self.pamStruct)
    #     self.pamExtendBytes = struct.calcsize(self.pamExtendStruct)
    #     self.guideExtendBytes = struct.calcsize(self.guideExtendStruct)
    #     self.guideBytes = struct.calcsize(self.guideStruct)
    #     self.contigByteStart = 0
    #     self.strandPositionByteStart = self.contigByteStart + self.contigBytes
    #     self.pamByteStart = self.strandPositionByteStart + self.strandPositionBytes
    #     self.pamExtendByteStart = self.pamByteStart + self.pamBytes
    #     self.guideExtendByteStart = self.pamExtendByteStart + self.pamExtendBytes
    #     self.guideByteStart = self.guideExtendByteStart + self.guideExtendBytes
    #     self.guideSeqBits, self.guidePackBits = self.twoBitHandle.calculateBitLength(self.guideLength)
        
    def encodePositionAndStrand(self, position, strand):
        position = int(position)
        if strand == "+":
            strandBit = 1
        elif strand == "-":
            strandBit = 0
        else:
            raise RuntimeError("Error, strand value passed must be either + or -")
        return (position << 1) + strandBit 
    
    def decodePositionAndStrand(self, encoded):
        encoded = int(encoded)
        if encoded & 1:  #checking the last bit (where we put the strand info)
            strand = "+"
        else:
            strand = "-"
        position = encoded >> 1
        return (position, strand)
        
    def encodeDNA(self, dna):
        return self.twoBitHandle.encode(dna)
    
    def decodeDNA(self, dna, seqLength):
        return self.twoBitHandle.decode(dna, seqLength)
    
    def getPackingPattern(self, contigByteLength, strandPositionStruct, dnaSeq, guideExtend, pamExtend):  #expected input will be the integer size needed to hold enumerated contigs (deterined elsewhere) and a PAM_GUIDE separated sequence
        positionAndStrandStruct = strandPositionStruct
        pam, guide = dnaSeq.split("_")
        pamStruct = self.twoBitHandle.calculateByteLength(pam)
        guideStruct = self.twoBitHandle.calculateByteLength(guide)
        pamExtendStruct = self.twoBitHandle.calculateByteLength(pamExtend)
        guideExtendStruct = self.twoBitHandle.calculateByteLength(guideExtend)
        return (contigByteLength, positionAndStrandStruct, pamStruct, pamExtendStruct, guideExtendStruct, guideStruct)
    
    # def validatePackingPattern(self, packingPattern):
    #     packingPattern = packingPattern.replace(",","")
    #     for character in packingPattern:
    #         if character not in "QIHB":
    #             return False
    #     return True
    
    def packData(self, enumeratedContig, startPosition, strand, seq, guideExtension, pamExtension, packingPattern = False):  #contigShould be the enumerated integer
        if not packingPattern:
            packingPattern = self.compressionScheme
        if not packingPattern: #if there is not one saved in the object already
            raise RuntimeError("No packing pattern given or stored")
        if not type(enumeratedContig) == int:
            raise RuntimeError("Contig for packing should already be enumerated")
        dataByteString = bytes()
        dataByteString += int(enumeratedContig).to_bytes(self.contigByteLength, self.byteOrder)
        dataByteString += self.encodePositionAndStrand(startPosition, strand).to_bytes(self.strandPositionByteLength, self.byteOrder)
        pam, guide = seq.split("_")
        dataByteString += self.encodeDNA(pam).to_bytes(self.pamByteLength, self.byteOrder)
        dataByteString += self.encodeDNA(guideExtension).to_bytes(self.guideExtendByteLength, self.byteOrder)
        dataByteString += self.encodeDNA(pamExtension).to_bytes(self.pamExtendByteLength, self.byteOrder)
        dataByteString += self.encodeDNA(guide).to_bytes(self.guideByteLength, self.byteOrder)
        return dataByteString
    
    def unpackData(self, data, packingPattern = False):  #data should come in as a bytestream
        if not packingPattern:
            packingPattern = self.compressionScheme
        if not packingPattern:
            raise RuntimeError("No packing pattern available for struct unpacking")
        contigByteString = data[self.contigStart : self.contigStart + self.contigByteLength]
        positionStrandByteString = data[self.strandPositionStart : self.strandPositionStart + self.strandPositionByteLength]
        pamByteString = data[self.pamStart : self.pamStart + self.pamByteLength]
        pamExtensionByteString = data[self.pamExtendStart : self.pamExtendStart + self.pamExtendByteLength]
        guideExtensionByteString = data[self.guideExtendStart : self.guideExtendStart + self.guideExtendByteLength]
        guideByteString = data[self.guideStart : self.guideStart + self.guideByteLength]
        enumeratedContig = int.from_bytes(contigByteString , self.byteOrder)
        encodedPositionAndStrand = int.from_bytes(positionStrandByteString , self.byteOrder)
        encodedPam = int.from_bytes(pamByteString , self.byteOrder)
        encodedPamExtension = int.from_bytes(pamExtensionByteString , self.byteOrder)
        encodedGuideExtension = int.from_bytes(guideExtensionByteString , self.byteOrder)
        encodedGuide = int.from_bytes(guideByteString , self.byteOrder)
        return (enumeratedContig, encodedPositionAndStrand, encodedPam, encodedPamExtension, encodedGuideExtension, encodedGuide)
        
    def decodeData(self, data, packingPattern = False, guideLength = False, pamLength = False, guideExtendLength = False, pamExtendLength = False):
        if not packingPattern:
            packingPattern = self.compressionScheme
        if not packingPattern:
            raise RuntimeError("No packing pattern available for struct unpacking")
        if not guideLength:
            guideLength = self.guideLength
        if not guideLength:
            raise RuntimeError("No guide length available for decoding DNA")
        if not pamLength:
            pamLength = self.pamLength
        if not pamLength:
            raise RuntimeError("No pam length available for decoding DNA")
        if not pamExtendLength:
            pamExtendLength = self.pamExtendLength
        if not pamExtendLength:
            raise RuntimeError("No pam extended length available for decoding DNA")
        if not guideExtendLength:
            guideExtendLength = self.guideExtendLength
        if not guideExtendLength:
            raise RuntimeError("No guide extend length available for decoding DNA")
        enumeratedContig, encodedPositionAndStrand, encodedPam, encodedGuideExtension, encodedPamExtension, encodedGuide = self.unpackData(data, packingPattern)
        position, strand = self.decodePositionAndStrand(encodedPositionAndStrand)
        pam = self.decodeDNA(encodedPam, pamLength)
        guide = self.decodeDNA(encodedGuide, guideLength)
        guideExtension = self.decodeDNA(encodedGuideExtension, guideExtendLength)
        pamExtension = self.decodeDNA(encodedPamExtension, pamExtendLength)
        return SiteData(enumeratedContig, position, pam + "_" + guide, guideExtension, pamExtension, strand)
    
    def qualifySite(self, dataStruct, encodedDNA, shortestSeqLength, mismatchTolerance, endClip):
        longSeqBytes = dataStruct[self.guideStart:]
        longSeq = int.from_bytes(longSeqBytes, self.byteOrder)
        return self.twoBitHandle.withinMismatchToleranceAndCount(encodedDNA, longSeq, shortestSeqLength, mismatchTolerance, endClip)
    
    # def packedMismatchCount(self, dataStruct, encodedDNA, shortestSeqLength, alreadyComparedBases = 0, alreadyFoundMismatches = 0, endClip = 0):
    #     #longSeq will be the (potentially) longer sequence stored for comparison, shortSeq will be from the target itself, which can be no longer than the reference
    #     longSeqBytes = dataStruct[self.guideStart:]
    #     longSeq = int.from_bytes(longSeqBytes, self.byteOrder)
    #     return self.twoBitHandle.countMismatches(longSeq, encodedDNA, shortestSeqLength, endClip, alreadyComparedBases, alreadyFoundMismatches)
    # 
    # def packedMismatchCount2(self, dataStruct, encodedDNA, shortestSeqLength, mismatchTolerance, alreadyComparedBases = 0, alreadyFoundMismatches = 0, endClip = 0):
    #     #similar to the above function, but faster if we can reject after a number of mismatches
    #     longSeqBytes = dataStruct[self.guideStart:]
    #     longSeq = int.from_bytes(longSeqBytes, self.byteOrder)
    #     return self.twoBitHandle.withinMismatchTolerance(longSeq, encodedDNA, shortestSeqLength, mismatchTolerance, endClip, alreadyComparedBases, alreadyFoundMismatches)
    # 
    def getPAMSeq(self, seqStruct):
        pamBytes = seqStruct[self.pamStart : self.pamStart + self.pamByteLength]
        return self.decodeDNA(int.from_bytes(pamBytes, self.byteOrder) , self.pamLength)
        
    def qualifyingSeqTableFromBuffer(self, seqBuffer, guideSeq, canonicalPAM, mismatchTolerance, endClip):
        encodedGuide = self.encodeDNA(guideSeq[::-1])
        matchBytes = {}
        if canonicalPAM:
            import degenerateBaseHandle
            if "," in canonicalPAM:
                canonicalPAMSeq, canonicalPAMMode = canonicalPAM.split(",")
                canonicalPAMMode = int(canonicalPAMMode)
            else:
                canonicalPAMSeq = canonicalPAM
                canonicalPAMMode = 1
            rangeExtension = calculatePotentialPamMismatch(canonicalPAM)
            if canonicalPAMMode == 1:
                canonicalPAMList = degenerateBaseHandle.NondegenerateBases(canonicalPAMSeq).permutations()  #this should work whether or not there is a comma in the canonical PAM
            if canonicalPAMMode == 2:
                canonicalPAMList = self.createCanonicalPAMLetterLists(canonicalPAMSeq)
        else:
            rangeExtension = 0
            canonicalPAMList = False
        for i in range(0,mismatchTolerance + 1 + rangeExtension + endClip): 
            matchBytes[i] = bytes()
        position = 0
        matchCount = 0
        while position < len(seqBuffer):
            currentSiteBytes = seqBuffer[position : position + self.siteDataByteLength]
            mismatchCount = self.qualifySite(currentSiteBytes, encodedGuide, len(guideSeq), mismatchTolerance, endClip)
            if mismatchCount != -1:
                matchCount += 1
                if canonicalPAM:
                    pam = self.getPAMSeq(currentSiteBytes)[::-1]   #this will probably need to be reversed
                    mismatchCount += self.calculatePAMMismatches(pam, canonicalPAMMode, canonicalPAMList)
                matchBytes[mismatchCount] += currentSiteBytes
            position += self.siteDataByteLength
        return (matchCount, matchBytes)
    
    def calculatePAMMismatches(self, pam, mode, sequenceList):  #the list will come in as a matrix if mode 2 or a list of sequences if 1
        if mode == 1:
            if not pam in sequenceList:
                return 1
            else:
                return 0
        if mode == 2:
            mismatches = 0
            for i in range(0, len(pam)):
                if pam[i] not in sequenceList[i]:
                    mismatches += 1
            return mismatches
        else:
            raise RuntimeError("Error: Canonical PAM mode must be either 1 or 2")
        
    def createCanonicalPAMLetterLists(self, sequence):
        import degenerateBaseHandle
        baseMatrix = []
        for letter in sequence:
            baseMatrix.append(degenerateBaseHandle.NondegenerateBases(letter).permutations())
        return baseMatrix
    
    def calculateByteLength(self, number):  #for the love of all things good and holy, please use the largest possible number.  This will mostly be for analyzing the enumerated contigs to determine byte length needed
        import math
        fractionalBitRequirement = math.log(number, 2)
        bitRequirement = int(fractionalBitRequirement)
        if fractionalBitRequirement > bitRequirement:
            bitRequirement += 1
        byteRequirement = -(-bitRequirement // self.byteLength)  #shortcut for doing ceiling division
        if byteRequirement == 0:
            raise RuntimeError("Error: Told to calculate a byte length requirement for zero.  This is almost certainly an error.")
        return byteRequirement
    
    def dumpSiteBuffer(self, siteBuffer, contigDenumerationTable):
        position = 0
        sites = []
        while position < len(siteBuffer):
            currentSiteBytes = siteBuffer[position : position + self.siteDataByteLength]
            siteData = self.decodeData(currentSiteBytes)
            sites.append([siteData.sequence[::-1], contigDenumerationTable[siteData.enumeratedContig], str(siteData.start), str(siteData.end)])
            if siteData.sequence[::-1] == "TCAAGCCGACGGGTCTAGAG_GGG":
                print("Found it")
                longSeqBytes = currentSiteBytes[self.guideStart:]
                longSeq = int.from_bytes(longSeqBytes, self.byteOrder)
                print(longSeq)
                import time
                time.sleep(10)
            position += self.siteDataByteLength
        for site in sites:
            print("\t".join(site))
            
def calculatePotentialPamMismatch(canonicalPAM):
    potentialMismatches = 0
    if "," in canonicalPAM:
        sequence, mode = canonicalPAM.split(",")
        mode = int(mode)
    else:
        sequence = canonicalPAM
        mode = 1
    if mode == 1:
        return 1
    if mode == 2:
        for letter in sequence:
            if letter != "N":
                potentialMismatches += 1
        return potentialMismatches
    else:
        raise RuntimeError("Canonical PAM mode should be either 1 or 2.  %s was found." %(mode))
                
class SiteData(object):
    
    def __init__(self, enumeratedContig, start, sequence, guideExtension, pamExtension, strand):
        self.enumeratedContig = enumeratedContig
        self.start = start
        self.end = start + len(sequence.replace("_","")) + 1
        self.guideExtension = guideExtension
        self.pamExtension = pamExtension
        self.sequence = sequence
        self.strand = strand