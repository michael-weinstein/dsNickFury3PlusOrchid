#!/usr/bin/env python3

class EnsemblConversion(object):
    
    def __init__(self):
        pass
    
    def renewTable(self):
        self.conversionTable = loadTable(True)
        
    def convert(self, key):
        key = key.upper()  #going to be case insensitive in almost all cases.  This will prevent case-related problems
        value = ""
        if key in self.conversionTable:
            value = self.conversionTable[key]
        else:
            raise RuntimeError("Sorry, unable to find a conversion for " + key)
        return value
    
    def loadTable(self, renew = False):
        import pickle
        if not renew:
            try:
                savedTable = open(self.fileName,'rb')
                conversionTable = pickle.load(savedTable)
                savedTable.close()
                return conversionTable
            except FileNotFoundError:
                renew = True
        if renew:
            conversionTable = self.getDatabase()
            savedTable = open(self.fileName,'wb')
            pickle.dump(conversionTable, savedTable)
            savedTable.close()
            return conversionTable
    
class RefSeqToENST(EnsemblConversion):

    def __init__(self):
        self.fileName = "refSeqToENSTTable.pkl"
        self.conversionTable = self.loadTable()

    def convert(self, refSeqID):
        conversionTable = loadRefSeqtoENSTTable()
        ensemblTranscriptID = ""
        try:
            ensemblTranscriptID = conversionTable[refSeqID]
        except KeyError:
            simplifiedID = refSeqID.split(".")[0]
            tableKeys = list(conversionTable.keys())
            for key in tableKeys:
                simplifiedKey = key.split(".")[0]
                if simplifiedID == simplifiedKey:
                    ensemblTranscriptID =conversionTable[key]
        if not ensemblTranscriptID:
            raise RuntimeError("Sorry, unable to figure out which Ensembl ID goes with " + refSeqID)
        return ensemblTranscriptID
    
    def getDatabase(self):
        import pymysql
        ensemblDb = pymysql.connect(host='ensembldb.ensembl.org',
                                    user='anonymous',
                                    password='',
                                    db='homo_sapiens_core_85_38',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        ensemblConnection = ensemblDb.cursor()
        query ="SELECT \
                    transcript.stable_id, xref.display_label \
                FROM \
                    transcript, object_xref, xref,external_db \
                WHERE \
                        object_xref.xref_id = xref.xref_id \
                    AND object_xref.ensembl_id = transcript.transcript_id \
                    AND object_xref.ensembl_object_type = 'Transcript' \
                    AND xref.external_db_id = external_db.external_db_id \
                    AND external_db.db_name = 'RefSeq_mRNA'"
        ensemblConnection.execute(query)
        rawConversionTable = ensemblConnection.fetchall()
        conversionTable = {}
        for item in rawConversionTable:
            ensemblTranscriptID = item['stable_id']
            refSeqTranscriptID = item['display_label']
            conversionTable[refSeqTranscriptID] = ensemblTranscriptID
        return conversionTable

##################Converting geneID to transcriptID list

class ENSGToENST(EnsemblConversion):
    
    def __init__(self):
        self.fileName = "ensgToENSTTable.pkl"
        self.conversionTable = self.loadTable()
        self.biotypeSpace = self.getBiotypeSpace()
        
    def getBiotypeSpace(self):
        biotypes = set()
        for gene in self.conversionTable:
            for transcript in self.conversionTable[gene]:
                biotypes.add(transcript[1])
        biotypes = list(biotypes)
        biotypes.sort()
        return biotypes
    
    def convert(self, ensg, biotypeFilter = False):
        if biotypeFilter:
            if type(biotypeFilter) == str:
                biotypeFilter = [biotypeFilter]
            for biotype in biotypeFilter:
                if not biotype in self.biotypeSpace:
                    print("Warning: Biotype %s not a biotype found in list of loci." %(biotype))
        ensg = ensg.upper()  #going to be case insensitive in almost all cases.  This will prevent case-related problems
        value = []
        if ensg in self.conversionTable:
            for transcript in self.conversionTable[ensg]:
                if not biotypeFilter or transcript[1] in biotypeFilter:
                    value.append(transcript)
        else:
            raise RuntimeError("Sorry, unable to find a conversion for " + ensg)
        return value        
        
    def getDatabase(self):
        import pymysql
        ensemblDb = pymysql.connect(host='ensembldb.ensembl.org',
                                    user='anonymous',
                                    password='',
                                    db='homo_sapiens_core_85_38',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        ensemblConnection = ensemblDb.cursor()
        query = "SELECT \
                    gene.stable_id as 'GENE', transcript.stable_id as 'TRANSCRIPT', transcript.biotype\
                FROM\
                    transcript, gene\
                WHERE\
                    transcript.gene_id = gene.gene_id"
        ensemblConnection.execute(query)
        rawConversionTable = ensemblConnection.fetchall()
        conversionTable = {}
        for item in rawConversionTable:
            if not item['GENE'] in conversionTable:
                conversionTable[item['GENE']] = []
            conversionTable[item['GENE']].append((item['TRANSCRIPT'],item['biotype']))
        return conversionTable

#converting gene symbol to ENSG

class SymbolToENSG(EnsemblConversion):
    
    def __init__(self):
        self.fileName = "symbolToENSG.pkl"
        self.conversionTable = self.loadTable()
        
    def getDatabase(self):
        import pymysql
        ensemblDb = pymysql.connect(host='ensembldb.ensembl.org',
                                    user='anonymous',
                                    password='',
                                    db='ensembl_website_85',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        ensemblConnection = ensemblDb.cursor()
        query = "SELECT\
                    display_label, gene_autocomplete.stable_id, homo_sapiens_core_85_38.gene.biotype\
                 FROM\
                    gene_autocomplete, homo_sapiens_core_85_38.gene\
                 WHERE\
                    species = 'homo_sapiens' and gene_autocomplete.stable_id = homo_sapiens_core_85_38.gene.stable_id"        
        ensemblConnection.execute(query)
        rawConversionTable = ensemblConnection.fetchall()
        conversionTable = {}
        for item in rawConversionTable:
            conversionTable[item["display_label"].upper()] = (item["stable_id"].upper(), item["biotype"])
        
        ensemblDb = pymysql.connect(host='ensembldb.ensembl.org',
                                    user='anonymous',
                                    password='',
                                    db='homo_sapiens_core_85_38',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        ensemblConnection = ensemblDb.cursor()
        query = "SELECT\
                    synonym, ensembl_website_85.gene_autocomplete.stable_id, biotype\
                FROM\
                    external_synonym, xref, ensembl_website_85.gene_autocomplete, gene\
                WHERE\
                        external_synonym.xref_id = xref.xref_id\
                    AND	xref.display_label = ensembl_website_85.gene_autocomplete.display_label\
                    AND ensembl_website_85.gene_autocomplete.species = 'homo_sapiens'\
                    AND ensembl_website_85.gene_autocomplete.stable_id = gene.stable_id"        
        ensemblConnection.execute(query)
        rawConversionTable = ensemblConnection.fetchall()
        for item in rawConversionTable:
            if not item["synonym"] in conversionTable:
                conversionTable[item['synonym'].upper()] = ((item['stable_id'].upper(),item['biotype']))
        return conversionTable 

#  getting a list of genes and their coordinates

class GenesFromChromosomeInterval(EnsemblConversion):
    
    def __init__(self):
        self.fileName = "geneFromLocus.pkl"
        self.clusterSize = 10000000
        self.conversionTable = self.loadTable()
        self.biotypeSpace = self.getBiotypeSpace()
        
    def getBiotypeSpace(self):
        biotypes = set()
        for contig in self.conversionTable:
            for gene in self.conversionTable[contig]:
                biotypes.add(gene[4])
        biotypes = list(biotypes)
        biotypes.sort()
        return biotypes
        
    def convert(self, contig, start = False, end = False, biotypeFilter = False, value = False):
        if value:
            if not type(value) == str:
                raise RuntimeError("Value type for return must be a string.")
            value = value.upper()
            if value == "SYMBOL":
                column = 2
            elif value == "ENSG":
                column = 3
            else:
                raise RuntimeError()
        if biotypeFilter:
            if type(biotypeFilter) == str:
                biotypeFilter = [biotypeFilter]
            for biotype in biotypeFilter:
                if not biotype in self.biotypeSpace:
                    print("Warning: Biotype %s not a biotype found in list of loci." %(biotype))
        contig = str(contig)
        if start and end:
            if start > end:
                raise RuntimeError("Error, start position cannot be larger than end position.")
        if not contig in self.conversionTable:
            raise RuntimeError("Error, no entries for supplied chromosome:" + contig)
        if not start and not end and not biotypeFilter:
            return self.conversionTable[contig]
        if not start and not end and biotypeFilter:
            geneList = []
            for gene in self.conversionTable[contig]:
                if gene[4] in biotypeFilter:
                    geneList.append(gene)
            if value:
                return [gene[column] for gene in geneList]
            else:
                return geneList
        elif start and not end:
            geneList = []
            for gene in self.conversionTable[contig]:
                if gene[1] >= start:
                    if not biotypeFilter or gene[4] in biotypeFilter:
                        geneList.append(gene)
            if value:
                return [gene[column] for gene in geneList]
            else:
                return geneList
        elif end and not start:
            geneList = []
            for gene in self.conversionTable[contig]:
                if gene[0] <= end:
                    if not biotypeFilter or gene[4] in biotypeFilter:
                        geneList.append(gene)
            if value:
                return [gene[column] for gene in geneList]
            else:
                return geneList
        elif start and end:
            geneList = []
            for gene in self.conversionTable[contig]:
                if (gene[0] >= start and gene[0] <= end) or (gene[1] >= start and gene[1] <= end) or (gene[0] <= start and gene[1] >= end) or (gene[0] >= start and gene[1] <= end):  #just described starting in, ending in, interval contained in gene, or gene contained in interval
                    if not biotypeFilter or gene[4] in biotypeFilter:
                        geneList.append(gene)
            if value:
                return [gene[column] for gene in geneList]
            else:
                return geneList
        
    def getDatabase(self):
        import operator
        clusterSize = self.clusterSize
        import pymysql
        ensemblDb = pymysql.connect(host='ensembldb.ensembl.org',
                                    user='anonymous',
                                    password='',
                                    db='ensembl_website_85',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        ensemblConnection = ensemblDb.cursor()
        query = "SELECT\
                    display_label, gene_autocomplete.stable_id, location, homo_sapiens_core_85_38.gene.biotype\
                 FROM\
                    gene_autocomplete, homo_sapiens_core_85_38.gene\
                 WHERE\
                    species = 'homo_sapiens' and gene_autocomplete.stable_id = homo_sapiens_core_85_38.gene.stable_id"        
        ensemblConnection.execute(query)
        rawConversionTable = ensemblConnection.fetchall()
        conversionTable = {}
        for item in rawConversionTable:
            locus = item["location"]
            contig, position = locus.split(":")
            start, end = position.split("-")
            start = int(start)
            end = int(end)
            startCluster = start % clusterSize
            endCluster = end % clusterSize
            if not contig in conversionTable:
                conversionTable[contig] = []
            conversionTable[contig].append((start, end, item['display_label'], item['stable_id'], item['biotype']))
        for contig in list(conversionTable.keys()):
            conversionTable[contig].sort(key = operator.itemgetter(0))
        return conversionTable


# def main():
#     #table = loadRefSeqtoENSTTable()
#     #table = loadENSGtoENSTTable()
#     #conversion = SymbolToENSG()
#     # conversion = GenesFromChromosomeInterval()
#     # check = conversion.convert(21, biotypeFilter = "protein_coding")
#     # geneCount = len(check)
#     # useless = True
#     # for line in check:
#     #     if line[2] == "COL18A1":
#     #         print(line)
#     import datetime
#     conversion1 = SymbolToENSG()
#     conversion2 = ENSGToENST()
#     for symbol in ["TRPV4", "GPIHBP1", "SLURP1", "COL18A1"]:
#         startTime = datetime.datetime.now()
#         ensg = conversion1.convert(symbol)
#         transcriptList = conversion2.convert(ensg[0], biotypeFilter = "protein_coding")
#         useless = True
#         runtime = datetime.datetime.now() - startTime
#         print(transcriptList)
#         print("Runtime = %s" %(runtime))
#     quit()
#     
# main()
