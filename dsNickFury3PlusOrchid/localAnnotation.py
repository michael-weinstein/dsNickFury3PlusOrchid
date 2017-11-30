#!/usr/bin/env python3

class LocalGeneCheck(object):
    
    def __init__(self):
        self.fileName = "locusGeneCheck.pkl"
        self.clusterSize = 10000000
        self.conversionTable = self.loadTable()
        self.biotypeSpace = self.getBiotypeSpace()

    def renewTable(self):
        self.conversionTable = self.loadTable(True)
    
    def getBiotypeSpace(self):
        biotypes = set()
        for contig in self.conversionTable:
            for cluster in self.conversionTable[contig]:
                for gene in self.conversionTable[contig][cluster]:
                    biotypes.add(gene[3])
        biotypes = list(biotypes)
        biotypes.sort()
        return biotypes
        
    def checkLocus(self, contig, start, end = False, biotypeFilter = False):
        contig = str(contig)
        contig = contig.upper()
        if contig == "M":
            contig = "MT"
        if biotypeFilter:
            if type(biotypeFilter) == str:
                biotypeFilter = [biotypeFilter]
            for biotype in biotypeFilter:
                if not biotype in self.biotypeSpace:
                    print("Warning: Biotype %s not a biotype found in list of loci." %(biotype))
        if not type(start) == int:
            raise RuntimeError("Error, start value must be an integer.")
        if end and not type(end) == int:
            raise RuntimeError("Error, end value must be an integer")
        if end:
            if start > end:
                raise RuntimeError("Error, start position cannot be larger than end position.")
        if not contig in self.conversionTable:
            raise RuntimeError("Error, no entries for supplied chromosome:" + contig)
        if not end:
            geneList = []
            cluster = start // self.clusterSize
            for gene in self.conversionTable[contig][cluster]:
                if gene[0] <= start and gene[1] >= start:
                    if not biotypeFilter or gene[3] in biotypeFilter:
                        geneList.append(gene)
                if gene[0] > start:
                    return geneList
            return geneList
        else:
            geneList = []
            countedGenes = []
            startCluster = start // self.clusterSize
            endCluster = end // self.clusterSize
            if startCluster == endCluster:
                for gene in self.conversionTable[contig][startCluster]:
                    if (gene[0] >= start and gene[0] <= end) or (gene[1] >= start and gene[1] <= end) or (gene[0] <= start and gene[1] >= end) or (gene[0] >= start and gene[1] <= end):  #just described starting in, ending in, interval contained in gene, or gene contained in interval
                        if not gene[2] in countedGenes:
                            if not biotypeFilter or gene[3] in biotypeFilter:
                                countedGenes.append(gene[2])
                                geneList.append(gene[2])
            else:
                for cluster in range(startCluster, endCluster + 1):
                    if cluster == startCluster:
                        for gene in self.conversionTable[contig][cluster]:
                            if gene[1] >= start:
                                if not gene[2] in countedGenes:
                                    if not biotypeFilter or gene[3] in biotypeFilter:
                                        geneList.append(gene[2])
                                        countedGenes.append(gene[2])
                    elif cluster != endCluster:
                        for gene in self.conversionTable[contig][cluster]:
                            if not gene[2] in countedGenes:
                                if not biotypeFilter or gene[3] in biotypeFilter:
                                    geneList.append(gene[2]) #we don't need to check location here because this whole cluster should be in the interval in question
                                    countedGenes.append(gene[2])
                    else:  # only possibility left should be the final cluster
                        for gene in self.conversionTable[contig][cluster]:
                            if gene[0] <= end:
                                if not gene[2] in countedGenes:
                                    if not biotypeFilter or gene[3] in biotypeFilter:
                                        geneList.append(gene[2])
                                        countedGenes.append(gene[2])
            return geneList                        
    
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

    def getDatabase(self):
        import operator
        clusterSize = self.clusterSize
        import pymysql
        ensemblDb = pymysql.connect(host='ensembldb.ensembl.org',
                                    user='anonymous',
                                    password='',
                                    db='ensembl_website_88',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        ensemblConnection = ensemblDb.cursor()
        query = "SELECT\
                    display_label, location, homo_sapiens_core_88_38.gene.biotype\
                 FROM\
                    gene_autocomplete, homo_sapiens_core_88_38.gene\
                 WHERE\
                    species = 'homo_sapiens' and gene_autocomplete.stable_id = homo_sapiens_core_88_38.gene.stable_id"        
        ensemblConnection.execute(query)
        rawConversionTable = ensemblConnection.fetchall()
        conversionTable = {}
        for item in rawConversionTable:
            locus = item["location"]
            contig, position = locus.split(":")
            start, end = position.split("-")
            start = int(start)
            end = int(end)
            startCluster = start // clusterSize
            endCluster = end // clusterSize
            if not contig in conversionTable:
                conversionTable[contig] = {}
            for cluster in range(startCluster, endCluster + 1):
                if not cluster in conversionTable[contig]:
                    conversionTable[contig][cluster] = []
            if startCluster == endCluster:
                conversionTable[contig][startCluster].append((start, end, item["display_label"].upper(), item["biotype"]))
            else:
                for cluster in range(startCluster, endCluster + 1):
                    if cluster == startCluster:
                        conversionTable[contig][cluster].append((start, (cluster + 1) * clusterSize, item["display_label"].upper(), item["biotype"]))
                    elif cluster != endCluster:
                        conversionTable[contig][cluster].append((cluster * clusterSize, (cluster + 1) * clusterSize, item["display_label"].upper(), item["biotype"]))
                    else:  #only possibility left is the cluster being the final cluster
                        conversionTable[contig][cluster].append((cluster * clusterSize, end, item["display_label"].upper(), item["biotype"]))
        for contig in list(conversionTable.keys()):
            for cluster in list(conversionTable[contig]):
                conversionTable[contig][cluster].sort(key = operator.itemgetter(0))
        return conversionTable
        
# def main():
#     checker = LocalGeneCheck()
#     test = checker.checkLocus("12", 109809469, biotypeFilter = "protein_coding")
#     uselessValue = True
#     useless1 = uselessValue
#     quit()
#     
# main()