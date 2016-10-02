#!/usr/bin/env python3

class CheckArgs():  #class that checks arguments and ultimately returns a validated set of arguments to the main program
    
    def __init__(self):
        import argparse
        import os
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--repair", help = "Attempt to rerun failed jobs", action = 'store_true')
        parser.add_argument("-v", "--verbose", help = "Verbose mode", action = 'store_true')
        parser.add_argument("-s", "--rescan", help = "Rescan for job completion", action = 'store_true')
        parser.add_argument("-m", "--mock", help = "Mock run. Don't rerun anything, don't write anything to storage.", action = 'store_true')
        parser.add_argument("-d", "--directory", help = "Force the examination of a single directory specified as the argument")
        rawArgs = parser.parse_args()
        self.mock = rawArgs.mock
        self.verbose = rawArgs.verbose
        self.repair = rawArgs.repair
        self.rescan = rawArgs.rescan
        directory = rawArgs.directory
        if directory:
            if not os.path.isdir(directory):
                raise RuntimeError("Unable to find specified directory %s" %(directory))
        self.directory = directory
        if self.repair and self.mock:
            raise RuntimeError("A run cannot be both set to perform repairs and to be a mock run.")
                
def main():
    import datetime
    startTime = datetime.datetime.now()
    import os  #import the library for making os system calls
    # import pickle
    global args
    args =  CheckArgs()
    if not args.directory:
        dirList = os.listdir()
        jobDirs = []
        if args.verbose:
            print("Finding run data.")
        for item in dirList:
            if os.path.isdir(item) and item.startswith(".ENSG"):
                jobDirs.append(item)
        del dirList
    else:
        jobDirs = [args.directory]
    totalJobs = len(jobDirs)
    if args.verbose:
        print("Found data on %s runs" %(totalJobs))
    siteStatusTable = {}
    jobStatusTable = {}
    progress = 0
    successfulSites = 0
    successfulRunners = 0
    failedSites = 0
    totalRunners = 0
    genesWithNoTargets = 0
    for jobDir in jobDirs:
        progress += 1
        if args.verbose:
            print("Analyzing run %s of %s" %(progress, totalJobs), end = "\r")
        directory = jobDir + os.sep
        geneDirList = os.listdir(directory)
        for file in geneDirList:
            if not os.path.isfile(directory + os.sep + file):
                continue
            if file == "no.targets":
                genesWithNoTargets += 1
            elif ".runner." in file:
                nameSplit = file.split(".")
                runnerNumber = int(nameSplit[0])
                runnerStatus = nameSplit[-1]
                if runnerStatus == "ended":
                    mark = True
                    successfulRunners += 1
                else:
                    mark = False
                    totalRunners += 1
                if not jobDir in jobStatusTable:
                    jobStatusTable[jobDir] = {}
                if not runnerNumber in jobStatusTable[jobDir]:
                    jobStatusTable[jobDir][runnerNumber] = False
                jobStatusTable[jobDir][runnerNumber] = jobStatusTable[jobDir][runnerNumber] or mark
            elif file.endswith(".done") or file.endswith(".failed"):
                nameSplit = file.split(".")
                runnerNumber = int(nameSplit[0])
                siteNumber = int(nameSplit[1])
                siteStatus = nameSplit[-1]
                if siteStatus == "done":
                    mark = True
                    successfulSites += 1
                else:
                    mark = False
                    failedSites += 1
                if not jobDir in siteStatusTable:
                    siteStatusTable[jobDir] = {}
                if not runnerNumber in siteStatusTable[jobDir]:
                    siteStatusTable[jobDir][runnerNumber] = {}
                if not siteNumber in siteStatusTable[jobDir][runnerNumber]:
                    siteStatusTable[jobDir][runnerNumber][siteNumber] = False
                siteStatusTable[jobDir][runnerNumber][siteNumber] = siteStatusTable[jobDir][runnerNumber][siteNumber] or mark
    if args.verbose:
        print()  #blank line to save counter above
        failedRunners = totalRunners - successfulRunners
        runnerFailPercent = failedRunners/totalRunners * 100
        runnerSuccessPercent = successfulRunners/totalRunners * 100
        totalSites = successfulSites + failedSites
        siteFailPercent = failedSites/totalSites * 100
        siteSuccessPercent = successfulSites/totalSites * 100
        print("RUNNERS: %s total\t%s(%s%%) successful\t%s(%s%%) failed" %(totalRunners, successfulRunners, runnerSuccessPercent, failedRunners, runnerFailPercent))
        print("SITES:   %s total\t%s(%s%%) successful\t%s(%s%%) failed" %(totalSites, successfulSites, siteSuccessPercent, failedSites, siteFailPercent))
        print("%s genes had no usable targets in any transcript." %(genesWithNoTargets))
    # if not args.mock:
    #     pickleOut = open("lastHealer.pkl",'wb')
    #     pickle.dump(siteStatusTable, pickleOut)
    #     pickle.dump(jobStatusTable, pickleOut)
    #     pickleOut.close()
    reruns = []
    for jobDir in list(siteStatusTable.keys()):  
        for runner in list(jobStatusTable[jobDir].keys()):
            if not jobStatusTable[jobDir][runner]:
                print("Incomplete runner: %s job %s" %(jobDir[1:], runner))
                rerunTuple = (jobDir, runner)
                if not rerunTuple in reruns:
                    reruns.append(rerunTuple)
    for jobDir in list(siteStatusTable.keys()):
        for runner in list(siteStatusTable[jobDir].keys()):
            added = False
            for site in list(siteStatusTable[jobDir][runner].keys()):
                if not siteStatusTable[jobDir][runner][site]:
                    print("Failed site: %s job %s site %s" %(jobDir[1:], runner, site))
                    rerunTuple = (jobDir, runner, site)
                    if not added and not rerunTuple in reruns:
                        reruns.append(rerunTuple)
    for rerun in reruns:
        if len(rerun) == 2:
            command = "python3 arrayWrapper.py -d " + rerun[0] + " -j " + str(rerun[1])
        elif len(rerun) == 3:
            command = "python3 arrayWrapper.py -d " + rerun[0] + " -j " + str(rerun[1]) + " -s " + str(rerun[2])
        if args.verbose:
            print(command)
        if args.repair:                
            os.system(command)
    if args.verbose:
        print("Repair run completed in %s" %(datetime.datetime.now() - startTime))
                
main()
