#!/usr/bin/env python3

class CheckArgs():  #class that checks arguments and ultimately returns a validated set of arguments to the main program
    
    def __init__(self):
        import argparse
        import os
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--directory", help = "Directory with job data")
        parser.add_argument("-j", "--job", help = "Force this instance to use a job number without looking at env variables.", type = int)
        parser.add_argument("-s", "--subjob", help = "Force this instance to only run a specific subjob from the line")
        parser.add_argument("--noClockOut", help = "Do not clock out via this wrapper.", action = 'store_true')
        rawArgs = parser.parse_args()
        if rawArgs.directory:
            if os.path.isdir(rawArgs.directory):
                self.directory = rawArgs.directory
            else:
                raise RuntimeError("Temporary directory not found: " + rawArgs.directory)
        else:
            raise RunTimeError("No temporary directory specified.")
        if rawArgs.job:
            self.job = rawArgs.job
        else:
            self.job = False
        subjob = rawArgs.subjob
        if subjob and not self.job:
            raise RuntimeError("A job is needed if a subjob is specified.")
        if subjob:
            try:
                subjob = int(subjob)
            except ValueError:
                raise RuntimeError("Subjob must be specified as an integer.")
            self.subjob = subjob
        else:
            self.subjob = -1
        self.noClockOut = rawArgs.noClockOut
        
                
def main():
    import datetime
    startTime = datetime.datetime.now()
    import os  #import the library for making os system calls
    import pickle
    import random
    import time
    global args  #declare args as a global
    args = CheckArgs()  #get an object containing validated arguments
    try:
        nodeNumber = os.environ["HOSTNAME"].replace("n","")
        nodeNumber = int(nodeNumber)
    except ValueError:
        nodeNumber = False
    # if nodeNumber and nodeNumber in [2210, 2211, 2212, 2213, 2214, 2215, 2216, 2217, 2218, 2219, 2220]:  #This seems to be a bad group of nodes.
    #     import sys
    #     sys.exit(99)
    if not args.job:
        try:
            jobListNumber = int(os.environ["SGE_TASK_ID"])   #get the array job number from environmental variables
        except KeyError:  #if it cannot get that value
            raise RuntimeError("Unable to find a valid task ID in OS environment variables.")   #something is wrong so quit
    else:
        jobListNumber = args.job
    directory = args.directory  #get the tempdir from arguments
    if not directory.endswith(os.sep):  #if it does not end with a separator
        directory += os.sep  #add one
    jobListFile = open(directory + "jobs.pkl",'rb')
    jobLists = pickle.load(jobListFile)
    jobListFile.close()
    thisJobList = jobLists[jobListNumber]
    if type(thisJobList) == str:
        thisJobList = [thisJobList]
    # random.seed(jobListNumber)  #introducing some jitter here
    # delay = random.uniform(0,60)
    # time.sleep(delay)
    if args.subjob != -1:
        jobRange = [args.subjob]
    else:
        jobRange = range(0, len(thisJobList))
    if not args.noClockOut:
        startTouchFile = directory + str(jobListNumber) + ".runner.started"
        touchFile = open(startTouchFile, 'w')
        touchFile.close()
    for thisJobNumber in jobRange:
        if os.path.isfile(directory + str(jobListNumber) + "." + str(thisJobNumber) + ".done") or os.path.isfile(directory + str(jobListNumber) + "." + str(thisJobNumber) + ".already.done"):
            print("Job %s.%s has already been marked as done.  Skipping it." %(jobListNumber, thisJobNumber))
            continue
        print("Running job %s.%s" %(jobListNumber, thisJobNumber))
        jobStatus = os.system(thisJobList[thisJobNumber])  #run the bash file we just identified and set jobStatus to its exit status
        print("Job exit status: %s" %(jobStatus))
        if not args.noClockOut:
            if jobStatus == 0:  #if the job finished successfully
                touchFilePath = directory + str(jobListNumber) + "." + str(thisJobNumber) + ".done"  #define our clockout file
                touchFile = open(touchFilePath, 'w')  #create our clockout file
                touchFile.close()  #close it without writing anything
                failedFile = directory + str(jobListNumber) + "." + str(thisJobNumber) + ".failed"
                if os.path.isfile(failedFile):
                    os.remove(failedFile)
            elif jobStatus == 10752 or jobStatus == 42:  #I have no idea why I tell it to exit 42 and it exits 10752, but I can't be arsed to fix it right now.
                touchFilePath = directory + str(jobListNumber) + "." + str(thisJobNumber) + ".already.done"  #define our clockout file
                touchFile = open(touchFilePath, 'w')  #create our clockout file
                touchFile.close()  #close it without writing anything
                failedFile = directory + str(jobListNumber) + "." + str(thisJobNumber) + ".failed"
                if os.path.isfile(failedFile):
                    os.remove(failedFile)
            else:
                try:
                    nodeNumber = os.environ["HOSTNAME"]
                except ValueError:
                    nodeNumber = "Unable to get node number"
                touchFilePath = directory + str(jobListNumber) + "." + str(thisJobNumber) + ".failed"  #define our clockout file
                touchFile = open(touchFilePath, 'w')  #create our clockout file
                touchFile.write("Failed on node " + nodeNumber + "\n")
                touchFile.close()  #close it without writing anything
        endTouchFile = directory + str(jobListNumber) + ".runner.ended"
        touchFile = open(endTouchFile, 'w')
        touchFile.close()
    while not (datetime.datetime.now() - startTime).seconds > 120:  #throttle this!
        time.sleep(1)
    
main()
