#!/usr/bin/env python3

global pythonInterpreterAbsolutePath
pythonInterpreterAbsolutePath = "/u/local/apps/python/3.4.3/bin/python3"

class CheckArgs():  #class that checks arguments and ultimately returns a validated set of arguments to the main program
    
    def __init__(self):
        import argparse
        import os
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--chromosome", help = "Chromosome to run")
        parser.add_argument("-m", "--mock", help = "Mock run", action = 'store_true')
        parser.add_argument("-s", "--subset", help = "Run only a subset of genes from the chromosome.")
        rawArgs = parser.parse_args()
        if not rawArgs.chromosome:
            raise RuntimeError("No chromosome was given.")
        self.chromosome = rawArgs.chromosome
        self.mock = rawArgs.mock
        subset = rawArgs.subset
        if not subset:
            self.subset = False
        else:
            self.subset = True
            if ":" in subset:
                blockSize, blockNumber = subset.split(":")
                self.blockSize = int(blockSize)
                self.blockNumber = int(blockNumber)
                self.blocks = True
                self.firstGenes = False
            else:
                self.firstGenes = int(subset)
                self.blocks = False

def geneIsDone(ensg):
    import os
    import shutil
    workingDir = "." + ensg + os.sep
    if not os.path.isdir(workingDir):
        return False
    directoryListing = os.listdir(workingDir)
    for file in directoryListing:
        if file.endswith(".done") or file.endswith(".ended") or file == "no.targets":
            return True
    if not args.mock:
        shutil.rmtree(workingDir)
    else:
        print("Removing tree: %s" %(ensg))
    return False


                
def main():
    import datetime
    import time
    startTime = datetime.datetime.now()
    import os  #import the library for making os system calls
    if os.path.isfile("stop.chromosomeRunner.now"):
        raise RuntimeError("Stop signal file was found before run started:  stop.chromosomeRunner.now")
    import ensemblDataConversion
    global args
    args =  CheckArgs()
    converter = ensemblDataConversion.GenesFromChromosomeInterval()
    ensgList = converter.convert(args.chromosome ,biotypeFilter =  "protein_coding", value = "ENSG")
    if args.subset:
        if args.blocks:
            start = args.blockSize * (args.blockNumber - 1)
            end = (args.blockSize * args.blockNumber) - 1
            ensgList = ensgList[start:end]
        elif args.firstGenes:
            ensgList = ensgList[:args.firstGenes]
    progress = 0
    geneCount = len(ensgList)
    for ensg in ensgList:
        if os.path.isfile("stop.chromosomeRunner.now"):
            os.remove("stop.chromosomeRunner.now")
            quit("Stop signal file was found.")
        progress += 1
        print("Running gene %s of %s" %(progress, geneCount))
        if geneIsDone(ensg):
            print("%s has already been run." %(ensg))
            continue
        success = False
        failures = 0
        while not success:
            command = pythonInterpreterAbsolutePath + " ensemblGeneAnalyzer.py -g " + ensg
            if args.mock:
                command += " -m"
            print(command)
            submission = os.system(command)
            if submission == 0:
                success = True
            else:
                failures += 1
                time.sleep(90)
                if failures > 10:
                    raise RuntimeError("Unable to launch subprocess.")
    runTime = datetime.datetime.now() - startTime
    print("Completed submissions in %s" %(runTime))
    
main()
