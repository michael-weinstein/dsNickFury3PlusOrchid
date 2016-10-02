#!/usr/bin/env python3

'''
open GTF
iterate over
for each line
    split line on tabs
        0: contig (strip off any beginning chr)
        1: source
        2: feature
        3: start
        4: stop
        5: score
        6: strand (+ or -)
        7: frame
        8: attributes
    filter for feature type
        gene
        transcript
        start_codon
'''

class GTFLine(object):
    
    def __init__(self, rawLine, featureFilters = []):
        self.rawLine = rawLine
        self.unpackLine()
        if not featureFilters or self.feature in featureFilters:
            self.filteredOut = False
            self.unpackAttributes()
        else:
            self.filteredOut = True
        
    def unpackLine(self):
        self.contig, self.source, self.feature, start, stop, score, self.strand, frame, self.attributes = self.rawLine.split("\t")
        if frame == ".":
            self.frame = None
        else:
            self.frame = int(frame)
        self.start = int(start)
        self.stop = int(stop)
        if score == ".":
            self.score = None
        else:
            self.score = float(score)
        
    def unpackAttributes(self):
        attributeDict = {}
        attributeList = self.attributes.split("; ")
        attributeList = [item.strip() for item in attributeList]
        for attribute in attributeList:
            if not attribute:
                continue
            attributeSplit = attribute.split('"')
            key = attributeSplit[0].strip()
            value = attributeSplit[1].strip()
            value.strip(";")
            value = value.strip('"')
            if key in ["contig", "source", "feature", "start", "stop", "score", "strand", "frame", "attributes"]:
                raise RuntimeError("Reserved key used in line: %s" %(self.rawLine))
            attributeDict[key] = value
        if self.feature == "transcript":
            if not "transcript_support_level" in attributeDict:
                attributeDict['transcript_support_level'] = None
            else:
                try:
                    attributeDict['transcript_support_level'] = int(attributeDict['transcript_support_level'])
                except ValueError:
                    attributeDict['transcript_support_level'] = None
        self.__dict__.update(attributeDict)

def main():
    import datetime
    runStart = datetime.datetime.now()
    gene2transcript = {}
    #transcriptStartPosition = {}
    translationStartSite = {}
    gtFile = open("Homo_sapiens.GRCh38.85.gtf",'r')
    rawline = gtFile.readline().strip()
    rawline = rawline.strip(";")
    progress = 0
    transcriptCount = 0
    geneCount = 0
    #rawline = '1\thavana\ttranscript\t11869\t14409\t.\t+\t.\tgene_id "ENSG00000223972"; gene_version "5"; transcript_id "ENST00000456328"; transcript_version "2"; gene_name "DDX11L1"; gene_source "havana"; gene_biotype "transcribed_unprocessed_pseudogene"; havana_gene "OTTHUMG00000000961"; havana_gene_version "2"; transcript_name "DDX11L1-002"; transcript_source "havana"; transcript_biotype "processed_transcript"; havana_transcript "OTTHUMT00000362751"; havana_transcript_version "1"; tag "basic"; transcript_support_level "1"'
    while rawline:
        if progress % 10000 == 0:
            print("Processed %s lines. Found %s transcripts in %s genes." %(progress, transcriptCount, geneCount), end = "\r")
        progress += 1
        if rawline.startswith("#"):
            rawline = gtFile.readline().strip()
            continue
        line = GTFLine(rawline, ["gene", "transcript","start_codon"])
        if line.filteredOut:
            rawline = gtFile.readline().strip()
            continue
        if line.feature == "gene":
            try:
                gene2transcript[line.gene_id] = []
            except AttributeError:
                raise RuntimeError("Failed on line: %s" %(line.rawLine))
            geneCount += 1
        elif line.feature == "transcript":
            try:
                gene2transcript[line.gene_id].append((line.transcript_id, line.transcript_biotype, line.transcript_support_level))
                currentTranscript = line.transcript_id
                if line.strand == "+":
                    currentTranscriptStart = line.start
                elif line.strand == "-":
                    currentTranscriptStart = line.stop
                else:
                    raise RuntimeError("Got an invalid strand value on line: %s" %(line.rawLine))
            except AttributeError:
                raise RuntimeError("Failed on line: %s" %(line.rawLine))
            transcriptCount += 1
        elif line.feature == "start_codon":
            if line.transcript_id != currentTranscript:
                raise RuntimeError("Got a mismatched start codon and transcript. Expected transcript: %s, start codon transcript: %s" %(currentTranscript, line.transcript_id))
            if line.strand == "+":
                translationStartSite[currentTranscript] = line.start - currentTranscriptStart
            elif line.strand == "-":
                translationStartSite[currentTranscript] = currentTranscriptStart - line.stop
        rawline = gtFile.readline().strip()
    print("Processed %s lines. Found %s transcripts in %s genes." %(progress, transcriptCount, geneCount))
    gtFile.close()
    print("Parsed file in %s" %(datetime.datetime.now() - runStart))
    testsites = ["ENST00000418703", "ENST00000261740", "ENST00000544971"]
    for site in testsites:
        start = datetime.datetime.now()
        value = translationStartSite[site]
        runtime = datetime.datetime.now() - start
        print("Found that %s starts at %s in %s" %(site, value, runtime))
    import pickle
    pickleOut = open("hg38TranslationStarts.pkl",'wb')
    pickle.dump(translationStartSite, pickleOut)
    pickleOut.close()
    print("Pickle file written")
main()