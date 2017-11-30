#!/usr/bin/env python3

import settings

class CheckArgs():  #class that checks arguments and ultimately returns a validated set of arguments to the main program
    
    def __init__(self):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--gene", help = "Ensembl gene ID", required = True)
        parser.add_argument("-s", "--genome", help = "Genome to use", required = True)
        parser.add_argument("-l", "--offTargetOutputLimit", help = "Limit number of off-targets listed in output", type = int)
        parser.add_argument("-n", "--noOffTargetList", help = "Do not compile a list of off-targets at all.", action = 'store_true')
        parser.add_argument("-v", "--verbose", help = "Run in verbose mode", action = "store_true")
        rawArgs = parser.parse_args()
        self.gene = rawArgs.gene.upper()
        self.genome = rawArgs.genome.lower()
        offTargetOutputLimit = rawArgs.offTargetOutputLimit
        if type(offTargetOutputLimit) == type(None):
            self.offTargetOutputLimit = False
        elif offTargetOutputLimit < 1:
            raise RuntimeError("Off target output limit must be 1 or greater.")
        else:
            self.offTargetOutputLimit = offTargetOutputLimit
        self.outputOffTargets = not rawArgs.noOffTargetList
        self.verbose = rawArgs.verbose

class geneSiteTable(object):
    
    def __init__(self, tableHandle, genome, geneID, generateOffTargetLists = True, offTargetOutputLimit = False, verbose = False):
        self.verbose = verbose
        self.tableHandle = tableHandle
        self.geneID = geneID
        self.genome = genome
        self.generateOffTargetLists = generateOffTargetLists
        if not self.generateOffTargetLists:
            self.offTargetOutputLimit = False
        elif type(offTargetOutputLimit) == int and offTargetOutputLimit < 1:
            raise RuntimeError("Off target output limit must be at least one")
        else:
            self.offTargetOutputLimit = offTargetOutputLimit
        if verbose:
            print("Downloading transcript list...", end = "", flush = True)
        self.getTranscriptList()
        if verbose:
            print("DONE")
            print("Downloading all site data for gene...", end = "", flush = True)
        self.getAllGeneData()
        if verbose:
            print("DONE")
            print("Compiling a list of targets...", end = "", flush = True)
        self.getTargetList()
        if verbose:
            print("DONE")
            print("Building a blank target table...", end = "", flush = True)
        self.buildTargetingDictionary()
        if verbose:
            print("DONE")
            print("Populating target data into table...")
        self.populateTargetProperties()
        if verbose:
            print("Populating transcript data into table...", end = "", flush = True)
        self.populateTranscriptProperties()
        if verbose:
            print("DONE")
            print("Creating formatted table of targets...", end = "", flush = True)
        self.outputTable = self.createOutputTable()
        if verbose:
            print("DONE")
        
    def getTranscriptList(self):
        import json
        self.transcriptList = json.loads(self.tableHandle.get_entity(self.genome, self.geneID, "info")["transcripts"])
    
    def getAllGeneData(self):
        geneData = self.tableHandle.query_entities(self.genome, filter="PartitionKey eq '%s'" %self.geneID)
        geneDataList = []
        for entity in geneData:
            geneDataList.append(dict(entity))
        self.geneData = geneDataList
        
    def getTargetList(self):
        self.targetList = []
        for row in self.geneData:
            if row['RowKey'] == 'info':
                continue
            self.targetList.append(row["RowKey"])
    
    def buildTargetingDictionary(self):
        self.targetDictionary = {}
        transcriptTargeting = {}
        for transcript in self.transcriptList:
            transcriptTargeting[transcript] = "Not Targeted"  #we will fill this in later if it is
        for target in self.targetList:
            self.targetDictionary[target] = {"target":target.replace("_",""), "onTarget":None, "offTarget":None, "multiplePerfectGenicMatches":False, "multiplePerfectMatches":False, "tooManyMismatches":False, "transcriptTargeting":transcriptTargeting, "offTargets":None}
    
    def buildOffTargetList(self, siteData):
        import json
        offTargetList = []
        complete = False
        subgroup = 0
        while not complete:
            currentSubList = "offTargets" + str(subgroup)
            if not currentSubList in siteData:
                complete = True
                break
            offTargetList += json.loads(siteData[currentSubList])
            subgroup += 1
        return offTargetList
    
    def populateTargetProperties(self):
        #print(len(self.geneData))
        totalTargets = 0
        excessOffTargets = 0
        for targetEntity in self.geneData:
            totalTargets += 1
            target = dict(targetEntity)
            targetID = target["RowKey"]
            if targetID == "info":
                continue
            if target["tooManyMismatches"]:  #note that if a site is over the mismatch limit, we won't generate any data on it beyond it having too many mismatches.  We'll set the flag and move on.
                self.targetDictionary[targetID]["tooManyMismatches"] = True
                self.targetDictionary[targetID]["offTargets"] = "Too Many"
                excessOffTargets += 1
                continue
            self.targetDictionary[targetID]["onTarget"] = target["azimuth"]
            self.targetDictionary[targetID]["offTarget"] = target["aggregatedOffTarget"]
            self.targetDictionary[targetID]["multiplePerfectGenicMatches"] = target["multiplePerfectGenicMatches"]
            self.targetDictionary[targetID]["multiplePerfectMatches"] = target["multiplePerfectMatches"]
            if self.generateOffTargetLists:
                self.targetDictionary[targetID]["offTargets"] = self.buildOffTargetList(target)
            else:
                 self.targetDictionary[targetID]["offTargets"] = "Not listed"
        if self.verbose:
            print("Analyzed %s sites.  %s had too many off targets for analysis." %(totalTargets, excessOffTargets))
            
    def populateTranscriptProperties(self):
        import json
        for transcript in self.transcriptList:
            transcriptData = self.tableHandle.query_entities(self.genome, filter="PartitionKey eq '%s'" %transcript)
            for infoSet in transcriptData:
                if infoSet["RowKey"] == "info":
                    continue
                for key in infoSet:
                    if self.isTargetFormat(key):
                        self.targetDictionary[key]["transcriptTargeting"][transcript] = json.loads(infoSet[key])
                    
    def createOutputLine(self, line, delimiter = "\t"):
        import json
        outputLineList = []
        outputLineList.append(line["target"])
        outputLineList.append(line["onTarget"])
        outputLineList.append(line["offTarget"])
        outputLineList.append(line["multiplePerfectGenicMatches"])
        outputLineList.append(line["multiplePerfectMatches"])
        for transcript in self.transcriptList:
            outputLineList.append(self.targetingSummary(line["transcriptTargeting"][transcript]))
        if self.offTargetOutputLimit and not type(line["offTargets"]) == str:
            outputLineList.append(json.dumps(line["offTargets"][0:self.offTargetOutputLimit]))
        elif not type(line["offTargets"]) == str:
            outputLineList.append(json.dumps(line["offTargets"]))
        else:
            outputLineList.append(line["offTargets"])
        outputLineList = [str(element) for element in outputLineList]
        return delimiter.join(outputLineList)
    
    def createHeaderLine(self, delimiter = "\t"):
        headerList = ["Target Sequence", "On Target Score", "Off Target Score", "Multi Genic Matches", "Multiple Matches"]
        for transcript in self.transcriptList:
            headerList.append(transcript)
        headerList.append("Off Target List")
        return delimiter.join(headerList)
            
    def isTargetFormat(self, string):
        stringSplit = string.split("_")
        if not len(stringSplit) == 2:
            return False
        if not len(stringSplit[0]) == 20:
            return False
        if not len(stringSplit[1]) == 3:
            return False
        return True            
    
    def targetingSummary(self, targetingInfo, delimiter = "/"):
        #return str(targetingInfo)
        if type(targetingInfo) == str:
            return targetingInfo
        flagList = []
        for key in list(targetingInfo.keys()):
            if targetingInfo[key]:
                flagList.append(key)
        flagList = flagList.sort()
        if flagList:
            return delimiter.join(flagList)
        else:
            return "noFlag"
    
    def createOutputTable(self, delimiter = "\t"):
        outputTableLines = []
        outputTableLines.append(self.createHeaderLine())
        for target in self.targetList:
            outputTableLines.append(self.createOutputLine(self.targetDictionary[target], delimiter))
        return "\n".join(outputTableLines)
    
def getTableHandle():
    import azure.storage.table
    file = open("azureTable.apikey",'r')
    apikey = file.read().strip()
    tableHandle = azure.storage.table.TableService(account_name = settings.azure_account, account_key = apikey)
    return tableHandle

def main():
    args = CheckArgs()
    tableHandle = getTableHandle()
    siteTable = geneSiteTable(tableHandle, args.genome, args.gene, args.outputOffTargets, args.offTargetOutputLimit, args.verbose)
    outputFileName = "%s.targeting.txt" %args.gene
    if args.verbose:
        print("Writing data to %s" %outputFileName)
    outputFile = open(outputFileName, 'w')
    outputFile.write(siteTable.outputTable)
    outputFile.close()

if __name__ == '__main__':
    main()
    quit()