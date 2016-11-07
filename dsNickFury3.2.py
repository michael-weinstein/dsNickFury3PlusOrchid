#!/usr/bin/env python3
'''
Software License
Commercial reservation
This License governs use of the accompanying Software, and your use of the Software constitutes acceptance of this license.

You may use this Software for any non-commercial purpose, subject to the restrictions in this license. Some purposes which can be non-commercial are teaching, academic research, and personal experimentation. 

You may not use or distribute this Software or any derivative works in any form for any commercial purpose. Examples of commercial purposes would be running business operations, licensing, leasing, or selling the Software, or distributing the Software for use with commercial products. 

You may modify this Software and distribute the modified Software for non-commercial purposes; however, you may not grant rights to the Software or derivative works that are broader than those provided by this License. For example, you may not distribute modifications of the Software under terms that would permit commercial use, or under terms that purport to require the Software or derivative works to be sublicensed to others.

You agree: 
1.	Not remove any copyright or other notices from the Software.
2.	That if you distribute the Software in source or object form, you will include a verbatim copy of this license.
3.	That if you distribute derivative works of the Software in source code form you do so only under a license that includes all of the provisions of this License, and if you distribute derivative works of the Software solely in object form you do so only under a license that complies with this License.
4.	That if you have modified the Software or created derivative works, and distribute such modifications or derivative works, you will cause the modified files to carry prominent notices so that recipients know that they are not receiving the original Software. Such notices must state: (i) that you have changed the Software; and (ii) the date of any changes.
5.	THAT THIS PRODUCT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS PRODUCT, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  YOU MUST PASS THIS LIMITATION OF LIABILITY ON WHENEVER YOU DISTRIBUTE THE SOFTWARE OR DERIVATIVE WORKS.

6.	That if you sue anyone over patents that you think may apply to the Software or anyone's use of the Software, your license to the Software ends automatically.
7.	That your rights under the License end automatically if you breach it in any way.
8.	UCLA and the Regents of the University of California reserves all rights not expressly granted to you in this license.

9.	Nothing in this Agreement grants by implication, estoppel, or otherwise any rights to any intellectual property owned by the Regents of the University of California, except as explicitly set forth in this license.
10.	You will hold the Regents of the harmless for all claims, suits, losses, liabilities, damages, costs, fees, and expenses resulting from their respective activities arising from this license.  
11.	You will not use any name, trade name, trademark, name of any campus, or other designation of the Regents of the University of California in advertising, publicity, or other promotional activity, except as permitted herein.
'''

#This is the path for the python interpreter.  You must set it before this will run.  If you are unsure what this is, try the command "which python3" or "which pypy3" and try pasting the path returned between the quotes on the next line.
global pythonInterpreterAbsolutePath; global pythonCompilerAbsolutePath
#pythonInterpreterAbsolutePath = "/Library/Frameworks/Python.framework/Versions/3.4/bin/python3"
pythonInterpreterAbsolutePath = "/u/local/apps/python/3.4.3/bin/python3"  #Set the absolute path for your python interpreter here between the quotes.  Depending on your system configuration, you may also be able to use a shortcut, such as python3, but that has a greater chance of errors
pythonCompilerAbsolutePath = ""
    
#USEFUL DEFAULT SETTINGS HERE
global selectionModeTargetLimitPerJob
selectionModeTargetLimitPerJob = 0 #This prevents a user from submitting a job with too many target sites that might overload or degrade performance on the system.  Clobber mode can override this.  Change this value according to your system's capabilities.  Set to 0 or negative value for no limit.

global clusterDefaultSelectionModeParallelJobLimit; global standAloneDefaultSelectionModeParallelJobLimit; global clusterMaxArrayJobs;
clusterDefaultSelectionModeParallelJobLimit = 230  #Limit on how many simultaneous parallel jobs can be going at once on a cluster (set this based on the limit for how many queued items you can have)
standAloneDefaultSelectionModeParallelJobLimit = 1  #Limit on how many simultaneous parallel jobs can be going if run on a single system.  Change according to your machine.
clusterMaxArrayJobs = 1000  #for an array job, this is the maximum number of crispr sites that can be in a single sequence if there is no selectionModeTargetLimitPerJob set.

global positionByteLength
positionByteLength = 4  #setting this to a regular, unsigned integer for now (4 bytes).  Hopefully I don't find anything with a larger genome or I have to use Q

global currentVersion
currentVersion = "3.2"

global versionName
versionName = "The Orchid edition. Perfecting the replacement base fragment. I totally asked for this."

global yearWritten
yearWritten = "2016"

def yesAnswer(question):  #asks the question passed in and returns True if the answer is yes, False if the answer is no, and keeps the user in a loop until one of those is given.  Also useful for walking students through basic logical python functions
    answer = False  #initializes the answer variable to false.  Not absolutely necessary, since it should be undefined at this point and test to false, but explicit is always better than implicit
    while not answer:  #enters the loop and stays in it until answer is equal to True
        print (question + ' (Y/N)')  #Asks the question contained in the argument passed into this subroutine
        answer = input('>>') #sets answer equal to some value input by the user
        if str(answer) == 'y' or str(answer) == 'Y':  #checks if the answer is a valid yes answer
            return True  #sends back a value of True because of the yes answer
        elif str(answer) == 'n' or str(answer) == 'N': #checks to see if the answer is a valid form of no
            return False  #sends back a value of False because it was not a yes answer
        else: #if the answer is not a value indicating a yes or no
            print ('Invalid response.')
            answer = False #set ansewr to false so the loop will continue until a satisfactory answer is given

def reportUsage(details):  #this will report usage back to us.  This is required by the people who maintain the Azimuth server.  This will not send back any details of your job except if azimuth was used.
    import urllib.request
    url = "http://pathways.mcdb.ucla.edu/cgi-bin/MW_counter/counter.cgi?counter=" + details
    try:
        req = urllib.request.urlopen(url)
    except:
        pass        

def printStartUp():
    print("       _            _            _              _           _             _              _      _                  _    _        _     _      ")
    print("      /\\ \\         / /\\         /\\ \\     _     /\\ \\       /\\ \\           /\\_\\           /\\ \\   /\\_\\               /\\ \\ /\\ \\     /\\_\\ /\\ \\     ")
    print("     /  \\ \\____   / /  \\       /  \\ \\   /\\_\\   \\ \\ \\     /  \\ \\         / / /  _       /  \\ \\ / / /         _    /  \\ \\\\ \\ \\   / / //  \\ \\    ")
    print("    / /\\ \\_____\\ / / /\\ \\__   / /\\ \\ \\_/ / /   /\\ \\_\\   / /\\ \\ \\       / / /  /\\_\\    / /\\ \\ \\\\ \\ \\__      /\\_\\ / /\\ \\ \\\\ \\ \\_/ / // /\\ \\ \\   ")
    print("   / / /\\/___  // / /\\ \\___\\ / / /\\ \\___/ /   / /\\/_/  / / /\\ \\ \\     / / /__/ / /   / / /\\ \\_\\\\ \\___\\    / / // / /\\ \\_\\\\ \\___/ / \\/_/\\ \\ \\  ")
    print("  / / /   / / / \\ \\ \\ \\/___// / /  \\/____/   / / /    / / /  \\ \\_\\   / /\\_____/ /   / /_/_ \\/_/ \\__  /   / / // / /_/ / / \\ \\ \\_/      / / /  ")
    print(" / / /   / / /   \\ \\ \\     / / /    / / /   / / /    / / /    \\/_/  / /\\_______/   / /____/\\    / / /   / / // / /__\\/ /   \\ \\ \\      / / /   ")
    print("/ / /   / / /_    \\ \\ \\   / / /    / / /   / / /    / / /          / / /\\ \\ \\     / /\\____\\/   / / /   / / // / /_____/     \\ \\ \\    / / /  _ ")
    print("\\ \\ \\__/ / //_/\\__/ / /  / / /    / / /___/ / /__  / / /________  / / /  \\ \\ \\   / / /        / / /___/ / // / /\\ \\ \\        \\ \\ \\  / / /_/\\_\\")
    print(" \\ \\___\\/ / \\ \\/___/ /  / / /    / / //\\__\\/_/___\\/ / /_________\\/ / /    \\ \\ \\ / / /        / / /____\\/ // / /  \\ \\ \\        \\ \\_\\/ /_____/ /")
    print("  \\/_____/   \\_____\\/   \\/_/     \\/_/ \\/_________/\\/____________/\\/_/      \\_\\_\\\\/_/         \\/_________/ \\/_/    \\_\\/         \\/_/\\________/ ")
    print("                   _ _ _ ____ ___ ____ _  _    _   _ ____ _  _ ____    ___ ____ ____ ____ ____ ___ ____")
    print("                   | | | |__|  |  |    |__|     \_/  |  | |  | |__/     |  |__| |__/ | __ |___  |  [__ ")
    print("                   |_|_| |  |  |  |___ |  |      |   |__| |__| |  \     |  |  | |  \ |__] |___  |  ___]")
    print("                                        _ _ _ _ ___ _  _    ___  ____ ___ _  _    ____ _   _ ____ ____    /")
    print("                                        | | | |  |  |__|    |__] |  |  |  |__|    |___  \_/  |___ [__    /")
    print("                                        |_|_| |  |  |  |    |__] |__|  |  |  |    |___   |   |___ ___]  .")
    print("Version " + currentVersion + " (" + versionName + ")")
    print("By Michael M. Weinstein, Copyright " + yearWritten)
    print("Dan Cohn Laboratory and Collaboratory, University of California, Los Angeles")
        
def printManual():
    import urllib.request
    try:
        import textwrap
        wrap = True
    except:
        wrap = False
    try:
        import random
        egg = random.randint(1,100)
        if egg == 42:
            print(urllib.request.urlopen("https://raw.githubusercontent.com/michael-weinstein/dsNickFury2/master/ajd/AJD.txt").read().decode('utf-8'))  #this works better if your terminal has a dark background
    except:
        pass
    manualURL = 'https://raw.githubusercontent.com/michael-weinstein/dsNickFury2/master/readme.md'
    try:
        rawManual = urllib.request.urlopen(manualURL)
        text = rawManual.read().decode('utf-8')
        print("Manual from " + manualURL)
        if not wrap:
            print(text)
        else:
            text = text.split("\n")
            for paragraph in text:
                print("\n".join(textwrap.wrap(paragraph, width = 120, break_long_words = False)))
    except:
        print("Unable to download and display manual.  Please view it in your browser at:\n\n" + manualURL + "\n")
    try:
        import random
        egg = random.randint(1,100)
        if egg == 42:
            print(urllib.request.urlopen("https://raw.githubusercontent.com/michael-weinstein/dsNickFury2/master/ajd/AJD.txt").read().decode('utf-8'))  #this works better if your terminal has a dark background
    except:
        pass
    quit()
    
def checkPythonInterpreterAbsolutePath(absPath):
    import os
    import subprocess
    if not absPath:
        printManual()
        raise RuntimeError("ABORTED: You must set the absolute path for your python interpreter at the beginning of this script.")
    if not os.path.isfile(absPath):  #if the absolute path is not actually a file, check if we have an alias we can expand upon
        import subprocess
        try:
            absPath = subprocess.check_output(['which',absPath]).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            raise RuntimeError("ABORTED: Python interpreter not found at " + absPath + " and it does not appear to be a valid alias.  Please correct the location.")
    return absPath
pythonInterpreterAbsolutePath = checkPythonInterpreterAbsolutePath(pythonInterpreterAbsolutePath)

#===================================Command line Argument Checking===========================================

class Args(object):
    
    def __init__(self):
        import os
        import argparse #loads the required library for reading the commandline
        parser = argparse.ArgumentParser()
        parser.add_argument ("--manual", help = "Print out the user manual and sample command lines.", action = 'store_true')
        parser.add_argument ("-m", "--mode", help = "Specify how the program is to run (what the desired task is)")
        parser.add_argument ("-g", "--genome", help = "Specify the genome for searching or indexing.")
        parser.add_argument ("-d", "--inputDirectory", help = "Specify genome index directory for a worker job.")
        parser.add_argument ("-f", "--inputfile", help = "Specify a single input genome for indexing")
        parser.add_argument ("--tempDir", help = "Temporary directory name for parallel jobs")
        parser.add_argument ("--parallelJobs", help = "Max number of parallel jobs at once. (Or per search if running in selection mode)")
        parser.add_argument ("-9", "--clobber", help = "Do not ask before overwriting files.", action = 'store_true')
        parser.add_argument ("-w", "--workerID", help = "Worker process ID.  Users should not be setting this value.")
        parser.add_argument ("-s", "--sequence", help = "Sequence of interest.  Format: NNNNNNGUIDERNANNNNNN_PAM")
        parser.add_argument ("-t", "--mismatchTolerance", help = "Maximim number of mismatches permitted for a positive result.")
        parser.add_argument ("--verbose", help = "Run in verbose mode", action = 'store_true')
        parser.add_argument ("--mock" , help = "Print exec commands instead of running them.", action = 'store_true')
        parser.add_argument ("--ordered", help = "Do not break up chromosomes for parallel analysis.", action = 'store_true')
        parser.add_argument ("-c", "--chunkSize", help = "Specify the chunk size for parallel genome annotation.")
        parser.add_argument ("--chromosome", help = "Used to specify the chromosome/contig ID.  This should be passed by the machine and not the user.")
        parser.add_argument ("--start", help = "Used to specify the starting byte of the FASTA for indexing.  This should be passed by the machine and not the user.")
        parser.add_argument ("--length", help = "Used to specify the bytelength of the chunk to be indexed by the program.  This should be passed by the machine and not the user.")
        parser.add_argument ("--forceJobIndex", help = "Force the indexing supervisor instance to take a specific job index.  Mostly useful for debugging functions.")
        parser.add_argument ("--outputDirectory", help = "Directory for outputting search results to a hypervisor.  This should generally be passed by the machine and not the user.")
        parser.add_argument ("--noCleanup", help = "Leave behind any temporary files for future inspection.", action = 'store_true')
        parser.add_argument ("--forceGenome", help = "Force the search supervisor to use this genome directory.  Generally this should be passed by the machine and not the user.")
        parser.add_argument ("--species", help = "Tell the indexer which species the genome is from.")
        parser.add_argument ("--targetSequence", help = "Enter a long sequence here to search for and analyze potential targets.")
        parser.add_argument ("--targetFasta", help = "Enter a file name for a FASTA file to search for and analyze potential target sites.")
        parser.add_argument ("--targetList", help = "Enter a list of potential sites to analyze for off-target risk.")
        parser.add_argument ("--noForcedBases", help = "Prevent forcing bases 1 and/or 3 in the guide RNA to match those submitted for Azimuth analysis")
        parser.add_argument ("--skipAzimuth", help = "Do not attempt Azimuth analysis.", action = 'store_true')
        parser.add_argument ("--parallelJobLimit", help = "Set a limit on the number of parallel jobs allowed at once in the queue for highly parallelized tasks (this MUST be set below your scheduler's limit for queued jobs for a single user, and should be set 5-10 percent below it).")
        parser.add_argument ("--genomeDirectory", help = "Specify an alternate directory to search for suitable indexed genomes.")
        parser.add_argument ("--annotationExpansion", help = "Specify how far from the target site to search for an annotated gene/genomic feature (default is 1KB).")
        parser.add_argument ("--azimuthSequence", help = "Specify a sequence for Azimuth analysis.")
        parser.add_argument ("--outputToFile", help = "In selection mode, dump the output to the filename passed as an argument here.")
        parser.add_argument ("--scratchFolder", help = "Specify a directory to use for writing temporary (job) folders.")
        parser.add_argument ("--cluster", help = "Specify that this is running on a cluster system.", action = "store_true")
        parser.add_argument ("--standAlone", "--standalone", help = "Specify that this is running on a single system or server.", action = "store_true")
        parser.add_argument ("--mixed", help = "In selection mode, run each site on a separate node, but parallelize searching within a single node.", action = "store_true")
        parser.add_argument ("--directToCompiler", help = "If you already have run the index, but compiling did not complete successfully, try this to recompile.", action = "store_true")
        parser.add_argument ("--recreateTree", help = "Recreate the tree pickle for an existing genome index.", action = "store_true")
        parser.add_argument ("--bins", help = "Pass a comma-separated list of bins for this compiler instance to work on.")
        parser.add_argument ("--treeLevel1", help = "Pass an integer value for the first level of the tree")
        parser.add_argument ("--treeLevel2", help = "Pass an integer value for the second level of the tree")
        parser.add_argument ("-r", "--preferredPAM", help = "Use this to pass a preferred PAM site for a selection job" )
        parser.add_argument ("-p", "--canonicalPAM", help = "Pass a canonical PAM sequence for a sysem indexed for multiple PAMs.  A mode may be specified after a comma (Mode 1: Any non-canonical PAM will be considered a single mismatch.  Mode 2: Any individual base not valid for the canonical PAM will add a mismatch)")
        parser.add_argument ("--arrayJob", help = "This will be used by a selection hypervisor to initiate array jobs", action = "store_true")
        parser.add_argument ("-a", "--useArray", help = "Use array jobs on an SGE cluster in mixed mode (recommended if possible, this will turn on mixed mode automatically)", action = "store_true")
        parser.add_argument ("--delayIO", help = "Delay search worker IO calls by a random time to avoid IO traffic jams.", action = "store_true")
        parser.add_argument ("--totalArrayJobs", help = "Total number of array jobs for this run, used by the array job launcher.")
        parser.add_argument ("--spoofTaskID", help = "Pass an integer to force a task ID (rather than pulling one from environment variables).  Used for debugging and testing the array job runner.")
        parser.add_argument ("--quickExtend", help = "Quick extension mode", action = "store_true")
        parser.add_argument ("--guideExtension", help = "Set the length of the extension before the guide to store or use")
        parser.add_argument ("--pamExtension", help = "Set the length of the extension after the PAM to store or use")
        parser.add_argument ("--beforeAltStart", help = "Flag this site as being before a potential alternative start site", action = "store_true")
        parser.add_argument ("--lastExon", help = "Flag this site as being in the last exon of a gene", action = "store_true")
        parser.add_argument ("--azureTableOut", help = "Output results to an azure table.  Argument should be formatted as account,tableName,partitionKey,rowKey")
        parser.add_argument ("--endClip", help = "Ignore the last n bases (distal to PAM) when matching", type = int, default = 0)
        parser.add_argument ("--matchSiteCutoff", help = "Stop searching after finding this number of potential mismatches (set to 0 for no limit)", type = int, default = 10000)
        parser.add_argument ("--forcePamList", help = "Force the use of a specific list of (potentially degenerate) PAM sites instead of determining it from the passed sequence")
        parser.add_argument ("--enumeratedContig", help = "For passing the enumerated contig number and encoding scheme")
        parser.add_argument ("--cacheSize", help = "Size of sites that can be cached before analysis in search or dumping to drive in index", type = int, default = 25000000)
        parser.add_argument ("--noElevation", help = "Skip elevation analysis during a site search", action = "store_true")
        args = parser.parse_args()  #puts the arguments into the args object
       
        if args.arrayJob:  #quick trap for array job runners... it will be run during the checkargs phase and return to the main function where it will report itself done and quit
            if not args.tempDir:
                raise RuntimeError("Unable to run array job without being passed the name of the temporary directory under --tempDir.")
            try:
                totalArrayJobs = int(args.totalArrayJobs)
            except ValueError:
                raise RuntimeError("Argument passed as --totalArrayJobs must be an integer. " + str(args.totalArrayJobs) + " was passed instead.")
            spoofTaskID = False
            if args.spoofTaskID:
                try:
                    spoofTaskID = int(args.spoofTaskID)
                except ValueError:
                    raise RuntimeError("Spoofed task ID must be passed as an integer.  We got: " + str(args.spoofTaskID))
            arrayJobTrap(args.tempDir, totalArrayJobs, spoofTaskID)
            self.mode = "ARRAY RUNNER"

        else:
            if args.quickExtend:  #adding a catch for quick return mode
                args.mode = "search"
                args.standAlone = True
                self.quickExtend = True
            else:
                self.quickExtend = False
            if (args.standAlone and args.cluster) or (args.mixed and args.cluster) or (args.mixed and args.standAlone): #You really can't be both.
                raise RuntimeError("Aborted: You must specify --cluster OR --standAlone OR --mixed.  You can't be more than one.")
            if not (args.standAlone or args.cluster or args.mixed or args.manual) and args.mode in ['index', 'selection']:
                raise RuntimeError("ABORTED: You must specify if this will be running on a stand-alone system or a cluster. (--standAlone or --cluster)")
            else:
                if args.standAlone:
                    self.standAlone = True
                    self.cluster = False
                    self.mixed = False
                elif args.cluster:
                    self.cluster = True
                    self.standAlone = False
                    self.mixed = False
                elif args.mixed:
                    self.cluster = False
                    self.standAlone = False
                    self.mixed = True
                    if args.mode and args.mode.upper() == "INDEX":
                        raise RuntimeError("Mixed system cannot be specified for an index run.")
            if not args.mode and not args.manual:  #series of case statements for mode to determine which set of inputs to validate.  If no mode was set, it will see if the user is asking for the manual.  
                raise RuntimeError("ABORTED: No run mode was set on the commandline.")
            self.mode = args.mode
            if not args.genomeDirectory:
                self.genomeListDirectory = "genomes/"
            else:
                self.genomeListDirectory = args.genomeDirectory
                if not self.genomeListDirectory[-1] == "/":
                    self.genomeListDirectory += "/"
                if not os.path.isdir(self.genomeListDirectory) and not self.mode == 'index':
                    raise RuntimeError("ABORTED: User-specified genome: " + self.genomeListDirectory + " not found.")
            if args.mode == 'worker':
                self.setWorkerArgs(args)
            elif args.mode == 'search':
                self.setSearchArgs(args)
            elif args.mode == 'index':
                self.setIndexArgs(args)
            elif args.mode == 'FASTAWorker':
                self.setFASTAWorkerArgs(args)
            elif args.mode == 'selection':
                self.setSelectionArgs(args)
            elif args.mode == 'compiler':
                self.setCompilerArgs(args)
            elif args.manual:
                printManual()
                quit()
            else:
                raise RuntimeError('ABORTED: Invalid/no mode set on commandline.  Please select a mode or run with --manual set for assistance.')
            
    def setSelectionArgs(self, args):  #validating and setting arguments for selection of targets from a user-provided sequence
        import os
        import degenerateBaseHandle
        self.sequence = args.sequence
        if not self.sequence:
            raise RuntimeError("ABORTED: You must specify a generic sequence to describe your system (see manual, argument --manual) for more information.")
        if "_" in args.sequence:
            guide, pam = args.sequence.split("_")
            try:
                guide = int(guide)
            except ValueError:
                pass
            else:
                args.sequence = "N"*guide + "_" + pam
            self.sequence = args.sequence.upper()
        else:
            raise RuntimeError("ABORTED: Invalid sequence passed. Please include an underscore between the guide and PAM sequences.")
        if not len(self.sequence) > 15 and not args.clobber:
            raise RuntimeError("ABORTED: This guide+pam combination appears too short, and will likely cause memory and other errors.  Rerun in clobber mode (argument -9) to proceed anyway.")
        self.targetSequence = args.targetSequence
        self.targetFasta = args.targetFasta
        if self.targetFasta and not os.path.isfile(self.targetFasta):
            raise RuntimeError("ABORTED: " + self.targetFasta + " is not a valid file.")
        self.targetList = args.targetList
        if self.targetList and not os.path.isfile(self.targetList):
            raise RuntimeError("ABORTED: " + self.targetList + " is not a valid file.")
        if not args.genome:
            raise RuntimeError("ABORTED: You must set a genome.  See manual (run with --manual) for details.")
        self.genome = args.genome.upper()
        self.verbose = args.verbose
        self.mock = args.mock
        if args.parallelJobs:
            try:
                self.parallelJobs = int(args.parallelJobs)
            except ValueError:
                raise RuntimeError("ABORTED: Parallel jobs argument must be an integer")
        else:
            self.parallelJobs = 5
        if not args.mismatchTolerance:
            self.mismatchTolerance = 3
        else:
            try:
                self.mismatchTolerance = int(args.mismatchTolerance)
            except ValueError:
                raise RuntimeError("ABORTED: Mismatch tolerance must be an integer.  Please check your command line options and try again.")
        if args.noForcedBases:
            if args.noForcedBases == "1":
                self.noForcedBases = False
                self.noForced1 = True
                self.noForced3 = False
            if args.noForcedBases == "3":
                self.noForcedBases = False
                self.noForced1 = False
                self.noForced3 = True
            else: #if they put in any other argument here, we block forcing either base (this could include 1,3 or all or anything else)
                self.noForcedBases = True
                self.noForced1 = True
                self.noForced3 = True
        else:  #if the argument was left blank or not passed at all, we allow base forcing
            self.noForcedBases = False
            self.noForced1 = False
            self.noForced3 = False
            self.skipAzimuth = args.skipAzimuth
        self.noCleanup = args.noCleanup
        if not args.parallelJobLimit:
            if self.cluster or self.mixed:
                self.maxParallelJobs = clusterDefaultSelectionModeParallelJobLimit  #set this value at the top of the script for your configuration of choice
            if self.standAlone:
                self.maxParallelJobs = standAloneDefaultSelectionModeParallelJobLimit
        else:
            try:
                self.maxParallelJobs = int(args.parallelJobLimit)
            except ValueError:
                raise RuntimeError("ABORTED: Parallel job limit must be an integer.")
        if self.maxParallelJobs < self.parallelJobs:
            self.maxParallelJobs = self.parallelJobs
        self.outputToFile = args.outputToFile
        if self.outputToFile and os.path.isfile(self.outputToFile) and not args.clobber:
            raise RuntimeError("ABORTED: Output file " + self.outputToFile + " already exists.  Run in clobber mode to overwrite.")
        self.clobber = args.clobber
        self.scratchFolder = args.scratchFolder
        if not self.scratchFolder:
            self.scratchFolder = "" #making sure this is cast to a string and not a NoneType (although that will probably add to a string with no trouble)
        else:
            if not self.scratchFolder[-1] == "/":
                self.scratchFolder = self.scratchFolder + "/"  #make sure that the directory name is passed ending with a slash so we can prepend it directly to our tempDir name
            if not os.path.isdir(self.scratchFolder):
                try:
                    os.mkdir(self.scratchFolder)
                except OSError:
                    if not os.path.isdir(self.scratchFolder):  #This could happen because of a data race type condition, if one process creates the directory after this one checks for it, but before it creates it.  This will catch that problem.
                        raise RuntimeError("ABORTED: Unable to create scratch folder.  Check if directory containing this folder already exists.")
        self.preferredPAM = False
        self.preferredPAMWeight = False
        if args.preferredPAM:
            if "," in args.preferredPAM:
                if not args.preferredPAM.count(",") == 1:
                    raise RuntimeError("PreferredPAM argument can be passed with only one comma-separated value for SITE,PREFERENCEVALUE.  Passed value was " + args.preferredPAM)
                self.preferredPAM, self.preferredPAMWeight = args.preferredPAM.split(",")
                self.preferredPAM = self.preferredPAM.upper()
                try:
                    self.preferredPAMWeight = int(self.preferredPAMWeight)
                except ValueError:
                    try:
                        self.preferredPAMWeight = float(self.preferredPAMWeight)
                    except:
                        raise RuntimeError("PreferredPAM argument must be a number.  Program was passed " + self.preferredPAMWeight + " in preferredPAM argument " + args.preferredPAM)
            else:
                self.preferredPAM = args.preferredPAM.upper()
                self.preferredPAMWeight = False
            systemPAM = self.sequence.split("_")[1]
            systemPAMList = degenerateBaseHandle.NondegenerateBases(systemPAM).permutations()
            self.preferredPAMList = degenerateBaseHandle.NondegenerateBases(self.preferredPAM).permutations()
            for preferredSite in self.preferredPAMList:
                if not preferredSite.upper() in systemPAMList:
                    raise RuntimeError("ABORTED: Your preferred PAM site of " + self.preferredPAM + " is not a subset for the system PAMs of " + systemPAM + ".")
        self.useArray = False
        if args.useArray:
            if not self.mixed:
                if self.standAlone:
                    raise RuntimeError("Array mode is invalid in stand alone mode.  Please run in mixed mode and try again.")
                self.mixed = True
                self.cluster = False
                print("Array use must be done in mixed mode to avoid overloading the job scheduler.")
                if not yesAnswer("Change to mixed mode now?"):
                    quit("Ok, exiting.")
            self.useArray = True
        if args.guideExtension:
            try:
                self.guideExtension = int(args.guideExtension)
            except ValueError:
                raise RuntimeError("Error: Guide extension value must be an integer.")
        else:
            self.guideExtension = 4
        if args.pamExtension:
            try:
                self.pamExtension = int(args.pamExtension)
            except ValueError:
                raise RuntimeError("Error: PAM extension value must be an integer")
        else:
            self.pamExtension = 3
    
    def setWorkerArgs(self, args):  #Validating arguments for a search worker.  This should not require too much validation, as users should not be launching worker processes themselves
        self.mode = "worker"
        self.workerID = args.workerID
        self.tempDir = args.tempDir
        self.sequence = args.sequence
        self.mismatchTolerance = int(args.mismatchTolerance)
        self.inputDirectory = args.inputDirectory
        self.verbose = args.verbose
        self.skipAzimuth = True
        self.delayIO = False
        if args.delayIO:
            self.delayIO = True
        if args.guideExtension:
            try:
                self.guideExtension = int(args.guideExtension)
            except ValueError:
                raise RuntimeError("Error: Guide extension value must be an integer.")
        else:
            self.guideExtension = 4
        if args.pamExtension:
            try:
                self.pamExtension = int(args.pamExtension)
            except ValueError:
                raise RuntimeError("Error: PAM extension value must be an integer")
        else:
            self.pamExtension = 3
           
    def setSearchArgs(self, args):  #Validating arguments for launching a search supervisor.  This will require good validations, as users are likely to be launching this on their own.
        import os
        import degenerateBaseHandle
        self.mode = "search"
        self.matchSiteCutoff = args.matchSiteCutoff
        self.endClip = args.endClip
        self.sequence = args.sequence
        if not self.sequence:
            raise RuntimeError("ABORTED: You must specify a sequence to search for.  Remember to place an underscore between the guide and PAM sequences.")
        if not "_" in self.sequence:
            raise RuntimeError("ABORTED: You must include an underscore '_' in your sequence between the guide RNA portion and the PAM sequence.")
        if not len(self.sequence) > 15 and not args.clobber:
            raise RuntimeError("ABORTED: This guide+pam combination appears too short, and will likely cause memory and other errors.  Rerun in clobber mode (argument -9) to proceed anyway.")
        self.sequence = self.sequence.upper()
        if not args.mismatchTolerance:
            if args.quickExtend:
                self.mismatchTolerance = 0
            else:
                self.mismatchTolerance = 3
        else:
            try:
                self.mismatchTolerance = int(args.mismatchTolerance)
            except ValueError:
                raise RuntimeError("ABORTED: Mismatch tolerance must be an integer.  Please check your command line options and try again.")
        self.tempDir = args.tempDir
        self.workerID = args.workerID
        self.inputDirectory = args.inputDirectory
        self.verbose = args.verbose
        self.mock = args.mock
        if not args.forceGenome:
            self.genome = args.genome.upper()  #if a genome is forced by a hypervisor function, this will prevent an error from trying to uppercase a NoneType variable.
        if args.parallelJobs:
            try:
                self.parallelJobs = int(args.parallelJobs)
            except ValueError:
                raise RuntimeError("ABORTED: Parallel jobs argument must be an integer")
        elif args.quickExtend:
            self.parallelJobs = 1
        else:
            self.parallelJobs = 12
        self.outputDirectory = args.outputDirectory
        self.noCleanup = args.noCleanup
        self.forceGenome = args.forceGenome
        self.skipAzimuth = True
        self.annotationExpansion = args.annotationExpansion
        if not self.annotationExpansion:
            self.annotationExpansion = 1000
        else:
            try:
                self.annotationExpansion = int(self.annotationExpansion)
            except ValueError:
                raise RuntimeError("ABORTED: Annotation expansion range must be an integer value.")
        self.azimuthSequence = args.azimuthSequence
        if not self.azimuthSequence or self.azimuthSequence == "False":
            self.azimuthSequence = False
        else:
            self.azimuthSequence = self.azimuthSequence.upper()
        self.scratchFolder = args.scratchFolder
        if not self.scratchFolder:
            self.scratchFolder = "" #making sure this is cast to a string and not a NoneType (although that will probably add to a string with no trouble)
        else:
            if not self.scratchFolder[-1] == "/":
                self.scratchFolder = self.scratchFolder + "/"  #make sure that the directory name is passed ending with a slash so we can prepend it directly to our tempDir name
            if not os.path.isdir(self.scratchFolder):
                try:
                    os.mkdir(self.scratchFolder)
                except OSError:
                    raise RuntimeError("ABORTED: Unable to create scratch folder.  Check if directory containing this folder already exists.")
        self.clobber = False
        if args.clobber:
            self.clobber = True
        self.preferredPAM = False
        self.preferredPAMWeight = False
        if args.preferredPAM:
            if "," in args.preferredPAM:
                if not args.preferredPAM.count(",") == 1:
                    raise RuntimeError("PreferredPAM argument can be passed with only one comma-separated value for SITE,PREFERENCEVALUE.  Passed value was " + args.preferredPAM)
                self.preferredPAM, self.preferredPAMWeight = args.preferredPAM.split(",")
                try:
                    self.preferredPAMWeight = int(self.preferredPAMWeight)
                except ValueError:
                    try:
                        self.preferredPAMWeight = float(self.preferredPAMWeight)
                    except:
                        raise RuntimeError("PreferredPAM argument must be a number.  Program was passed " + self.preferredPAMWeight + " in preferredPAM argument " + args.preferredPAM)
            else:
                self.preferredPAM = args.preferredPAM.upper()
                self.preferredPAMWeight = False
            systemPAM = self.sequence.split("_")[1]
            self.preferredPAMList = degenerateBaseHandle.NondegenerateBases(self.preferredPAM).permutations()
            if not self.forceGenome:  #if we have a forceGenome argument, this is a subprocess of a selection job and this has already been checked.  It will also fail, since a nondegenerate PAM will be passed.
                systemPAMList = degenerateBaseHandle.NondegenerateBases(systemPAM).permutations()
                for preferredSite in self.preferredPAMList:
                    if not preferredSite in systemPAMList:
                        raise RuntimeError("ABORTED: Your preferred PAM site of " + self.preferredPAM + " is not a subset for the system PAMs of " + systemPAM + ".")
        self.useArray = False
        if args.useArray:
            self.useArray = True
        self.delayIO = False
        if args.delayIO:
            self.delayIO = True
        if args.guideExtension:
            try:
                self.guideExtension = int(args.guideExtension)
            except ValueError:
                raise RuntimeError("Error: Guide extension value must be an integer.")
        else:
            self.guideExtension = 4
        if args.pamExtension:
            try:
                self.pamExtension = int(args.pamExtension)
            except ValueError:
                raise RuntimeError("Error: PAM extension value must be an integer")
        else:
            self.pamExtension = 3
        self.beforeAltStart = args.beforeAltStart
        self.lastExon = args.lastExon
        self.azureTableOut = args.azureTableOut
        if args.azureTableOut:
            azureTableInfo = args.azureTableOut.split(",")
            if not len(azureTableInfo) == 4:
                raise RuntimeError("To output to an azure table, you need to specify the table info and location for the output.  See help for more information.")
            self.azureTableAccountName = azureTableInfo[0]
            self.azureTableName = azureTableInfo[1]
            self.partitionKey = azureTableInfo[2]
            self.rowKey = azureTableInfo[3]
        canonicalPAM = args.canonicalPAM
        if not canonicalPAM:
            self.canonicalPAM = False
            self.canonicalPAMMismatchRangeExtension = 0
        else:
            canonicalPAM = canonicalPAM.upper()
            seqPAM = self.sequence.split("_")[1]
            if not len(seqPAM) == len(canonicalPAM.split(",")[0]):
                raise RuntimeError("Sequence and canonical PAMs must have the same length.  Lengths were %s and %s, respectively." %(len(seqPAM), len(canonicalPAM.split(",")[0])))
            self.canonicalPAMMismatchRangeExtension = calculatePotentialPamMismatch(canonicalPAM)
            self.canonicalPAM = canonicalPAM
            #self.canonicalPAM = degenerateBaseHandle.NondegenerateBases(canonicalPAM).permutations()
        self.outputToFile = args.outputToFile
        if self.outputToFile and os.path.isfile(self.outputToFile) and not args.clobber:
            raise RuntimeError("ABORTED: Output file " + self.outputToFile + " already exists.  Run in clobber mode to overwrite.")
        cacheSize = args.cacheSize
        if cacheSize < 1:
            raise RuntimeError("Error, cacheSize must be > 1.  Passed value was %s" %s(cacheSize))
        if cacheSize < 1000000:
            cacheSize = cacheSize * 1000000
        self.cacheSize = cacheSize
        self.noElevation = args.noElevation

    def setIndexArgs(self, args):  #Validating arguments for launching an indexing supervisor.  This will also require good validations as users are likely to be launching this on their own.
        import os
        self.mode = "index"
        if not args.sequence:
            raise RuntimeError("ABORTED: No search sequence specified.")
        if "_" in args.sequence:
            guide, pam = args.sequence.split("_")
            try:
                guide = int(guide)
            except ValueError:
                pass
            else:
                args.sequence = "N"*guide + "_" + pam
            self.sequence = args.sequence.upper()
        else:
            raise RuntimeError("ABORTED: Invalid sequence passed. Please include an underscore between the guide and PAM sequences.")
        if not len(self.sequence) > 15 and not args.clobber:
            raise RuntimeError("ABORTED: This guide+pam combination appears too short, and will likely cause memory and other errors.  Rerun in clobber mode (argument -9) to proceed anyway.")
        if not args.inputfile:
            raise RuntimeError("ABORTED: No FASTA specified for searching.")
        if os.path.isfile(args.inputfile):
            self.inputfile = args.inputfile
        else:
            raise RuntimeError("ABORTED: FASTA file: " + args.inputfile + " not found.")
        if not args.genome:
            raise RuntimeError("ABORTED: You must specify the name you want to identify this genome by.")
        self.genome = args.genome.upper()
        self.clobber = args.clobber
        self.mock = args.mock
        self.tempDir = args.tempDir
        self.ordered = args.ordered
        self.workerID = args.workerID
        self.species = args.species.upper()
        if args.chunkSize:
            try:
                args.chunkSize = int(args.chunkSize)
            except ValueError:
                raise RuntimeError("ABORTED: Invalid chunk size passed as argument (must be an integer)")
            self.chunkSize = args.chunkSize
        else:
            self.chunkSize = 20000000
        if self.chunkSize < 100:
            self.chunkSize = 1000000 * self.chunkSize
        if args.forceJobIndex:
            try:
                tester = int(args.forceJobIndex)  #Leave this argument as a string until it is used so that a zero value can be passed for the index and will still evaluate to true.
            except ValueError:
                raise RuntimeError("ABORTED: Forced job index argument must be an integer so that it can be used as an index.  If you don't understand why this is, you probably should not be messing with this argument.")
            self.forceJobIndex = args.forceJobIndex
        else:
            self.forceJobIndex = False
        self.noCleanup = args.noCleanup
        self.skipAzimuth = True
        self.verbose = args.verbose
        if not args.parallelJobLimit:
            if self.cluster:
                self.maxParallelJobs = clusterDefaultSelectionModeParallelJobLimit
            if self.standAlone:
                self.maxParallelJobs = standAloneDefaultSelectionModeParallelJobLimit
        else:
            try:
                self.maxParallelJobs = int(args.parallelJobLimit)
            except ValueError:
                raise RuntimeError("ABORTED: Parallel job limit must be an integer.")
            else:
                if self.maxParallelJobs < 1:
                    raise RuntimeError("ABORTED: Parallel job limit must be greater than 0")
        self.scratchFolder = args.scratchFolder
        if not self.scratchFolder:
            self.scratchFolder = "" #making sure this is cast to a string and not a NoneType (although that will probably add to a string with no trouble)
        else:
            if not self.scratchFolder[-1] == "/":
                self.scratchFolder = self.scratchFolder + "/"  #make sure that the directory name is passed ending with a slash so we can prepend it directly to our tempDir name
            if not os.path.isdir(self.scratchFolder):
                try:
                    os.mkdir(self.scratchFolder)
                except OSError:
                    raise RuntimeError("ABORTED: Unable to create scratch folder.  Check if directory containing this folder already exists.")
        self.directToCompiler = False
        self.recreateTree = False
        if args.recreateTree:
            if args.directToCompiler:
                raise RuntimeError("You cannot set both the --directToCompiler and --recreateTree arguments.  If you need both, --directToCompiler will run both for you.")
            else:
                self.recreateTree = True
                self.directToCompiler = True
        else:
            if args.directToCompiler:
                self.directToCompiler = True
        if args.treeLevel1:
            try:
                args.treeLevel1 = int(args.treeLevel1)
            except ValueError:
                raise RuntimeError("ABORTED: Invalid tree level 1 size passed as argument (must be an integer).  We got " + str(args.treeLevel1))
            self.treeLevel1 = args.treeLevel1
        else:
            self.treeLevel1 = 5
        if args.treeLevel2:
            try:
                args.treeLevel2 = int(args.treeLevel2)
            except ValueError:
                raise RuntimeError("ABORTED: Invalid tree level 2 size passed as argument (must be an integer).  We got " + str(args.treeLevel2))
            self.treeLevel2 = args.treeLevel2
        else:
            self.treeLevel2 = 5
        if args.guideExtension:
            try:
                self.guideExtension = int(args.guideExtension)
            except ValueError:
                raise RuntimeError("Error: Guide extension value must be an integer.")
        else:
            self.guideExtension = 4
        if args.pamExtension:
            try:
                self.pamExtension = int(args.pamExtension)
            except ValueError:
                raise RuntimeError("Error: PAM extension value must be an integer")
        else:
            self.pamExtension = 3
        if not args.forcePamList:
            self.forcePamList = False
        else:
            self.forcePamList = args.forcePamList
        cacheSize = args.cacheSize
        if cacheSize < 1:
            raise RuntimeError("Error, cacheSize must be > 1.  Passed value was %s" %s(cacheSize))
        if cacheSize < 1000000:
            cacheSize = cacheSize * 1000000
        self.cacheSize = cacheSize
    
    def setFASTAWorkerArgs(self, args):  #Validate arguments for launching a FASTA indexing worker.  Users are unlikely to be launching this on their own.
        import os
        self.mode = "FASTAWorker"
        self.chromosome = args.chromosome
        self.start = args.start
        self.length = args.length
        if "_" in args.sequence:
            self.sequence = args.sequence
        else:
            raise RuntimeError("ABORTED: Invalid sequence passed to worker. Please include an underscore between the guide and PAM sequences.")
        if os.path.isfile(args.inputfile):
            self.inputfile = args.inputfile
        else:
            raise RuntimeError("ABORTED: FASTA file: " + args.inputfile + " not found.")
        self.genome = args.genome.upper()
        self.tempDir = args.tempDir
        self.workerID = args.workerID
        self.chunkSize = args.chunkSize
        #if os.path.isdir(args.tempDir):
        #    self.tempDir = args.tempDir
        #else:
        #    raise RuntimeError("ABORTED: Unable to detect temporary directory: " + args.tempDir)
        self.skipAzimuth = True
        self.species = args.species
        self.verbose = args.verbose
        try:
            args.treeLevel1 = int(args.treeLevel1)
        except ValueError:
            raise RuntimeError("ABORTED: Invalid tree level 1 size passed as argument (must be an integer).  We got " + str(args.treeLevel1))
        self.treeLevel1 = args.treeLevel1
        try:
            args.treeLevel2 = int(args.treeLevel2)
        except ValueError:
            raise RuntimeError("ABORTED: Invalid tree level 2 size passed as argument (must be an integer).  We got " + str(args.treeLevel2))
        self.treeLevel2 = args.treeLevel2
        if args.guideExtension:
            try:
                self.guideExtension = int(args.guideExtension)
            except ValueError:
                raise RuntimeError("Error: Guide extension value must be an integer.")
        else:
            self.guideExtension = 4
        if args.pamExtension:
            try:
                self.pamExtension = int(args.pamExtension)
            except ValueError:
                raise RuntimeError("Error: PAM extension value must be an integer")
        else:
            self.pamExtension = 3
        if not args.forcePamList:
            self.forcePamList = False
        else:
            self.forcePamList = args.forcePamList
        self.enumeratedContig = args.enumeratedContig
        cacheSize = args.cacheSize
        if cacheSize < 1:
            raise RuntimeError("Error, cacheSize must be > 1.  Passed value was %s" %s(cacheSize))
        if cacheSize < 1000000:
            cacheSize = cacheSize * 1000000
        self.cacheSize = cacheSize
        
    def setCompilerArgs(self, args):
        import os
        self.mode = "compiler"
        if "_" in args.sequence:
            self.sequence = args.sequence
        else:
            raise RuntimeError("ABORTED: Invalid sequence passed to worker. Please include an underscore between the guide and PAM sequences.")
        self.genome = args.genome.upper()
        self.tempDir = args.tempDir
        self.workerID = args.workerID
        self.skipAzimuth = True
        self.species = args.species
        self.verbose = args.verbose
        if not args.bins:
            raise RuntimeError("Tried to run a bin compiler without specifying bins to compile.  It got bored.")
        self.bins = args.bins
        self.noCleanup = False
        if args.noCleanup:
            self.noCleanup = True
        self.enumeratedContig = args.enumeratedContig
        
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

#=================================================SGE Array Job trapper==============================================================================

def arrayJobTrap(tempDir, totalArrayJobs, spoofTaskID):
    import os
    import pickle
    import time
    import random
    if not spoofTaskID:
        try:
            thisJob = int(os.environ["SGE_TASK_ID"])   #Yes, yes, this is a fertile job and we will thrive.  We will rule over all this job and we will call it... thisJob.
        except KeyError:   #I think we should call it your unhandled exception
            raise RuntimeError("Unable to find a valid task ID in OS environment variables.")  #Arghhh... curse your sudden but inevitable betrayal!
    else:
        thisJob = int(spoofTaskID)
    random.seed(thisJob)
    sleepyTime = random.uniform(0,totalArrayJobs/1.5)  #stagger the starts of these jobs to control how much simultaneous IO we run
    print("Random hold for " + str(sleepyTime) + " seconds to avoid overloading the IO system.")
    time.sleep(sleepyTime)
    jobArrayFilePath = tempDir
    if not tempDir.endswith(os.sep):
        jobArrayFilePath += os.sep
    jobArrayFilePath += "jobArray.pkl"
    try:
        jobArrayFile = open(jobArrayFilePath,"rb")
    except FileNotFoundError:
        raise RuntimeError("Unable to find job array file at " + jobArrayFile)
    except:  #Any error besides a missing file could be due to excessive simultaneous access.  If so, wait some random amount of time and try again
        try:
            jobArrayFile = open(jobArrayFilePath,"rb")
        except:  #Give it one more shot.  If it still fails, we probably have a serious problem on our hands want an unhandled exception.
            jobArrayFile = open(jobArrayFilePath,"rb")
    jobArray = pickle.load(jobArrayFile)
    jobArrayFile.close()
    try:
        bashFileList = jobArray[thisJob - 1]  #Subtract 1 because python indexes to 0 while the SGE scheduler indexes to 1
    except IndexError:
        raise RuntimeError("Tried to run job number " + str(thisJob) + " from the job array at " + jobArrayFilePath + ".  It was not found.")
    print("Running array job number " + str(thisJob - 1))
    try:
        nodeNumber = os.environ["HOSTNAME"].replace("n","")
        nodeNumber = int(nodeNumber)
    except ValueError:
        nodeNumber = False
    if False and nodeNumber and nodeNumber in range(2208,2222):  #This seems to be a bad group of nodes.
        import sys
        sys.exit(99)
    else:
        for bashFilePath in bashFileList:
            os.system("bash " + bashFilePath)
    
#=================================================Sequence target analysis/hypervisor objects=================================================================================================================================

class TargetSite(object):  #This object holds attributes that describe a potential target site found in the user-defined target sequence.  This can be extended as we get better ways to describe potential target sites.  Only needs a cut site sequence to be initialized, all else can be set later.
    
    def __init__(self, cutSeq, longSeq = False):
        self.longSeq = longSeq
        self.cutSeq = cutSeq  #this value should come in with the underscore already added between guide and pam
        self.matches = {}   #This is designed to hold the dictionary of match/mismatch sites that gets passed from the search function
        for i in range(0, args.mismatchTolerance + 1):
            self.matches[i] = []
        self.azimuthScore = -1  #Default value for this is -1 to indicate no score.
        self.score = False
        self.acceptable = True  #This flag gets set to false if the target has more than one perfect match in the genome
        self.mismatchRisk = False  #This is a function of how well-matched the sites are and if they are in or near an annotated gene
        self.tooManyMatches = False  #This flags any sites with more than 100 * mismatch tolerance potential off-targets.  They're not especially useful for genome editing, generate obscenely huge outputs, and severely degrade performance when annotated.
        
    def calculateSortValue(self):
        self.sortValue = (self.mismatchRisk, -self.azimuthScore)

class TargetFinder(object):  #This object is analogous to a FASTA indexer, except designed to deal with smaller sequences and can be extended to collect larger windows for analysis in azimuth
    
    def __init__(self, target):
        import degenerateBaseHandle
        self.target = target  #This is the target sequence passed in.  Should be supplied by the user either on the command line or in a FASTA file
        self.longSeq = False  #If we can generate a 30bp site to pass to azimuth, this is where it gets stored.  Note that we may have to force it a bit if we try to apply their model to other systems
        self.lastGroup = 0
        self.done = False
        self.cutWindow = len(args.sequence) - 1  #subtract out the underscore
        self.start = 0  #start is inclusive
        self.end = self.cutWindow
        self.guide, self.pam = args.sequence.split("_")
        if args.preferredPAM:
            self.pam = args.preferredPAM  #If the user specified an optimal PAM sequence, we will use that instead.  It will still probably be degenerate, but a bit more restricted.
        self.pamList = degenerateBaseHandle.NondegenerateBases(self.pam).permutations()
        self.pamLength = len(self.pam)
        self.matches = []  #initialize an empty list to hold our match sites (which will be TargetSite class instances)
        self.done = False
        self.forceAzimuthPam = False  #This indicates that we have forced the azimuth model for this system by trimming the fixed bases on the end of the pam
        self.forceGuide1 = False  #This indicates that we have forced the azimuth model by making the 5' base we submit into the 5' base on the guide
        self.forceGuide3 = False  #This indicates we have done the same thing with the second base from the 5' end (base 3 if the guide is indexed to 1)
        
    def findMatches(self):  #main running function for this object, actually runs the search, gets azimuth scores if needed, and returns the list of matches
        while not self.done:
            import degenerateBaseHandle
            windowSeq = self.target[self.start:self.end]
            revComp = str(degenerateBaseHandle.ReverseComplement(windowSeq))
            if windowSeq[-self.pamLength:] in self.pamList:
                guide = windowSeq[:-self.pamLength]
                pam = windowSeq[-self.pamLength:]
                if not args.skipAzimuth:
                    longSeq = self.getLongSeq(guide, pam,'+')  #tries to get an extended sequence for azimuth analysis
                self.matches.append(TargetSite(guide + "_" + pam, longSeq))
            if revComp[-self.pamLength:] in self.pamList:
                guide = revComp[:-self.pamLength]
                pam = revComp[-self.pamLength:]
                if not args.skipAzimuth:
                    longSeq = self.getLongSeq(guide, pam,'-')
                self.matches.append(TargetSite(guide + "_" + pam, longSeq))
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
        self.done = self.end > len(self.target)
        
    def getLongSeq(self, guide, pam, strand):  #this method gets an extended sequence for azimuth or other analysis if possible
        import degenerateBaseHandle
        pamExtensionLength = 3
        guideExtensionLength = 24 - len(self.guide)
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
    
    def getAzimuth(self, sequence, failedPrevious = False):  #this handles communication with the azure server to get a score.  This can later be replaced if we decide to run a local instance with the source code.
        import urllib.request
        import json
        import time
        import sys #for error catching
        data = {
            "Inputs":{
                "input1":{
                    "ColumnNames":["sequence", "cutsite", "percentpeptide"],
                    "Values":[[sequence, "-1", "-1"]]
                }
            },
                "GlobalParameters": {}
        }
        body = str.encode(json.dumps(data))
        #url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/c24d128abfaf4832abf1e7ef45db4b54/execute?api-version=2.0&details=true'
        url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/5c6cbabaef4947b4b7425e934b6f7d6b/execute?api-version=2.0&details=true'  #slower, but only one working for now.  Use for testing
        api_key = self.azimuthAPIkey
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
        req = urllib.request.Request(url, body, headers)
        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            result = json.loads(result)
            return float(result['Results']['output2']['value']['Values'][0][0])
        except urllib.error.HTTPError as error:
            if error.code == 401:
                print("Unable to use Azimuth due to a possible invalid API key.  Please check on the status of key: " + self.azimuthAPIkey)
            else:
                print("The Azimuth request failed with status code: " + str(error.code))
                print(error.info())
                print(json.loads(error.read().decode('utf-8')))
            self.useAzimuth = False
            return -1  #Remember that -1 is our placeholder value for a failed attempt or no attempt.
        except urllib.error.URLError:
            if not failedPrevious:
                time.sleep(5) #wait 5 seconds before retry
                return self.getAzimuth(sequence, True)
            else:
                print("Unable to reach/find Azimuth server.  Please confirm you are connected to the internet.")
                self.useAzimuth = False
                return -1
        except:  #Allowing this for now while dealing with many possible exceptions due to experimental server and software
            if not failedPrevious:
                time.sleep(5)
                return self.getAzimuth(sequence, True)  #give it another go, because why not...
            else:
                error = sys.exc_info()
                print("Unexpected error in Azimuth scoring:")
                for item in error:
                    print(item)
                return -1
        
    def getAzimuthAPIkey(self):  #this gets the API key from a file
        import os
        if os.path.isfile("azimuth.apikey"):
            file = open("azimuth.apikey", 'r')
            key = file.read()
            file.close()
            key = key.strip()
            return key
        else:
            print("Unable to run azimuth.  Cannot locate API key.  Please save the key the same directory as this program under filename azimuth.apikey.")
            return False
        
    def assignAzimuthScores(self):  #iterate over all our matches and get an azimuth score if there is a saved extended sequence, otherwise it is left as the default -1 value
        for i in range(0,len(self.matches)):
            if self.matches[i].longSeq and self.useAzimuth:
                self.matches[i].azimuthScore = self.getAzimuth(self.matches[i].longSeq)        
                
class TargetSelection(object):  #This is the main running object for the target selection job
    
    def __init__(self):
        printStartUp()
        reportUsage("SELECTION")
        self.targetList = []
        self.indexedGenome = self.selectIndexedGenome() #we will pass this to the search supervisor.  This will save each supervisor a few seconds (probably not significant) and will cover for the potential loss of degeneracy when we pass the sequence to searcher agents 
        print("Checking for target sites")
        self.getTargetSequence()
        if not self.targetList:
            self.targetList = TargetFinder(self.target).findMatches()
        if not self.targetList:
            raise RuntimeError('ABORTED: No suitable target sequences found.')
        if selectionModeTargetLimitPerJob > 0 and len(self.targetList) > selectionModeTargetLimitPerJob and not args.clobber:
            raise RuntimeError("ABORTED: Too many targets in sequence.  Try running a shorter target sequence, a more specific Crispr system, or using clobber mode (argument -9) to override this.")
        print("Found " + str(len(self.targetList)) + " potential target sites.")
        self.createTempDir()
        if not args.useArray:
            self.createJobList()
            self.runJobList()
        else:
            self.createJobArray()
            self.runJobArray()
            self.monitorJobArray()
        self.gatherResults()
        self.sortResults()
        if not args.outputToFile:
            self.reportResults()
        else:
            self.reportToFile()
        if not args.noCleanup:
            self.cleanup()
        
    def getTargetSequence(self):
        if args.targetSequence:  #if the user just passed the sequence as an argument...
            target = args.targetSequence.strip()
            target = target.upper()
            for letter in target:
                if letter not in ['A','T','G','C']:  #reject any degenerate sequences passed (probably reasonable to expect the user to have a good sequence for their target)
                    raise RuntimeError("ABORTED: Invalid letters in targeted DNA sequence")
            self.target = target
        elif args.targetFasta:  #if the user referred us to a file for the sequence...
            try:
                targetFasta = open(args.targetFasta, 'r')
            except FileNotFoundError:
                raise RuntimeError("ABORTED: Unable to open the specified FASTA file")
            else:
                target = ""
                line = targetFasta.readline()
                while line:
                    if ">" in line:  #fasta standards state that a line starting with > is identifying a contig and will not contain sequence
                        line = targetFasta.readline()  #readline is probably less efficient than slurping the whole file.  If the user wants to run this on a sequence big enough that this becomes a concern, they are going to have bigger problems in their future.
                        continue
                    else:
                        line = line.replace("\n","")
                        line = line.upper()
                        for letter in line:
                            if letter not in ["A","T","G","C"]:
                                targetFasta.close()
                                raise RuntimeError("ABORTED: Invalid letters in the sequence file")
                        target += line
                        line = targetFasta.readline()
            self.target = target
            targetFasta.close()
        elif args.targetList:  #if the user passed a list of targets...
            try:
                targetListFile = open(args.targetList, 'r')
            except FileNotFoundError:
                raise RuntimeError("ABORTED: Unable to open the specified list of target sites")
            targetList = []
            line = targetListFile.readline()
            while line:
                line = line.strip()
                line = line.replace("\n","")
                line = line.upper()
                for letter in line:
                    if letter not in ['A','T','G','C','_']:
                        raise RuntimeError("ABORTED: Invalid character specified in target list item.")
                if not "_" in line:
                    line = line[:-len(self.pam)] + "_" + line[-len(self.pam):]
                targetList.append(TargetSite(line))  #we can't get an extended sequence from here, so longSeq will remain the default False value and the azimuth score will remain -1
                line = targetListFile.readline()
            self.targetList = targetList
            targetListFile.close()
            print("Using targets from target list file.")
        else:
            raise RuntimeError("ABORTED: No target sequence or list of target sites given/nothing for me to do.")
    
    def selectIndexedGenome(self):  #uses the user-passed guide_pam scheme to pick an indexed genome (or say if we don't have one) that is suitable for this run.  Remember that the sequence is stored in reverse
        import os
        import degenerateBaseHandle
        if not os.path.isdir(args.genomeListDirectory):
            raise RuntimeError("ABORTED: No indexed genome directory found.  Please run the indexer to create indexed genomes for searching.")
        seqPam, seqGuide = args.sequence[::-1].split("_")
        self.pam = seqPam[::-1]
        self.guide = seqGuide[::-1]
        directoryContents = os.listdir(args.genomeListDirectory)
        for item in directoryContents:
            if not item[0] == "." and "." in item and "_" in item and "NNN" in item:
                itemSeq, itemGenome, species = item.split(".")
                if itemGenome == args.genome:
                    itemPam, itemGuide = itemSeq.split("_")
                    if len(itemPam) == len(seqPam):
                        itemPamList = degenerateBaseHandle.NondegenerateBases(itemPam).permutations()
                        if (seqPam == itemPam or seqPam in itemPam) and len(seqGuide) <= len(itemGuide):
                            return item
        raise RuntimeError("ABORTED: Please create an indexed genome for this search.  No suitable indexed genome was found.")
        
    def createTempDir(self):  #makes a temporary directory for this run.  Completions will clock out here and results will be reported back to it.
        if args.verbose:
            print ("Creating temporary directory")
        import re
        import os
        import datetime
        successful = False
        while not successful:
            currenttime = datetime.datetime.now()
            currenttime = str(currenttime)
            currenttime = re.sub(r'\W','',currenttime)
            self.tempDir = args.scratchFolder + '.shieldHQ' + currenttime
            if os.path.isdir(self.tempDir):
                continue
            try:
                os.mkdir(self.tempDir)
            except OSError:
                continue
            successful = True
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        os.mkdir(self.tempDir + "/result")
        if args.verbose:
            print ("Temporary directory created.")
        return True
        
    def createJobList(self):
        self.jobList = {'queued':[], 'running':[], 'complete':[]}
        for targetSite in self.targetList:
            self.jobList['queued'].append(targetSite)
            
    def runJobList(self):
        import os
        import time
        self.submittedJob = 1
        if not args.mixed:
            maxSimultaneousJobs = args.maxParallelJobs // args.parallelJobs
        else:
            maxSimultaneousJobs = args.maxParallelJobs #because now each site is a single parallel job run on a single node
        while self.jobList['queued'] or self.jobList['running']:
            try:
                while self.jobList['queued'] and len(self.jobList['running']) < maxSimultaneousJobs:
                    self.createJobBash(self.jobList['queued'][0])
                    self.submitJob(self.jobList['queued'][0])
                    self.jobList['running'].append(self.jobList['queued'][0])
                    del self.jobList['queued'][0]
                while len(self.jobList['running']) >= maxSimultaneousJobs or len(self.jobList['queued']) == 0:
                    newlyCompleted = []
                    for i in range(0, len(self.jobList['running'])):
                        if os.path.isfile(self.tempDir + "/completed/" + self.jobList['running'][i].cutSeq):
                            newlyCompleted.append(i)
                    newlyCompleted.sort(reverse = True)  #we need to reverse this list so that we remove items in reverse index order.  If we did not do this, and we had two items on the list (say 1 and 3), we could potentially remove item 1 first, and then item 3 becomes item 2, with what started off as item 4 now targeted for deletion and a very high probability that at some point we will run off the end of the list (IndexError)
                    if newlyCompleted:
                        for completedIndex in newlyCompleted:
                            self.jobList['complete'].append(self.jobList['running'][completedIndex])
                            del self.jobList['running'][completedIndex]
                    if not self.jobList['running'] and not self.jobList['queued']:
                        break
                    time.sleep(10)
            except KeyboardInterrupt:
                for key in list(self.jobList.keys()):
                    print(key)
                    for item in self.jobList[key]:
                        print("\t" + item.cutSeq)
                    if yesAnswer("Continue with run?"):
                        continue
                    else:
                        quit("ABORTED: By your command.")
                    
    def createJobBash(self, job):  #Creates a bash file to submit for running the job
        self.bash = self.tempDir + "/" + str(job.cutSeq) + ".sh"
        bashFile = open(self.bash, 'w')
        bashFile.write("#! /bin/bash\n")
        scratchFolder = ""
        clobber = ""
        if args.clobber:
            clobber = " --clobber"
        if args.scratchFolder:
            scratchFolder = " --scratchFolder " + args.scratchFolder
        if args.cluster:
            systemInfo = " --cluster "
        if args.standAlone:
            systemInfo = " --standAlone "
        if args.mixed:
            systemInfo = " --mixed "
        if args.useArray:
            delayIO = " --delayIO"
        else:
            delayIO = ""
        preferredPAMArg = ""
        if args.preferredPAM:
            preferredPAMArg = " --preferredPAM " + args.preferredPAM
            if args.preferredPAMWeight:
                preferredPAMArg += "," + str(args.preferredPAMWeight)
        # bashFile.write(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode search --mismatchTolerance " + str(args.mismatchTolerance) + clobber + delayIO + preferredPAMArg +" --sequence " + job.cutSeq + " --forceGenome " + self.indexedGenome + " --guideExtension " + str(args.guideExtension) + " --pamExtension " + str(args.pamExtension) +  " --outputDirectory " + self.tempDir + " --parallelJobs " + str(args.parallelJobs) + " --mismatchTolerance " + str(args.mismatchTolerance) + " --genomeDirectory " + args.genomeListDirectory.replace(" ",'\ ') + " --azimuthSequence " + str(job.longSeq) + scratchFolder + systemInfo + "\n")
        bashFile.write(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode search --mismatchTolerance " + str(args.mismatchTolerance) + clobber + preferredPAMArg +" --sequence " + job.cutSeq + " --forceGenome " + self.indexedGenome + " --guideExtension " + str(args.guideExtension) + " --pamExtension " + str(args.pamExtension) +  " --outputDirectory " + self.tempDir + " --parallelJobs " + str(args.parallelJobs) + " --mismatchTolerance " + str(args.mismatchTolerance) + " --genomeDirectory " + args.genomeListDirectory.replace(" ",'\ ') + " --azimuthSequence " + str(job.longSeq) + scratchFolder + systemInfo + "\n")

        bashFile.close()
    
    def submitJob(self, job):  #submits the bash file to the queue scheduler
        shortName = "ShieldHQ" + str(self.submittedJob)
        self.submittedJob += 1
        if args.cluster or args.mixed:
            import os
            command = "qsub -cwd -V -N " + shortName + " -l h_data=2G,time=23:59:00 -e " + os.getcwd() +  "/schedulerOutput/ -o " + os.getcwd() + "/schedulerOutput/ " + self.bash
            if not args.mock:
                import os
                import time
                submitted = False
                while not submitted:
                    submission = os.system(command)
                    if not submission == 0:
                        print("Job submission unsuccessful, waiting 5 seconds and resubmitting.")
                        time.sleep(5)
                        continue
                    else:
                        submitted = True
            else:
                print ("MOCK SUBMIT: " + command)
        if args.standAlone:
            command = "bash " + self.bash
            if not args.mock:
               import subprocess
               import time
               subprocess.Popen(command, shell = True)
               print("Holding for 5 seconds.")
               time.sleep(5) #First thing the search supervisor will do is load the tree pickle file.  This can degrade performance if they ALL try to load the same file simultaneously.
            else:
                print ("MOCK SUBMIT: " + command)

    def createJobArray(self):
        self.jobArray = []
        if len(self.targetList) <= clusterMaxArrayJobs:
            for targetSite in self.targetList:
                self.createJobBash(targetSite)
                self.jobArray.append([self.bash])
        else:
            for i in range(0, clusterMaxArrayJobs):
                self.jobArray.append([])
            for i in range(0, len(self.targetList)):
                self.createJobBash(self.targetList[i])
                self.jobArray[i % clusterMaxArrayJobs].append(self.bash)          
            
    def runJobArray(self):
        import os
        import time
        import pickle
        jobArrayFilePath = self.tempDir + os.sep + "jobArray.pkl"
        jobArrayFile = open(jobArrayFilePath,'wb')
        pickle.dump(self.jobArray, jobArrayFile)
        jobArrayFile.close()
        arrayRunnerBashFilePath = self.tempDir + os.sep + "arrayRunner.sh"
        arrayRunnerBashFile = open(arrayRunnerBashFilePath, 'w')
        arrayRunnerBashFile.write("#!/bin/bash\n")
        arrayRunnerBashFile.write(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --arrayJob --tempDir " + self.tempDir + " --totalArrayJobs " + str(len(self.jobArray)))
        arrayRunnerBashFile.close()
        jobRange = " 1-" + str(len(self.jobArray)) + " "
        command = "qsub -cwd -V -N ShieldHQ -l h_data=4G,time=23:59:00 -e " + os.getcwd() +  "/schedulerOutput/ -o " + os.getcwd() + "/schedulerOutput/ " + "-t " + jobRange + arrayRunnerBashFilePath
        if not args.mock:
            failedSubmissions = 0
            submitted = False
            while not submitted and failedSubmissions < 10:
                submission = os.system(command)
                if not submission == 0:
                    print("Job submission unsuccessful, waiting 5 seconds and resubmitting.")
                    failedSubmissions += 1
                    time.sleep(5)
                    continue
                else:
                    submitted = True
        else:
            print ("MOCK SUBMIT: " + command)
            
    def monitorJobArray(self):
        import time
        import os
        jobMonitorArray = []
        for item in self.targetList:
            jobMonitorArray.append([item.cutSeq, False])  #each item added to this array will be the job identifier in the first index (0) and a boolean indicating it is done.  Lacking easy access to a TARDIS, we can assume no job is completed before it starts.  Should this change, it will still work anyway.
        totalJobs = len(jobMonitorArray)
        completedJobs = 0  #again, the TARDIS thing
        print("Waiting for " + str(totalJobs - completedJobs) + " of " + str(totalJobs) + " sites to complete.           ", end = "\r")
        while completedJobs < totalJobs:  #if it becomes greater, we have a problem
            for i in range(0, totalJobs):
                if not jobMonitorArray[i][1]: #if we already know it's done, we don't need to check again
                    if os.path.isfile(self.tempDir + os.sep + "completed" + os.sep + jobMonitorArray[i][0]):
                        jobMonitorArray[i][1] = True
                        completedJobs += 1
            print("Waiting for " + str(totalJobs - completedJobs) + " of " + str(totalJobs) + " sites to complete.           ", end = "\r")
            time.sleep(1)
        print("\nCompleted!  Reporting results.")
                    
    def gatherResults(self):  #gathers the results from the worker processes (passed via pickle), checks for unacceptable sites (ones that have perfect matches in multiple genomic locations), and calculates mismatch risk numbers
        import pickle
        printedNoPerfectMatchWarning = False
        for i in range(0,len(self.targetList)):
            totalMismatchRisk = 0
            genesCounted = [] #prevent us from counting multiple hits in the same gene twice
            inputFile = open(self.tempDir + "/result/" + self.targetList[i].cutSeq, 'rb')
            result = pickle.load(inputFile)
            inputFile.close()
            if result['matches'] == -1:
                self.targetList[i].acceptable = False
                self.targetList[i].matches = {0:["Aborted search due to high number of potential off-targets."]}
                for j in range(1, args.mismatchTolerance + 1):
                    self.targetList[i].matches[j] = []
                self.targetList[i].mismatchRisk = 9999999
            else:
                self.targetList[i].matches = result['matches']
            self.targetList[i].azimuthScore = result['azimuthScore']
            if len(self.targetList[i].matches[0]) > 1:
                first = self.targetList[i].matches[0][0].gene
                for site in self.targetList[i].matches[0]:
                    if site.gene != first:
                        self.targetList[i].acceptable = False
                        break
            try:
                if self.targetList[i].matches[0][0].tooManyOtherSites:    
                    self.targetList[i].tooManyMatches = self.targetList[i].matches[0][0].tooManyOtherSites
            except IndexError:
                if not printedNoPerfectMatchWarning:
                    print("WARNING: At least one target site did not perfectly match to the genome.  If you are targeting a mutant allele or artificial construct, this is to be expected.  If you are targeting a native sequence, this may indicate an error.  Please manually inspect any perfect matches, as this program assumes the first perfect match for any target is the intended target.")
                    printedNoPerfectMatchWarning = True
            except AttributeError:
                print("Got attribute error around 1327.")
                print(self.targetList[i].matches[0])
                print(self.targetList[i].matches[0][0])
            for j in range(0, args.mismatchTolerance + 1):
                for k in range(0, len(self.targetList[i].matches[j])):
                    risk = self.targetList[i].matches[j][k].calculateMismatchRisk()
                    if not (j == 0 and k == 0) or self.targetList[i].matches[j][k].gene in genesCounted:
                        totalMismatchRisk += risk
                    if self.targetList[i].matches[j][k].gene and self.targetList[i].matches[j][k].gene not in genesCounted:
                        genesCounted.append(self.targetList[i].matches[j][k].gene)
            self.targetList[i].mismatchRisk = totalMismatchRisk
                        
    def sortResults(self):  #Sorts in ascending order by mismatch risk first, then by azimuth score (done by sorting on the negative value of the azimuth score).  If no azimuth was given, the result will be shown last
        import operator
        for i in range(0, len(self.targetList)):
            self.targetList[i].calculateSortValue()        
        self.targetList.sort(key = operator.attrgetter('sortValue'))
        
    def reportResults(self):  #Reports results to STDOUT.  At some point, I should probably offer alternatives to output to a file or even some data object format like JSON
        import sys
        print("Command: " + " ".join(sys.argv))
        unacceptableHeaderPrinted = False
        tooManyMatchHeaderPrinted = False
        for target in self.targetList:
            if target.acceptable and not (target.tooManyMatches and not args.clobber):
                print(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk))
                if int(target.azimuthScore) != -1:
                    print(" "*len(target.cutSeq) + "\tAzimuth Score: " + str(target.azimuthScore))
                else:
                    print(" "*len(target.cutSeq) + "\tAzimuth Score: Cannot determine")
                for count in range(0, args.mismatchTolerance + 1):
                    print("\tMismatches: " + str(count))
                    for site in target.matches[count]:
                        print("\t\t" + str(site))
        for target in self.targetList:
            if not target.acceptable:
                if not unacceptableHeaderPrinted:
                    print("******SITES WITH PERFECT MATCHES ELSEWHERE IN THE GENOME******")
                    unacceptableHeaderPrinted = True
                print(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk))
                for count in range(0, args.mismatchTolerance + 1):
                    print("\tMismatches: " + str(count))
                    for site in target.matches[count]:
                        print("\t\t" + str(site))
        for target in self.targetList:
            if target.tooManyMatches and not args.clobber:
                if not tooManyMatchHeaderPrinted:
                    print("******SITES WITH TOO MANY POTENTIAL MISMATCHES TO DISPLAY******")
                    tooManyMatchHeaderPrinted = True
                print(target.cutSeq + "\tTotal off-target sites: " + str(target.tooManyMatches))
                        
    def reportToFile(self): #Reports results to a file passed as the appropriate argument
        output = open(args.outputToFile,'w')  #We validated that this is not an existing file (or we are willing to clobber it) in the arg checking above
        import sys
        output.write("Command: " + " ".join(sys.argv) + "\n")
        unacceptableHeaderPrinted = False
        tooManyMatchHeaderPrinted = False
        for target in self.targetList:
            if target.acceptable and not (target.tooManyMatches and not args.clobber):
                output.write(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk) + "\n")
                if int(target.azimuthScore) != -1:
                    output.write(" "*len(target.cutSeq) + "\tAzimuth Score: " + str(target.azimuthScore) + "\n")
                else:
                    output.write(" "*len(target.cutSeq) + "\tAzimuth Score: Cannot determine" + "\n")
                for count in range(0, args.mismatchTolerance + 1):
                    output.write("\tMismatches: " + str(count) + "\n")
                    for site in target.matches[count]:
                        output.write("\t\t" + str(site) + "\n")
        for target in self.targetList:
            if not target.acceptable:
                if not unacceptableHeaderPrinted:
                    output.write("******SITES WITH PERFECT MATCHES ELSEWHERE IN THE GENOME******" + "\n")
                    unacceptableHeaderPrinted = True
                output.write(target.cutSeq + "\tMismatch Risk: " + str(target.mismatchRisk) + "\n")
                for count in range(0, args.mismatchTolerance + 1):
                    output.write("\tMismatches: " + str(count) + "\n")
                    for site in target.matches[count]:
                        output.write("\t\t" + str(site) + "\n")
        for target in self.targetList:
            if target.tooManyMatches and not args.clobber:
                if not tooManyMatchHeaderPrinted:
                    output.write("******SITES WITH TOO MANY POTENTIAL MISMATCHES TO DISPLAY******\n")
                    tooManyMatchHeaderPrinted = True
                output.write(target.cutSeq + "\tTotal off-target sites: " + str(target.tooManyMatches) + "\n")
                        
    def cleanup(self):
        import shutil
        import time
        try:
            shutil.rmtree(self.tempDir)
        except OSError:
            time.sleep(5)
            try:
                shutil.rmtree(self.tempDir)
            except OSError:
                print("Error removing working folder " + self.tempDir + " please remove manually.")

#=================================================Azimuth analysis object==================================================================================================================

class AzimuthAnalysis(object):

    def __init__(self, sequence, failedPrevious = False):  #this handles communication with the azure server to get a score.  This can later be replaced if we decide to run a local instance with the source code.
        try:
            import predictionCaller
            sequence = sequence.replace("_","")
            score = predictionCaller.run("azimuth", sequence)
            if len(score) == 1:
                score = score[0]
            self.score = score
        except ImportError:
            print("Trying remote Azimuth analysis")
            import urllib.request
            import json
            import time
            import sys #for error catching
            self.azimuthAPIkey = self.getAzimuthAPIkey()
            if not self.azimuthAPIkey:
                self.score = -1
            else:
                data = {
                    "Inputs":{
                        "input1":{
                            "ColumnNames":["sequence", "cutsite", "percentpeptide"],
                            "Values":[[sequence, "-1", "-1"]]
                        }
                    },
                        "GlobalParameters": {}
                }
                body = str.encode(json.dumps(data))
                #url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/c24d128abfaf4832abf1e7ef45db4b54/execute?api-version=2.0&details=true'
                url = 'https://ussouthcentral.services.azureml.net/workspaces/ee5485c1d9814b8d8c647a89db12d4df/services/5c6cbabaef4947b4b7425e934b6f7d6b/execute?api-version=2.0&details=true'  #slower, but only one working for now.  Use for testing
                api_key = self.azimuthAPIkey
                headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
                req = urllib.request.Request(url, body, headers)
                try:
                    response = urllib.request.urlopen(req)
                    result = response.read().decode('utf-8')
                    result = json.loads(result)
                    self.score = float(result['Results']['output2']['value']['Values'][0][0])
                except urllib.error.HTTPError as error:
                    if error.code == 401:
                        print("Unable to use Azimuth due to a possible invalid API key.  Please check on the status of key: " + self.azimuthAPIkey)
                    else:
                        print("The Azimuth request failed with status code: " + str(error.code))
                        print(error.info())
                        print(json.loads(error.read().decode('utf-8')))
                    self.useAzimuth = False
                    self.score = -1  #Remember that -1 is our placeholder value for a failed attempt or no attempt.
                except urllib.error.URLError:
                    if not failedPrevious:
                        time.sleep(5) #wait 5 seconds before retry
                        self.score = AzimuthAnalysis(sequence, True).score
                    else:
                        print("Unable to reach/find Azimuth server.  Please confirm you are connected to the internet.")
                        self.useAzimuth = False
                        self.score = -1
                except:  #Allowing this for now while dealing with many possible exceptions due to experimental server and software
                    if not failedPrevious:
                        time.sleep(5)
                        self.score = AzimuthAnalysis(sequence, True)  #give it another go, because why not...
                    else:
                        error = sys.exc_info()
                        print("Unexpected error in Azimuth scoring:")
                        for item in error:
                            print(item)
                        self.score = -1
        
    def getAzimuthAPIkey(self):  #this gets the API key from a file
        import os
        if os.path.isfile("azimuth.apikey"):
            file = open("azimuth.apikey", 'r')
            key = file.read()
            file.close()
            key = key.strip()
            return key
        else:
            print("Unable to run azimuth.  Cannot locate API key.  Please save the key the same directory as this program under filename azimuth.apikey.")
            return False
        
def calculateElevationScoreOneBlock(intendedTarget, offTargetList):
    # data = []     #Hooking out code, comment when not hooking out this portion
    # for offTarget in offTargetList:
    #     data.append(-1)
    #return data
    import json
    import sys
    import time
    import urllib.request
    import urllib.parse
    import socket
    import datetime
    data = []
    print("Submitting %s sites." %(len(offTargetList)))
    for offTarget in offTargetList:
        data.append(("wildtype", intendedTarget))
        data.append(("offtarget", offTarget))
    urlData = bytes(urllib.parse.urlencode(data).encode())
    #print(urlData)
    successful = False
    timeout = max([len(offTargetList) * 0.5, 300]) #allowing 1/10 second per site to scale with the size of the request with a minimum time of 90
    failures = 0
    while not successful:
        if failures > 150:
            urlHandle = urllib.request.urlopen("http://elcloud.cloudapp.net/elevation", urlData, timeout = 600)  #we've already filtered out very large requests, so if this is not long enough, time isn't the problem
        else:
            try:
                requestStart = datetime.datetime.now()
                urlHandle = urllib.request.urlopen("http://elcloud.cloudapp.net/elevation", urlData, timeout = timeout)
                successful = True
            except urllib.error.HTTPError as e:
                print("Elevation returned error: %s while running %s sites." %(e.fp.msg, len(offTargetList)), file = sys.stderr)
                time.sleep(min([1.7**failures, 300]))
                failures += 1
            except (socket.timeout, urllib.error.URLError):
                print("Elevation call timed out after: %s seconds while running %s sites." %(timeout, len(offTargetList)), file = sys.stderr)
                #time.sleep(min([1.7**failures, 300]))
                failures += 1
    requestTime = datetime.datetime.now() - requestStart
    print("Got Elevation scores in %s with %s retries for %s sites." %(requestTime, failures, len(offTargetList)))
    result = json.loads(urlHandle.read().decode("utf-8"))
    return result["elevation score"]

def calculateElevationScore(intendedTarget, offTargetListDuped, maxRequestSize = 250):
    data = []     #Hooking out code, comment when not hooking out this portion
    # for offTarget in offTargetListDuped:
    #     data.append(-1)
    # return data
    import json
    import sys
    import time
    import urllib.request
    import urllib.parse
    import socket
    import datetime
    offTargetMap = {}
    for i in range(0,len(offTargetListDuped)):
        if not offTargetListDuped[i] in offTargetMap:
            offTargetMap[offTargetListDuped[i]] = []
        offTargetMap[offTargetListDuped[i]].append(i)
    offTargetList = list(offTargetMap.keys())
    data = []
    print("Submitting %s sites. %s redundant sites deduplicated." %(len(offTargetList), len(offTargetListDuped) - len(offTargetList)))
    # for offTarget in offTargetList:
    #     data.append(("wildtype", intendedTarget))
    #     data.append(("offtarget", offTarget))
    # urlData = bytes(urllib.parse.urlencode(data).encode())
    #print(urlData)
    successful = False
    timeout = 300 # max([len(offTargetList) * 0.5, 300]) #allowing 1/10 second per site to scale with the size of the request with a minimum time of 90
    remainingTargets = offTargetList.copy()
    targetBuffer = []
    resultCollector = []
    completed = False
    while remainingTargets:    
        failures = 0
        targetBuffer = []
        data = []
        for i in range(0, maxRequestSize):
            try:
                targetBuffer.append(remainingTargets.pop(0))
            except IndexError:
                break
        successful = False
        data = []
        for offTarget in targetBuffer:
            data.append(("wildtype", intendedTarget))
            data.append(("offtarget", offTarget))
        urlData = bytes(urllib.parse.urlencode(data).encode())
        while not successful:
            if failures > 150:
                urlHandle = urllib.request.urlopen("http://elcloud-40.cloudapp.net/elevation", urlData, timeout = 600)  #we've already filtered out very large requests, so if this is not long enough, time isn't the problem
            else:
                try:
                    requestStart = datetime.datetime.now()
                    urlHandle = urllib.request.urlopen("http://elcloud-40.cloudapp.net/elevation", urlData, timeout = timeout)
                    successful = True
                except urllib.error.HTTPError as e:
                    print(str(urlData).replace("&","\n"))
                    print("Elevation returned error: %s while running %s sites." %(e.fp.msg, len(targetBuffer)), file = sys.stderr)
                    time.sleep(min([1.7**failures, 300]))
                    failures += 1
                except (socket.timeout, urllib.error.URLError):
                    print("Elevation call timed out after: %s seconds while running %s sites." %(timeout, len(targetBuffer)), file = sys.stderr)
                    #time.sleep(min([1.7**failures, 300]))
                    failures += 1
        requestTime = datetime.datetime.now() - requestStart
        print("Got Elevation scores in %s with %s retries for %s sites." %(requestTime, failures, len(targetBuffer)), file = sys.stderr)
        resultCollector += json.loads(urlHandle.read().decode("utf-8"))["elevation score"]
        #print(resultCollector)
    reorderedResults = []
    for i in range(0, len(offTargetListDuped)):
        reorderedResults.append(None)
    for i in range(0,len(offTargetList)):
        cellsToFill = offTargetMap[offTargetList[i]]
        for cell in cellsToFill:
            reorderedResults[cell] = resultCollector[i]
    if None in reorderedResults:
        raise RuntimeError("No 'None' cells should be left in reordered results.")
    print("Returning %s Elevation scores." %(len(reorderedResults)))
    return reorderedResults

def calculateElevationScoreLocal(intendedTarget, offTargetListDuped):
    import datetime
    import predictionCaller
    startTime = datetime.datetime.now()
    offTargetListDuped = [item[::-1] for item in offTargetListDuped]  #fix this when the data structure is no longer reversed
    offTargetMap = {}
    for i in range(0,len(offTargetListDuped)):
        if not offTargetListDuped[i] in offTargetMap:
            offTargetMap[offTargetListDuped[i]] = []
        offTargetMap[offTargetListDuped[i]].append(i)
    offTargetList = list(offTargetMap.keys())
    offTargetListDuped = [item[::-1] for item in offTargetListDuped]  #fix this when the data structure is no longer reversed
    data = []
    print("Submitting %s sites. %s redundant sites deduplicated." %(len(offTargetList), len(offTargetListDuped) - len(offTargetList)))
    #print(offTargetList)
    #print("\n\n")
    #print(intendedTarget)
    results = predictionCaller.run("elevation", intendedTarget, offTargetList)
    reorderedResults = []
    for i in range(0, len(offTargetListDuped)):
        reorderedResults.append(None)
    for i in range(0,len(offTargetList)):
        cellsToFill = offTargetMap[offTargetList[i]]
        for cell in cellsToFill:
            reorderedResults[cell] = results[i]
    if None in reorderedResults:
        raise RuntimeError("No 'None' cells should be left in reordered results.")
    runtime = datetime.datetime.now() - startTime
    print("Returning %s Elevation scores in %s." %(len(reorderedResults), runtime))
    return reorderedResults

#================================================Search Objects to find potential targets in an indexed genome based on guide RNA sequence=======================================================
    
class MatchSite(object):  #Note that this is also used when we unpickle this object from the hypervisor (target selection) function
    def __init__(self, chrom, begin, end, matchSeq, score, strand, colorScheme, mismatches, extendedMatchSeq):
        self.chrom = chrom
        self.begin = begin
        self.end = end
        self.matchSeq = matchSeq
        self.score = score
        self.strand = strand
        self.colorScheme = colorScheme
        self.extendedMatchSeq = extendedMatchSeq
        self.thickStart = ""
        self.thickEnd = ""
        self.azimuth = False
        self.delimiter = "\t"
        try:  #this deals with sorting chromosomes that can be identified by numbers or X, Y, and M and being able to sort by number and then by letter
            sortChr = int(self.chrom)
            sortChr = str(sortChr).zfill(2)
        except ValueError:
            sortChr = self.chrom
        self.sortValue = (sortChr,int(begin))  #This value helps sort by chromosome/location
        self.mismatchRisk = False
        self.mismatches = mismatches
        self.gene = False
        self.tooManyOtherSites = False
        self.perfectMatch = False
        self.elevationScore = False
        self.stackerScore = False
        
    def calculateMismatchRisk(self):  #
        if self.mismatchRisk:
            return self.mismatchRisk
        else:
            self.mismatchRisk = args.mismatchTolerance + 2 - self.mismatches
            if self.gene:
                self.mismatchRisk = self.mismatchRisk ** 2
            if args.preferredPAMWeight:
                pamLength = len(args.sequence.split("_")[1])
                if self.matchSeq[-pamLength:] in args.preferredPAMList:
                    self.mismatchRisk = self.mismatchRisk * args.preferredPAMWeight
            return self.mismatchRisk
        
    def __str__(self):  #quick way to output the info on the match site
        if not self.gene:
            printGene = "NoGene"
        else:
            printGene = self.gene.split("[")[0].strip() #info on source of gene annotation follows the open bracket.  This just takes the part before it.
        if self.elevationScore == -1:
            printOffTargetAzimuth = "Not Determined"
        else:
            elevationScore = str(self.elevationScore)
        printName = "/".join([printGene, self.matchSeq[::-1]])
        returnThings = [self.chrom, str(self.begin), str(self.end), printName, str(self.score), self.strand, self.thickStart, self.thickEnd, self.colorScheme]
        return self.delimiter.join(returnThings)
    
    def getElevationScore(self, intendedTarget):
        if not self.elevationScore == False:
            return self.elevationScore
        else:
            if intendedTarget == self.matchSeq:
                self.perfectMatch = True
            self.elevationScore = calculateElevationScoreLocal(intendedTarget.replace("_",""), self.matchSeq.replace("_",""), self.extendedMatchSeq.replace("_",""))
            self.score = self.elevationScore
            return self.elevationScore
        
    def azureTableMismatchData(self):
        if not self.gene:
            gene = "NoGene"
        else:
            gene = self.gene
        return [self.chrom, self.begin, gene, self.elevationScore]      

def compileExtendedSeq(target, before, after):
    targetSeq = args.sequence
    targetGuide, targetPam = targetSeq.split("_")
    guideLength = len(targetGuide)
    pamLength = len(targetPam)
    beforeExtension = args.guideExtension
    afterExtension = args.pamExtension
    extendedGuideLength = guideLength + beforeExtension
    longSeq = before + target[::-1] + after[:afterExtension]
    longGuide, longPam = longSeq.split("_")
    extendedGuide = longGuide[-extendedGuideLength:]
    return extendedGuide + "_" + longPam


class SearchSupervisor(object):
    
    def __init__(self):
        import os
        if not args.forceGenome:
            printStartUp()
            reportUsage("SEARCH") 
            genomeDirectory = self.selectIndexedGenome()
        else:
            genomeDirectory = args.forceGenome
            pam, sequence, self.species = genomeDirectory.split(".")
        args.inputDirectory = args.genomeListDirectory + os.sep + genomeDirectory
        self.genomeDirectory = args.genomeListDirectory + genomeDirectory
        self.tooManyMismatches = False
        self.aggregateOffTargetScore = False
        #self.createTempDir()
        print("Creating job list")
        self.runSearchJob() #changed for single core
        if not self.tooManyMismatches:
            self.multiplePerfectMatches = len(self.matches[0]) > 1
        else:
            self.multiplePerfectMatches = False
            #print("Assigning jobs")
            #self.assignJobs()
        print("Calculating Azimuth Score")
        self.azimuthScore = -1
        if args.azimuthSequence:  #Do this after finishing local job, but before monitoring, since we will still be waiting on them
            self.azimuthScore = AzimuthAnalysis(args.azimuthSequence).score
        #print("Monitoring")
        #self.monitorJobs()
        #print("Gathering")
        #self.gatherJobs()
        if not self.tooManyMismatches:
            print("Sorting")
            self.sortResults()
            print("Annotating")
            import localAnnotation
            self.annotator = localAnnotation.LocalGeneCheck()
            self.annotateResults()
            if not args.noElevation:
                print("Calculating Elevation Scores")
                self.applyElevationScores(args.sequence)
                self.aggregateOffTargetScore = self.calculateAggregatedScore()
        print("Reporting")
        if args.outputToFile:
            self.outputToFile()
        elif args.outputDirectory:
            self.reportToDirectory()
        elif args.azureTableOut:
            self.reportToAzureTable()
        else:
            self.reportResults()
        #if not args.noCleanup:
        #    self.cleanup()
        
    def selectIndexedGenome(self):
        import os
        import degenerateBaseHandle
        if not os.path.isdir(args.genomeListDirectory):
            raise RuntimeError("ABORTED: No indexed genome directory found.  Please run the indexer to create indexed genomes for searching.")
        seqPam, seqGuide = args.sequence[::-1].split("_")
        directoryContents = os.listdir(args.genomeListDirectory)
        for item in directoryContents:
            if not item[0] == "." and "." in item and "_" in item and "NNN" in item:
                itemSeq, itemGenome, itemSpecies = item.split(".")
                if itemGenome == args.genome:
                    itemPam, itemGuide = itemSeq.split("_")
                    if len(seqPam) == len(itemPam):
                        itemPamList = degenerateBaseHandle.NondegenerateBases(itemPam).permutations()
                        if (seqPam.upper() == itemPam.upper() or seqPam.upper() in itemPamList) and len(seqGuide) <= len(itemGuide):
                            self.species = itemSpecies.strip().lower()
                            #args.inputDirectory = args.genomeListDirectory + os.sep + item
                            return item
        raise RuntimeError("ABORTED: Please create an indexed genome for this search.  No suitable indexed genome was found.")
                
    def createTempDir(self):
        if args.verbose:
            print ("Creating temporary directory")
        import re
        import os
        import datetime
        successful = False
        while not successful:
            currenttime = datetime.datetime.now()
            currenttime = str(currenttime)
            currenttime = re.sub(r'\W','',currenttime)
            self.tempDir = args.scratchFolder + '.dsNickFuryMission' + currenttime
            if os.path.isdir(self.tempDir):
                continue
            try:
                os.mkdir(self.tempDir)
            except OSError:
                continue
            successful = True
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        os.mkdir(self.tempDir + "/result")
        if args.verbose:
            print ("Temporary directory created.")
        return True
    
    def runSearchJob(self):
        import os
        import dataPacker
        import pickle
        guide = args.sequence.split("_")[0]
        encodingInfoFileName = self.genomeDirectory + os.sep + "genCodeData.pkl"
        if not os.path.isfile(encodingInfoFileName):
            raise RuntimeError("No encoding data file found at %s" %(encodingInfoFileName), end = "\r")
        encodingInfoFile = open(encodingInfoFileName, 'rb')
        encodingInfo = pickle.load(encodingInfoFile)
        encodingInfoFile.close()
        self.twoBitHandler = dataPacker.DataPacker(encodingInfo.compressionScheme, encodingInfo.pamLength, encodingInfo.guideLength, encodingInfo.guideExtendLength, encodingInfo.pamExtendLength)
        treeFileName = self.genomeDirectory + os.sep + "tree.pkl"
        if not os.path.isfile(treeFileName):
            raise RuntimeError("No tree file found where there should be one at %s" %(treeFileName))
        treeHandler = TreeNavigator(treeFileName, guide)
        matchBytes = {}
        for i in range(0,args.mismatchTolerance + 1 + args.endClip + args.canonicalPAMMismatchRangeExtension):   #adding 2 because we go out to the range of mismatchTolerance and one more for sites with that many mismatches plus a non-canonical pam
            matchBytes[i] = bytes()
        siteBuffer = bytes()
        nextTargetFileInfo = treeHandler.getNextLevel2()
        if not nextTargetFileInfo:  #in the unlikely event everything was disqualified before analysis
            return matchBytes
        totalMatchedSites = 0
        print("Using a cache size of %s" %(args.cacheSize))
        while nextTargetFileInfo:
            print("Loading binary site data.")
            while len(siteBuffer) < args.cacheSize:  #will probably have to play with this buffer size later, and probably make it user-defined
                seed1, bytesToRead = nextTargetFileInfo
                dataFileName = self.genomeDirectory + os.sep + "targets" + os.sep + seed1 + ".bct"
                dataFile = open(dataFileName, 'rb')
                for site in bytesToRead:
                    dataFile.seek(site[0])
                    siteBuffer += dataFile.read(site[1])
                dataFile.close()
                nextTargetFileInfo = treeHandler.getNextLevel2()
                if not nextTargetFileInfo:
                    break
            if siteBuffer:
                if not nextTargetFileInfo:
                    print("Analyzing final set of sites")
                else:
                    print("Buffer filled, analyzing current set of sites before emptying")
                siteCount, returnedSites = self.twoBitHandler.qualifyingSeqTableFromBuffer(siteBuffer, guide, args.canonicalPAM, args.mismatchTolerance, args.endClip)
                totalMatchedSites += siteCount
                for key in list(returnedSites.keys()):
                    matchBytes[key] += returnedSites[key]
                siteBuffer = bytes()
            if args.matchSiteCutoff and totalMatchedSites > args.matchSiteCutoff:
                self.tooManyMismatches = True
                break
        if not self.tooManyMismatches:
            print("Found %s matching sites." %(totalMatchedSites))
            self.matches = self.decodeMatchBytes(matchBytes, encodingInfo.contigDenumerationTable)
            
    def decodeMatchBytes(self, matchBytes, contigDenumerationTable):
        keys = list(matchBytes.keys())
        colorScheme = self.createColorScheme()
        matches = {}
        for key in keys:
            matches[key] = []
            position = 0
            siteByteLength = self.twoBitHandler.siteDataByteLength
            while position < len(matchBytes[key]):
                decodedSite = self.twoBitHandler.decodeData(matchBytes[key][position : position + siteByteLength])
                matches[key].append(MatchSite(contigDenumerationTable[decodedSite.enumeratedContig], decodedSite.start, decodedSite.end, decodedSite.sequence, 1000 - ((1000/len(keys))*key), decodedSite.strand, colorScheme[key], key, compileExtendedSeq(decodedSite.sequence, decodedSite.guideExtension, decodedSite.pamExtension)))
                position += siteByteLength
        return matches
                 
    def sortResults(self):
        import operator
        if args.verbose:
            print("Starting to sort.")
        for key in list(self.matches.keys()):
            if args.verbose:
                print("Sorting group " + str(i))
            self.matches[key].sort(key = operator.attrgetter('sortValue'))
    
    def getAnnotation(self, site, expand = 100, failedPrevious = False):
        if self.species.upper() == "HUMAN":
            begin = int(site.begin) - expand
            if begin < 1:
                begin = 1
            end = int(site.end) + expand
            #print("%s,%s,%s" %(site.chrom, begin, end))
            geneList = self.annotator.checkLocus(site.chrom, begin, end, "protein_coding")
            #print(geneList)
            return ", ".join(geneList)
        else:
            import urllib.request
            import json
            import time
            import random
            begin = int(site.begin) - expand
            if begin < 1:
                begin = 1
            end = int(site.end) + expand
            urlBase = 'http://rest.ensembl.org/overlap/region/' + self.species + '/'
            urlLocus = str(site.chrom) + ":" + str(begin) + "-" + str(end)
            urlArguments = "?feature=gene;content-type=application/json"
            fullURL = urlBase + urlLocus + urlArguments
            try:
                ensembl = urllib.request.urlopen(fullURL, timeout = 5)  #setting a timeout to avoid getting bogged down in bad requests
                ensembl = ensembl.read().decode('utf-8')
                ensembl = json.loads(ensembl)
            except urllib.error.HTTPError as error:
                if not failedPrevious:
                    time.sleep(5)
                    return self.getAnnotation(site, expand, True)
                else:
                    print("The ensembl annotation request failed with status code: " + str(error.code))
                    print(error.info())
                    print(error.read().decode('utf-8'))
                    return "Unable to get annotation.  Error code: " + str(error.code) + " FullURL = " + fullURL
            except urllib.error.URLError:
                if not failedPrevious:
                    time.sleep(random.uniform(1,10))
                    return self.getAnnotation(site, expand, True)
                else:
                    print("Unable to reach/find ensembl server.  Please confirm you are connected to the internet.")
                    return "Unable to contact ensembl. (URL/network error)"
            except Exception as error:
                if not failedPrevious:
                    time.sleep(5)
                    return self.getAnnotation(site, expand, True)
                else:
                    print("Got bad status line trying to pull up " + fullURL)
                    print("Response: " + str(error))
                    return "Unable to get annotation due to BadStatusCode error.  Matching " + args.sequence
            gene = False
            for item in ensembl:
                if item['description']:  #check if a gene is listed for the site, if not, check the next one.  If we get to the end and find no gene, then we return no gene.  Sometimes ensembl returns a result with no gene listed, followed by a second annotation listing the gene.
                    gene = item['description']
            return gene

    def annotateResults(self):
        for i in range(0,len(self.matches[0])):  #only look for precise sites with our perfet matches, everything else we can just run the expanded set
            self.matches[0][i].gene = self.getAnnotation(self.matches[0][i])
        for key in list(self.matches.keys()):
            for i in range(0,len(self.matches[key])):
                if not self.matches[key][i].gene:
                    self.matches[key][i].gene = self.getAnnotation(self.matches[key][i], args.annotationExpansion)
                    
    def applyElevationScoresOld(self, intendedTarget):
        for key in list(matches.keys()):
            offTargetSequences = []
            for line in self.matches[key]:
                offTargetSequences.append(line.matchSeq.replace("_",""))
            if offTargetSequences:
                elevationScoreList = calculateElevationScoreLocal(intendedTarget.replace("_",""), offTargetSequences)
                for j in range(0, len(elevationScoreList)):
                    self.matches[key][j].elevationScore = elevationScoreList[j][0]
                    self.matches[key][j].stackerScore = elevationScoreList[j][1]
                    self.matches[key][j].score = elevationScoreList[j][0]
                    
    def applyElevationScores(self, intendedTarget):
        offTargetSequences = []
        for i in range(0, len(self.matches)):
            for line in self.matches[i]:
                offTargetSequences.append(line.matchSeq.replace("_",""))
        if offTargetSequences:
            elevationScoreList = calculateElevationScoreLocal(intendedTarget.replace("_",""), offTargetSequences)
            for i in range(0, len(self.matches)):
                for j in range(0, len(self.matches[i])):
                    siteScore = elevationScoreList.pop(0)
                    self.matches[i][j].elevationScore = siteScore[0]
                    self.matches[i][j].stackerScore = siteScore[1]
                    self.matches[i][j].score = siteScore[0]
            if elevationScoreList:
                print("Elevation score list should have been depleted, but was not.  There were %s sites left." % (len(elevationScoreList)))
                raise RuntimeError("Elevation score list had items remaining: " + len(elevationScoreList))
    
    def calculateAggregatedScore(self):
        import predictionCaller
        elevationScoreList = []
        stackerScoreList = []
        genicScoreList = []
        for i in range(0, len(self.matches)):
            skip = -1  #value we won't hit while iterating, but still need to check.  Mostly here for handling multiple perfect match situations
            if i == 0:
                if len(self.matches[i]) <= 1:
                    continue
                else:  #multiple perfect match situation
                    skip = 0
                    for j in range(0, len(self.matches[i])):
                        if self.matches[i][j].gene:
                            skip = j
            for j in range(0, len(self.matches[i])):
                if j == skip:  #trap for when we need to skip a value
                    continue
                elevationScoreList.append(self.matches[i][j].elevationScore)
                stackerScoreList.append(self.matches[i][j].stackerScore)
                if self.matches[i][j].gene:
                    genicScoreList.append(True)
                else:
                    genicScoreList.append(False)
        result = predictionCaller.run("aggregation", stackerScoreList, elevationScoreList, genicScoreList)
        return result[0]
        
    def reportResults(self):
        if self.tooManyMismatches:
            print("Too many mismatches (more than %s)" %(args.matchSiteCutoff))
        else:
            if self.aggregateOffTargetScore or type(self.aggregateOffTargetScore) != bool:
                print("Aggregate mismatch risk: %s" %(self.aggregateOffTargetScore))
            for i in range(0, len(self.matches)):
                print("Mismatches: " + str(i) + " (" + str(len(self.matches[i])) + ")")
                for line in self.matches[i]:
                    print("\t" + str(line))
                    if args.quickExtend:
                        print("\tExtended site: " + line.extendedMatchSeq)
                        
    def outputToFile(self):
        print("Writing results to file %s" %(args.outputToFile))
        outputFile = open(args.outputToFile, 'w')
        if self.tooManyMismatches:
            print(args.sequence, file = outputFile)
            print("\tToo many mismatches (more than %s)" %(args.matchSiteCutoff), file = outputFile)
        else:
            print(args.sequence, file = outputFile)
            for i in range(0, len(self.matches)):
                if self.aggregateOffTargetScore or type(self.aggregateOffTargetScore) != bool:
                    print("Aggregate mismatch risk: %s" %(self.aggregateOffTargetScore), file = outputFile)
                print("\tMismatches: " + str(i) + " (" + str(len(self.matches[i])) + ")", file = outputFile)
                for line in self.matches[i]:
                    print("\t\t" + str(line), file = outputFile)
                    if args.quickExtend:
                        print("\t\tExtended site: " + line.extendedMatchSeq, file = outputFile)
        outputFile.close()
                    
    def createGuideAnalysisDictOld(self):
        print("Formatting data for Azure table")
        import json
        import operator
        guideAnalysisDict = {}
        guideAnalysisDict["target"] = args.sequence.replace("_","")
        guideAnalysisDict["azimuth"] = self.azimuthScore
        guideAnalysisDict["aggregatedOffTarget"] = self.aggregateOffTargetScore
        mismatchLists = [[]]
        mismatchListNumber = 0
        mismatchListCounter = 0
        #print(self.tooManyMismatches)
        if not self.tooManyMismatches:
            for i in range(1, len(self.matches)):
                self.matches[i].sort(key = operator.attrgetter("elevationScore"), reverse = True)        
            for i in range(1, len(self.matches)):   #starting off at 1, since anything in index 0 is a perfect match
                for line in self.matches[i]:
                    if mismatchListCounter >= 100:
                        mismatchLists.append([])
                        mismatchListCounter = 0
                        mismatchListNumber += 1
                    mismatchLists[mismatchListNumber].append(line.azureTableMismatchData())
                    mismatchListCounter += 1
            for i in range(0,mismatchListNumber + 1):
                guideAnalysisDict["offTargets" + str(i)] = json.dumps(mismatchLists[i])
            guideAnalysisDict["mismatchListCount"] = len(mismatchLists)
            #mismatchList.sort(key = operator.itemgetter(3), reverse = True)
            #guideAnalysisDict["offTargets"] = zlib.compress(json.dumps(mismatchList).encode(),9)
            #guideAnalysisDict["geneElevation"], guideAnalysisDict["nongeneElevation"] = self.calculateGeneAndNongeneElevation(mismatchLists)
        else:
            print("Too many mismatches for this site (greater than %s)" %(args.matchSiteCutoff))
        guideAnalysisDict["tooManyMismatches"] = self.tooManyMismatches
        guideAnalysisDict["beforeAltStart"] = args.beforeAltStart
        guideAnalysisDict["lastExon"] = args.lastExon
        return guideAnalysisDict
    
    def createGuideAnalysisDict(self, reportedMismatchLimit = 5000):
        print("Formatting data for Azure table")
        import json
        import operator
        guideAnalysisDict = {}
        guideAnalysisDict["target"] = args.sequence.replace("_","")
        guideAnalysisDict["azimuth"] = self.azimuthScore
        guideAnalysisDict["aggregatedOffTarget"] = self.aggregateOffTargetScore
        assumedIntendedTarget = []
        mismatchLists = [[]]
        mismatchListNumber = 0
        mismatchListCounter = 0
        #print(self.tooManyMismatches)
        if not self.tooManyMismatches:
            multiplePerfectMatches = False
            multiplePerfectGenicMatches = False
            if len(self.matches[0]) == 0:
                assumedIntendedTarget = []  #not actually doing anything of import, but a place holder for organization
            elif len(self.matches[0]) == 1:
                assumedIntendedTarget = self.matches[0][0].azureTableMismatchData()
            else:
                multiplePerfectMatches = True
            if multiplePerfectMatches:
                start = 0
                skip = 0
                genicPerfectMatches = []
                for i in range(0, len(self.matches[0])):
                    if self.matches[0][i].gene:
                        genicPerfectMatches.append(i)
                if len(genicPerfectMatches) > 1:
                    multiplePerfectGenicMatches = True
                if genicPerfectMatches:
                    skip = genicPerfectMatches[0]  #this will either set it to the first (and hopefully only) genic match, or leave it as the first element if there were none
                assumedIntendedTarget = self.matches[0][skip].azureTableMismatchData()
            else:
                start = 1
            fullMismatchList = []
            for i in range(start, len(self.matches)):
                for j in range(0, len(self.matches[i])):
                    if i == 0 and j == skip:
                        continue
                    fullMismatchList.append(self.matches[i][j])
            guideAnalysisDict["mismatchSiteCount"] = len(fullMismatchList)
            guideAnalysisDict["truncatedSiteList"] = len(fullMismatchList) > reportedMismatchLimit
            if fullMismatchList:
                fullMismatchList.sort(key = operator.attrgetter("elevationScore"), reverse = True)
            for line in fullMismatchList[0:reportedMismatchLimit]:
                if mismatchListCounter >= 100:
                    mismatchLists.append([])
                    mismatchListCounter = 0
                    mismatchListNumber += 1
                mismatchLists[mismatchListNumber].append(line.azureTableMismatchData())
                mismatchListCounter += 1
            for i in range(0,mismatchListNumber + 1):
                guideAnalysisDict["offTargets" + str(i)] = json.dumps(mismatchLists[i])
            guideAnalysisDict["mismatchListCount"] = len(mismatchLists)
            guideAnalysisDict["multiplePerfectMatches"] = multiplePerfectMatches
            guideAnalysisDict["multiplePerfectGenicMatches"] = multiplePerfectGenicMatches
            guideAnalysisDict["assumedIntendedTarget"] = json.dumps(assumedIntendedTarget)
            #mismatchList.sort(key = operator.itemgetter(3), reverse = True)
            #guideAnalysisDict["offTargets"] = zlib.compress(json.dumps(mismatchList).encode(),9)
            #guideAnalysisDict["geneElevation"], guideAnalysisDict["nongeneElevation"] = self.calculateGeneAndNongeneElevation(mismatchLists)
        else:
            print("Too many mismatches for this site (greater than %s)" %(args.matchSiteCutoff))
        guideAnalysisDict["tooManyMismatches"] = self.tooManyMismatches
        guideAnalysisDict["beforeAltStart"] = args.beforeAltStart
        guideAnalysisDict["lastExon"] = args.lastExon
        return guideAnalysisDict
    
    def calculateGeneAndNongeneElevation(self, mismatchLists):
        geneElevation = 0
        nongeneElevation = 0
        for sublist in mismatchLists:        
            for line in sublist:
                if line[2] == "NoGene" and not self.tooManyMismatches:  #if we have several mismatches, we will not annotate for genes and add all sites to genic value
                    nongeneElevation += line[3]
                else:
                    geneElevation += line[3]
        return (geneElevation, nongeneElevation)   
    
    def reportToDirectory(self):
        import pickle
        print("Starting reporter function.")
        print("Reporting to directory.")
        outputData = {}
        outputData['sequence'] = args.sequence
        outputData['matches'] = self.matches
        outputData['azimuthScore'] = self.azimuthScore
        outputData['multiplePerfectMatches'] = self.multiplePerfectMatches
        outputData['aggregatedOffTarget'] = self.aggregateOffTargetScore
        print(self.matches)
        print(args.sequence)
        print("Starting pickle")
        outputFile = open(args.outputDirectory + "/result/" + args.sequence, 'wb')
        pickle.dump(outputData, outputFile)
        outputFile.close()
        print("Pickle done.")
        clockOut = open(args.outputDirectory + "/completed/" + args.sequence, 'w')
        clockOut.close()
        print("Clocked out.")
        
    def reportToAzureTable(self):
        import time
        import sys
        print("Connecting to Azure tables for output")
        import azure.storage.table
        try:
            tableAccountKeyFile = open('azureTable.apikey','r')
        except FileNotFoundError:
            raise RuntimeError("Unable to find the key to the azure table in azureTable.apikey (file was absent)")
        tableAccountkey = tableAccountKeyFile.read().strip()
        tableAccountKeyFile.close()
        self.guideAnalysisDict = self.createGuideAnalysisDict()
        self.guideAnalysisDict["PartitionKey"] = args.partitionKey
        self.guideAnalysisDict["RowKey"] = args.rowKey
        #print(self.guideAnalysisDict)
        print("Writing data to Azure table")
        failures = 0
        tableHandle = False #initializing this so I can check it in the loop.  If the 
        while failures <= 10:
            try:
                if not tableHandle:
                    tableHandle = azure.storage.table.TableService(account_name=args.azureTableAccountName, account_key=tableAccountkey)
                tableHandle.insert_entity(args.azureTableName, self.guideAnalysisDict)
                break
            except azure.common.AzureConflictHttpError:
                print("Unable to report data to azure, as it has already been reported.", file = sys.stderr)
                sys.exit(42)  #Exit code indicating a good run with an already reported site.
            except:  #catching all exceptions here and just retrying
                time.sleep(5)
                failures += 1
        if failures > 10:
            tableHandle.insert_entity(args.azureTableName, self.guideAnalysisDict)  #this will try one more write (if it works, that's cool) to generate the appropriate error messages for tracing
        #self.getBackDataFromAzureTable(tableHandle)
        
    def getBackDataFromAzureTable(self, tableHandle):
        print("Getting results back from Azure")
        results = tableHandle.get_entity(args.azureTableName, args.partitionKey, args.rowKey)
        print(results)       
                
    def cleanup(self):
        import shutil
        shutil.rmtree(self.tempDir)
        
    def createMatchTable(self):
        matchTable = {}
        for i in range(0, args.mismatchTolerance+1):
            matchTable[i] = []
        return matchTable
    
    def createColorScheme(self):
        colorScheme = []
        colors = args.mismatchTolerance + 1 + args.canonicalPAMMismatchRangeExtension + args.endClip
        if colors > 7:
            increments = 8
            step = 255//8
        elif colors == 0:
            return ["0,0,0"]
        else:
            increments = colors
            step = 255//increments
        for i in range(0,increments + 1):
            if i < 8:
                red = 255 - (step*i)
                green = 0
                blue = 0 + step*i
                colorScheme.append(str(red) + "," + str(green) + "," + str(blue))
            else:
                colorScheme.append(str(red) + ",0," + str(blue))
        return colorScheme
    
class TreeNavigator(object):
    
    def __init__(self, treeFileName, sequence):
        self.treeFile = open(treeFileName, 'rb')
        self.sequence = sequence
        self.checkTreeLevel1()
        
    def checkTreeLevel1(self):
        import pickle
        self.treeFile.seek(0)
        level1Shortcut = int.from_bytes(self.treeFile.read(8), "little")
        self.treeFile.seek(level1Shortcut)
        level1 = pickle.load(self.treeFile)
        seeds = list(level1.keys())
        seeds.sort()
        seedLength = len(seeds[0])
        revSeq = self.sequence[::-1]
        sequenceSeed = revSeq[:seedLength]
        self.qualifiedLevel1 = []
        progress = 0
        qualified = 0
        for seed in seeds:
            print("Qualified %s of %s level 1 seeds." %(qualified, progress), end = "\r")
            progress += 1
            mismatches = 0
            for i in range(0, seedLength):
                if seed[i] == sequenceSeed[i]:
                    continue
                else:
                    mismatches += 1
                    if mismatches > args.mismatchTolerance:
                        break
            if mismatches <= args.mismatchTolerance:
                self.qualifiedLevel1.append((seed, level1[seed], mismatches))
                qualified += 1
        print()
    
    def getNextLevel2(self):
        import pickle
        if not self.qualifiedLevel1:
            return False
        seed1, fileReadSite, level1Mismatches = self.qualifiedLevel1[0]
        self.treeFile.seek(fileReadSite)
        level2 = pickle.load(self.treeFile)
        level2Seeds = list(level2.keys())
        level2Seeds.sort()
        seed2Length = len(level2Seeds[0])
        revSeq = self.sequence[::-1]
        sequenceSeed = revSeq[len(seed1):len(seed1) + seed2Length]
        self.qualifiedLevel2 = []
        for seed in level2Seeds:
            mismatches = level1Mismatches
            for i in range(0, seed2Length):
                if seed[i] == sequenceSeed[i]:
                    continue
                else:
                    mismatches += 1
                    if mismatches > args.mismatchTolerance:
                        break
            if mismatches <= args.mismatchTolerance:
                self.qualifiedLevel2.append(level2[seed])
        del self.qualifiedLevel1[0]
        if not self.qualifiedLevel2:
            return self.getNextLevel2()  #this will recurse until we get a level1 that has qualified level2s to return or we hit the end of the list and it returns false
        self.level2Groomer()
        return (seed1, self.qualifiedLevel2)
    
    def level2Groomer(self):
        index = 0
        while index < len(self.qualifiedLevel2) - 1:  #need to minus 1 since we don't want to index all the way to the last element
            currentStart, currentReadBytes = self.qualifiedLevel2[index]
            nextStart, nextReadBytes = self.qualifiedLevel2[index + 1]
            if currentStart + currentReadBytes == nextStart:
                del self.qualifiedLevel2[index + 1]
                self.qualifiedLevel2[index] = (currentStart, currentReadBytes + nextReadBytes)
            else:
                index += 1
        
                
class WorkerJob(object):
    
    def __init__(self, fileList = False):
        if not fileList:
            self.fileList = self.getJobList()
        else:
            self.fileList = fileList
        self.matchTable = self.createMatchTable()
        self.pam, self.guide = args.sequence[::-1].split("_")
        self.colorScheme = self.createColorScheme()
        print("Matching")
        self.checkAllSequences()
        print("Worker job reporting results")
        self.reportResult()

    def createMatchTable(self):
        matchTable = {}
        for i in range(0,args.mismatchTolerance+1):
            matchTable[i] = []
        return matchTable
        
    def getJobList(self):
        import pickle
        inputFile = open(args.tempDir + "/mission" + args.workerID, "rb")
        jobList = pickle.load(inputFile)
        inputFile.close()
        return jobList
        
    def createColorScheme(self):
        colorScheme = []
        if args.mismatchTolerance > 7:
            increments = 8
        elif args.mismatchTolerance == 0:
            return ["0,0,0"]
        else:
            increments = args.mismatchTolerance
            step = 255//increments
        for i in range(0,increments + 1):
            if i < 8:
                red = 255 - (step*i)
                green = 0
                blue = 0 + step*i
                colorScheme.append(str(red) + "," + str(green) + "," + str(blue))
            else:
                colorScheme.append(str(red) + ",0," + str(blue))
        return colorScheme
        
    def checkAllSequences(self):  #original method
        progress = 0
        allFiles = []
        if args.delayIO and standAloneDefaultSelectionModeParallelJobLimit > 1:
            import random
            import time
            randomBreak = random.uniform(0, standAloneDefaultSelectionModeParallelJobLimit)
            print("Delaying reads by " + str(randomBreak) + " seconds.")
            time.sleep(randomBreak)
        for fileData in self.fileList:
            print("Read " + str(progress) + " of " + str(len(self.fileList)) + " files.           ", end = "\r")
            progress += 1
            fileName, binMismatches, startIndex = fileData.split(":")  #the last two values will come in as strings, but need to be used as ints
            binMismatches = int(binMismatches)
            startIndex = int(startIndex)
            file = open(args.inputDirectory + "/" + fileName, 'r')
            wholeFile = file.read()
            file.close()
            lines = wholeFile.split("\n")
            for line in lines:
                allFiles.append([line, int(binMismatches)])
        print("All files read.                                      ")
        progress = 0
        totalLines = len(allFiles)
        totalMatchSiteCount = 0
        for lineMismatchCombo in allFiles:
            if lineMismatchCombo[0]:
                line = lineMismatchCombo[0]
                mismatches = lineMismatchCombo[1] #initialize this counter to however many mismatches we got during our tree search
                if line.count("\t") == 5:
                    chrom, begin, end, extendedSeq, score, strand = line.split("\t")
                elif line.count("\t") == 4:
                    chrom, begin, end, extendedSeq, strand = line.split("\t")
                else:
                    raise RuntimeError("Got an inappropriate number of tabs on this line: " + line)
                refSeq, beforeStart, afterPam = extendedSeq.split("/")
                pam, guide = refSeq.split("_")
                for i in range(startIndex,len(self.guide) - args.endClip):
                    try:
                        if guide[i] != self.guide[i]:
                            mismatches += 1
                            if mismatches > args.mismatchTolerance:
                                break
                    except IndexError:
                        raise RuntimeError("ABORTED: Encountered an error reading " + fileName + " where we got an error comparing input sequence " + self.guide + " to " + guide + ".  This could be due to a corrupted, shortened sequence in the data file, or a bug in the program.")
                    #extendedRefGuide = beforeStart + guide[::-1]
                    #extendedGuide = extendedRefGuide[-(len(beforeStart) + len(self.guide))]
                    #extendedPam = pam[::-1] + afterPam
                    extendedSiteSeq = compileExtendedSeq(refSeq, beforeStart, afterPam)
                    if i == len(self.guide) - 1 - args.endClip:
                        mismatchSites = []  #find the position in the guide of all mismatches, indexed to the base right before the PAM being [0]
                        for j in range(0,len(self.guide)):
                            if guide[j] != self.guide[j]:
                                mismatchSites.append(j)
                                if len(mismatchSites) == mismatches:  #once we have a number of mismatch index values equal to our number of mismatches, we can stop
                                    break                            
                        matchGuide = guide[:len(guide)]
                        matchGuide = matchGuide[::-1]
                        matchSeq = matchGuide + pam[::-1]
                        matchSeqExtended = matchSeq
                        guideDiff = len(guide) - len(self.guide) #accounting for a longer guide sequence in the stored reference
                        if guideDiff != 0:
                            matchSeq = matchSeq[guideDiff:]
                            if strand == "+":
                                begin = str(int(begin) + guideDiff)
                            if strand == "-":
                                end = str(int(end) - guideDiff)
                        self.matchTable[mismatches].append(MatchSite(chrom, begin, end, matchSeq, str(1000*((len(guide)-mismatches)/len(guide))), strand, self.colorScheme[mismatches], mismatches, extendedSiteSeq, mismatchSites))
                        totalMatchSiteCount += 1
                        if totalMatchSiteCount > args.matchSiteCutoff:
                            self.matchTable = -1
                            return "Aborted due to count"
                        if args.verbose:
                            print("\nFound Match")
                progress += 1
                if progress % 10000 == 0 and (args.verbose or args.workerID == "0"):
                    print("Processed " + str(progress) + " of " + str(totalLines) + " lines.            ", end = "\r")
        print("Processed " + str(progress) + " lines.                     ")

                            
    def reportResult(self):
        return self.matchTable


#===================================================FASTA indexing objects.  Requires a FASTA and FAI as input and will output a directory containing a list of targets for the system from the genome.=======================

class FASTAIndexLine(object):
    
    def __init__(self, line):
    # read from start to length + (length // 50) + start
        import re
        line = line.split("\t")
        line[0] = re.sub(r'chr','',line[0])
        self.contig = line[0]
        self.length = int(line[1])
        self.start = int(line[2])
        self.lineBases = int(line[3])
        self.lineBytes = int(line[4])
        self.end = self.length + ((self.lineBytes-self.lineBases)*(self.length // self.lineBases)) #this accounts for the fact that length is counted in bases and not bytes, and missed all the newline bytes that terminate each line
        self.endpoint = self.length + ((self.lineBytes-self.lineBases)*(self.length // self.lineBases)) + self.start

class ParallelIndexJob(object):
    
    def __init__(self, contig, start, end, workerID):
        self.contig = contig
        self.start = start
        self.end = end
        self.workerID = workerID
        self.jobName =  str(contig) + "." + str(workerID)
        self.chunkStartBase = 0
        
    def __str__(self):
        return str(self.contig) + "." + str(self.workerID)

class FASTASupervisor(object):
    
    def __init__(self):
        import os
        import dataPacker
        self.encoder = dataPacker.DataPacker()
        printStartUp()
        reportUsage("INDEX")
        if not self.isAnEnsemblSpecies(args.species):  #make sure that the species they entered is one that is annotated, or make them set an option to ignore this
            if not args.clobber:
                raise RuntimeError("ABORTED: " + args.species.upper() + " is not a valid ensembl species.  Please check your naming of this species.  If this is known not to be an ensembl species, rerun with clobber mode on (argument '-9') to ignore this issue.")
        redundantGenome = self.suitableIndexedGenomeExists()
        if redundantGenome:
            if not args.clobber:
                seq, genome, species = redundantGenome.split(".")
                print("Suitable indexed genome already exists.  Indexed genome info:")
                print("Sequence " + seq[::-1])
                print("  Genome " + genome)
                if not args.directToCompiler:
                    raise RuntimeError("ABORTED: Suitable genome exists.  Please delete existing one (or run in clobber mode, not recommended).")
                else:
                    if not args.recreateTree:
                        print("Attempting to compile directly.")
                    else:
                        print("Attempting to recreate saved tree structure.")
        self.countFileName = args.genomeListDirectory + "genomeData/" + args.sequence[::-1].upper() + "." + args.genome.upper() + "." + args.species.upper()
        if not args.directToCompiler and os.path.isfile(self.countFileName + ".gather"): #checking for an existing gather file and deleting it if it exists
            os.remove(self.countFileName + ".gather")
        if not args.directToCompiler and os.path.isfile(self.countFileName):  #and removing an existing countfile as well
            os.remove(self.countFileName)
        if args.directToCompiler and not redundantGenome:
            raise RuntimeError("ABORTED: Unable to find the genome for going direct to bin compilation.")
        if redundantGenome and not args.directToCompiler:
            import shutil
            shutil.rmtree(args.genomeListDirectory + redundantGenome)
        self.getFiles(args.inputfile)
        self.createTempDir()
        self.outputDirectory = self.createOutputDir()
        if not args.directToCompiler:
            if args.ordered:
                self.faiJobs()
            else:
                self.createParallelJobs()
                self.encodingScheme = self.getEncodingScheme()
                self.saveGenCodeData()
                self.assignParallelJobs()
                try:
                    self.monitorJobs()
                except KeyboardInterrupt:
                    if yesAnswer("\nJob monitoring interrupted.  Continue without finishing? (No to quit)"):
                        pass
                    else:
                        quit("Monitoring of jobs was interrupted.")
                if args.standAlone:
                    self.runJobQueue()
                #self.gatherCounts()
        if not args.recreateTree:
            self.runBinCompiler()
        self.createTreePickle()
        if not args.noCleanup:
            self.cleanup()
    
    def suitableIndexedGenomeExists(self):
        import os
        if not os.path.isdir(args.genomeListDirectory):
            return False
        seqPam, seqGuide = args.sequence[::-1].split("_")
        directoryContents = os.listdir(args.genomeListDirectory)
        for item in directoryContents:
            if not item[0] == "." and "." in item and "_" in item and "NNN" in item:
                try:
                    itemSeq, itemGenome, itemSpecies = item.split(".")
                except ValueError:
                    continue
                if itemGenome == args.genome:
                    if args.species.upper() != itemSpecies:  #If someone is trying to index a genome as being from a different species than an already annotated genome of the same name, warn them and require them to set the clobber option to do it.  They really should not be doing that.
                        if not args.clobber:
                            raise RuntimeError("ABORTED: Warning: This exact genome has already been indexed as species " + itemSpecies + " it should not also be indexed as " + args.species.upper() + ".  If you wish to actually have this situation (not recommended), please set the clobber option in arguments (argument '-9').")
                    itemPam, itemGuide = itemSeq.split("_")
                    if seqPam == itemPam and len(seqGuide) <= len(itemGuide):
                        return item
        return False
    
    def isAnEnsemblSpecies(self, species):
        import urllib.request
        url = 'http://rest.ensembl.org/overlap/region/' + species.lower() + '/1:1000000-1000001?feature=gene'
        try:
            ensembl = urllib.request.urlopen(url)
            ensembl = ensembl.read().decode('utf-8')
            if "Can not find internal name for species" in ensembl:
                return False
        except urllib.error.HTTPError as error:
            message = error.read().decode('utf-8')
            if "Can not find internal name for species" in message:
                return False
            else:
                return True
        except urllib.error.URLError:
            print("Unable to reach/find ensembl server.  Please confirm you are connected to the internet.")
            return True
        return True
    
    def getFiles(self, fastaName):
        try:
            self.fasta = open(fastaName)
            firstLine = self.fasta.readline()
            if not ">" in firstLine:
                raise RuntimeError("ABORTED: " + fastaName + " does not appear to be a properly formatted FASTA file.  Please check to be sure that it follows FASTA standards.")
            self.fasta.close()
        except FileNotFoundError:
            raise RuntimeError("ABORTED: " + fastaName + " was not found.  This file was passed as the reference genome.")
        try:
            self.fai = open(fastaName + ".fai",'r')
        except FileNotFoundError:
            try:
                self.fai = open(fastaName[:-4] + ".fai", 'r')
            except FileNotFoundError:
                raise RuntimeError("ABORTED: No FASTA index (.fai) file could be found for " + fastaName + " please run a FASTA indexer and try again.")
    
    def createOutputDir(self):
        import os
        if not os.path.isdir(args.genomeListDirectory):
            os.mkdir(args.genomeListDirectory)
        if not os.path.isdir(args.genomeListDirectory + os.sep + "genomeData"):
            os.mkdir(args.genomeListDirectory + os.sep + "genomeData")
        outputDirectory = args.genomeListDirectory + os.sep + args.sequence[::-1] + "." + args.genome + "." + args.species
        if not args.directToCompiler:
            if os.path.isdir(outputDirectory) and not args.clobber:
                raise RuntimeError("ABORTED: This genome/system combination has already been indexed.")
            else:
                os.mkdir(outputDirectory)
        return outputDirectory        
    
    def faiJobs(self):
        contigJobs = []
        rawLine = self.fai.readline()
        while rawLine:
            line = FASTAIndexLine(rawLine)
            contigJobs.append(line)
            rawLine = self.fai.readline()
        for job in contigJobs[1:]:
            self.createJobBash(job)
            self.submitJob(job)
        myJob = contigJobs[0]
        args.chromosome = myJob.contig
        args.start = str(myJob.start)
        args.length = str(myJob.end)
        myRun = FASTAreader()
        print("Completed this job.  Parallel jobs may still be running.")
        
    def createParallelJobs(self):
        contigData = []
        self.fai.seek(0)
        rawLine = self.fai.readline()
        while rawLine:
            line = FASTAIndexLine(rawLine)
            contigData.append(line)
            rawLine = self.fai.readline()
        self.contigList = []
        for line in contigData:
            self.contigList.append(str(line.contig))
        self.enumerateContigs()
        #if len(self.contigList) > args.maxParallelJobs:
        #    raise RuntimeError("ABORTED: Run cannot proceed with more contigs than allowed parallel jobs.  If you are using a genome version with large numbers of alternate assemblies, you should remove the corresponding lines from your FASTA index file.")
        parallelJobs = []
        windowLength = len(args.sequence) - 1  #the minus 1 accounts for the underscore separating the guide and pam
        for line in contigData:
            chunkSize = args.chunkSize
            chunkNumber = 0
            contigFinished = False
            contigStartByte = line.start
            contigEndByte = line.endpoint
            while not contigFinished:
                contig = line.contig
                start = contigStartByte + (chunkSize * chunkNumber)
                end = chunkSize + start
                if end >= contigEndByte:
                    contigFinished = True
                    readLength = contigEndByte - start
                    chunkNumber += 1
                else:
                    readLength = chunkSize + windowLength -1  #this will read windowLength - 1 bytes into the next chunk.  This means that the last window of this chunk will be one byte before the first windw of the next one
                    chunkNumber += 1
                parallelJobs.append(ParallelIndexJob(contig, start, readLength, chunkNumber))
        self.parallelJobs = parallelJobs
        
    def enumerateContigs(self):
        enumeratedContigs = enumerate(self.contigList)
        self.contigEnumeration = {}
        self.contigDenumeration = {}
        for item in enumeratedContigs:
            self.contigEnumeration[item[1]] = item[0]
            self.contigDenumeration[item[0]] = item[1]
        contigCount = len(self.contigList)
        self.contigByteLength = self.encoder.calculateByteLength(contigCount)
    
    def contigDataAsArgument(self, contig):  # if chromosome 5 corresponds to enumeration 6 and we are using a single byte for encoding, we would expect to get back "B6"
        return str(self.contigByteLength) + "," + str(self.contigEnumeration[contig])
    
    def getEncodingScheme(self):
        return self.encoder.getPackingPattern(self.contigByteLength, positionByteLength, args.sequence[::-1], args.guideExtension, args.pamExtension)

    def saveGenCodeData(self):
        import pickle
        import os
        guide, pam = args.sequence.split("_")
        encodingData = EncodingData(args.treeLevel1, args.treeLevel2, len(guide), len(pam), args.guideExtension, args.pamExtension, self.encodingScheme, self.contigEnumeration, self.contigDenumeration)
        genCodeFile = open(self.outputDirectory + os.sep + "genCodeData.pkl", 'wb')
        pickle.dump(encodingData, genCodeFile)
        genCodeFile.close()
   
    def assignParallelJobs(self):    
        import pickle
        import os
        if not args.forceJobIndex:
            self.myJobIndex = len(self.parallelJobs) // 2  #making this instance take the job in the middle so that it less likely to be running through a string of pure "N"s
        else:
            self.myJobIndex = int(args.forceJobIndex)
        jobArray =["Place holder for zeroth job"]
        for i in range(0,len(self.parallelJobs)):
            if i != self.myJobIndex:
                jobArray.append(self.createJobBash(self.parallelJobs[i],self.parallelJobs[i].workerID))
                #self.submitJob(self.parallelJobs[i],self.parallelJobs[i].workerID)
        self.arrayJobCount = len(jobArray)
        jobArrayFile = open(self.tempDir + os.sep + "fastaSearch" + os.sep + "jobs.pkl", 'wb')
        pickle.dump(jobArray, jobArrayFile)
        jobArrayFile.close()
        self.submitArrayJob(len(jobArray), "NFIndexer")
        myJob = self.parallelJobs[self.myJobIndex]
        args.chromosome = self.contigDataAsArgument(myJob.contig)
        args.start = str(myJob.start)
        args.length = str(myJob.end)
        args.workerID = str(myJob.workerID)
        args.enumeratedContig = self.contigDataAsArgument(myJob.contig)
        self.myRun = FASTAreader()
        print("Completed this job. Checking/monitoring other parallel jobs.")
    
    def submitArrayJob(self, jobArrayLength, jobName):
        import os
        jobRange = " 1-" + str(jobArrayLength - 1) + " "
        command = "echo \"" + pythonInterpreterAbsolutePath + " arrayWrapper.py -d " + self.tempDir +  os.sep + "fastaSearch\" | qsub -cwd -V -N " + jobName + " -l h_data=4G,time=23:59:00 -e " + os.getcwd() +  "/schedulerOutput/ -o " + os.getcwd() + "/schedulerOutput/ -M mweinste@ucla.edu -m a " + "-t " + jobRange
        success = False
        if not args.mock:
            print("Submitting: %s" %(command))
            for i in range(0,10):
                status = os.system(command)
                success = status == 0
                if success:
                    break
            if not success:
                raise RuntimeError("Failed to submit job to scheduler.  Please check the status of the scheduler.")
        else:
            print("Mock submit: " + command)
        
    def runJobQueue(self):   #keeping this around for standalone mode
        import os
        import time
        import datetime
        startTime = datetime.datetime.now()
        jobList = {'queued':[],'running':[],'complete':[]}
        maxSimultaneousJobs = args.maxParallelJobs #no further calculation is needed here, since FASTAworkers don't launch subprocesses like search managers do
        print("Allowing only " + str(maxSimultaneousJobs) + " running jobs at once.")
        jobList['queued'] = self.parallelJobs
        while jobList['queued'] or jobList['running']:
            try:
                while jobList['queued'] and len(jobList['running']) < maxSimultaneousJobs:
                    self.createJobBash(jobList['queued'][0],jobList['queued'][0].workerID)
                    self.submitJob(jobList['queued'][0],jobList['queued'][0].workerID)
                    jobList['running'].append(jobList['queued'][0])
                    del jobList['queued'][0]
                while len(jobList['running']) >= maxSimultaneousJobs or len(jobList['queued']) == 0:
                    newlyCompleted = []
                    for i in range(0, len(jobList['running'])):
                        if args.ordered:
                            touchFileName = jobList['running'].contig
                        else:
                            touchFileName = jobList['running'][i].contig + "." + str(jobList['running'][i].workerID)
                        if os.path.isfile(self.tempDir + "/completed/" + touchFileName):
                            newlyCompleted.append(i)
                    newlyCompleted.sort(reverse = True)
                    if newlyCompleted:
                        for completedIndex in newlyCompleted:
                            jobList['complete'].append(jobList['running'][completedIndex])
                            del jobList['running'][completedIndex]
                    if not jobList['running'] and not jobList['queued']:
                        break
                    time.sleep(10)
            except KeyboardInterrupt:
                for key in list(jobList.keys()):
                    print(key)
                    for item in jobList[key]:
                        print("\t" + item.jobName)
                    if yesAnswer("Continue with run?"):
                        continue
                    else:
                        raise RuntimeError("ABORTED: By your command.")
        runTime = datetime.datetime.now() - startTime
        print ("Parallel index completed in " + (str(runTime)))
        
    def calculateRAM(contigSize):
        pass  #skipping this method, as it seems like everything can run with 2G or less
    
    def createTempDir(self):
        import re
        import os
        import datetime
        successful = False
        while not successful:
            currenttime = datetime.datetime.now()
            currenttime = str(currenttime)
            currenttime = re.sub(r'\W','',currenttime)
            self.tempDir = args.scratchFolder + '.indexJob' + currenttime
            args.tempDir = self.tempDir
            if os.path.isdir(self.tempDir):
                continue
            try:
                os.mkdir(self.tempDir)
            except OSError:
                continue
            successful = True
        os.mkdir(self.tempDir + "/fastaSearch")
        os.mkdir(self.tempDir + "/completed")
        os.mkdir(self.tempDir + "/progress")
        os.mkdir(self.tempDir + "/compilerBash")
        os.mkdir(self.tempDir + "/compiled")
        return True
    
    def createJobBash(self, job, workerID = False):
        import os
        if args.forcePamList:
            forcePamListArg = " --forcePamList " + args.forcePamList
        return pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode FASTAWorker --workerID " + str(workerID) + " --enumeratedContig " + self.contigDataAsArgument(job.contig) + " --chromosome " + job.contig + " --start " + str(job.start) + " --length " + str(job.end) + " --sequence " + args.sequence + " --inputfile " + os.path.abspath(args.inputfile) + " --genome " + args.genome + " --tempDir " + args.tempDir + " --chunkSize " + str(args.chunkSize) + " --species " + args.species + " --treeLevel1 " + str(args.treeLevel1) + " --treeLevel2 " + str(args.treeLevel2) + " --cacheSize " + str(args.cacheSize) + " --guideExtension " + str(args.guideExtension) + " --pamExtension " + str(args.pamExtension) + " --genomeDirectory " + args.genomeListDirectory.replace(" ",'\ ') + forcePamListArg
    
    def monitorJobs(self):
        import time
        import os
        allDone = False
        while not allDone:
            dirList = os.listdir(self.tempDir + os.sep + "fastaSearch")
            #completedItems.append(str(args.chromosome + "." + str(args.workerID)))  #adding this instance's job to the completed job list
            completedJobs = []
            for file in dirList:
                if file.endswith(".done") and os.path.isfile(self.tempDir + os.sep + "fastaSearch" + os.sep + file):
                    completedJobs.append(int(file.split(".")[0]))
            incompleteJobCount = 0
            awaitedJobs = []
            for i in range(1, self.arrayJobCount):
                if not i in completedJobs:
                    incompleteJobCount += 1
                    awaitedJobs.append(i)
            if incompleteJobCount:
                if incompleteJobCount < 10:
                    print("Awaiting %s of %s array jobs.  Incomplete jobs: %s                                  " %(incompleteJobCount, self.arrayJobCount, ", ".join([str(awaitedJobNumber) for awaitedJobNumber in awaitedJobs])), end = "\r")
                else:
                    print("Awaiting %s of %s array jobs." %(incompleteJobCount, self.arrayJobCount), end = "\r")
            else:
                allDone = True
        print("All parallel jobs completed.  Compiling tree structures.                                               ")
        return True

    def gatherCounts(self):
        import re
        counts = {}
        alreadyCounted = {}
        for contig in self.contigList:
            counts[contig] = 0
            alreadyCounted[contig] = []
        gatherFile = open(self.countFileName +  ".gather", 'r')
        rawData = gatherFile.read()
        gatherFile.close()
        data = rawData.split("\n")
        for datum in data:
            if datum:
                contig, workerID, hitCount = datum.split("\t")
                if workerID in alreadyCounted[contig]:
                    continue #protection against unintentional double counting if the job was previously stopped and restarted
                else:
                    counts[contig] += int(hitCount)
                    alreadyCounted[contig].append(workerID)
        output = open(self.countFileName, 'w')
        for contig in self.contigList:
            output.write(contig + "\t" + str(counts[contig]) + "\n")
        output.close()
    
    def runBinCompiler(self):
        import os
        os.mkdir(self.outputDirectory + os.sep + "targets")
        os.mkdir(self.outputDirectory + os.sep + "binMaps")
        self.createBinCompilerJobs()
        self.runBinCompilerJobs()
        try:
            self.monitorCompilerJobs()
        except KeyboardInterrupt:
            if yesAnswer("\nJob monitoring interrupted.  Continue without finishing? (No to quit)"):
                pass
            else:
                quit("Job monitoring interrupted.")
    
    def createBinCompilerJobs(self):
        binCompilerParallelJobLimit = 300
        import os
        import pickle
        self.bigBinList = []
        for item in os.listdir(self.outputDirectory):
            if os.path.isdir(self.outputDirectory + os.sep + item) and item.endswith(".targetbin"):
                self.bigBinList.append(item.replace(".targetbin",""))
        if not self.bigBinList:
            raise RuntimeError("Quit with error.  Was expecting a list of bins to compile, but did not get one.")
        if binCompilerParallelJobLimit > len(self.bigBinList):
            binCompilerParallelJobLimit = len(self.bigBinList)
        # jobNumber = args.maxParallelJobs
        # if jobNumber < 1 or len(self.bigBinList) < jobNumber:
        # jobNumber = len(self.bigBinList)
        # jobList = []
        # for i in range(0,jobNumber):
        #     jobList.append([])
        # assignmentCounter = 0  #just initializing this value.  I can mod it by the jobNumber in the loop to know where to assign a bin
        # for bigBin in self.bigBinList:
        #     jobList[assignmentCounter % jobNumber].append(bigBin)
        #     assignmentCounter += 1
        # assignmentCounter = 0 #now using this to count job numbers
        commandLines = ["Zeroth Job Placeholder"]
        for i in range (0, binCompilerParallelJobLimit):
            commandLines.append([])
        assignmentCounter = 0
        for job in self.bigBinList:
            if not args.recreateTree:
                commandLines[(assignmentCounter % binCompilerParallelJobLimit) + 1].append(self.createBinCompilerBash(job))
            assignmentCounter += 1
        self.myJob = commandLines[1] #pulling off the first job for this node
        del commandLines[1]
        commandsFile = open(self.tempDir + "/compilerBash/jobs.pkl", 'wb')
        pickle.dump(commandLines, commandsFile)
        commandsFile.close()
        self.parallelCompileJobs = len(commandLines)
        self.binCompilerJobMatrix = {}
        for i in range(1, len(commandLines)):
            self.binCompilerJobMatrix[i] = {}
            for j in range(0, len(commandLines[i])):
                self.binCompilerJobMatrix[i][j] = False
            
    def createBinCompilerBash(self, jobList):
        noCleanup = ""
        if args.noCleanup:
            noCleanup = "--noCleanup "
        commandLines = ["Place holder for zeroth job"]
        return(pythonInterpreterAbsolutePath + " dsNickFury" + currentVersion + ".py --mode compiler --bins " + jobList + " --sequence " + args.sequence + " --genome " + args.genome + " --tempDir " + args.tempDir + " --species " + args.species + " " + noCleanup + " --genomeDirectory " + args.genomeListDirectory.replace(" ",'\ ') + "\n")
        
        
    def runBinCompilerJobs(self):
        import os
        import subprocess
        import time
        jobName = "binCompile"
        jobRange = " 1-" + str(self.parallelCompileJobs - 1) + " "
        command = "echo \"" + pythonInterpreterAbsolutePath + " arrayWrapper.py -d " + self.tempDir +  os.sep + "compilerBash\" | qsub -cwd -V -N " + jobName + " -l h_data=8G,time=23:59:00 -e " + os.getcwd() +  "/schedulerOutput/ -o " + os.getcwd() + "/schedulerOutput/ -M mweinste@ucla.edu -m a " + "-t " + jobRange
        success = False
        if not args.standAlone:
            if not args.mock:
                for i in range(0,10):
                    status = os.system(command)
                    success = status == 0
                    if success:
                        break
                if not success:
                    raise RuntimeError("Failed to submit job to scheduler.  Please check the status of the scheduler.")
            else:
                print("Mock submit: " + command)
        print("Running %s jobs on this node." %len(self.myJob))
        for job in self.myJob:
            print("Submitting: %s" %job)
            os.system(job)
        if args.standAlone:
            shortName = "Aug" + str(job)
            print("Submitting " + shortName)
            command = "bash " + self.tempDir + "/compilerBash/" + str(job) + ".sh"
            if not args.mock:
                import subprocess
                subprocess.Popen(command, shell = True)
            else:
                print ("MOCK SUBMIT: " + command)
        
    def monitorCompilerJobs(self):
        import time
        import os
        incomplete = True
        failedJobs = False
        totalJobs = 0
        for key1 in list(self.binCompilerJobMatrix.keys()):
            for key2 in list(self.binCompilerJobMatrix[key1].keys()):
                totalJobs += 1
        while incomplete:
            incomplete = 0
            rawDirList = os.listdir(self.tempDir + os.sep + "compilerBash")
            dirList = []
            for file in rawDirList:
                if file.endswith(".done") or file.endswith(".failed"):
                    dirList.append(file)
            #completedItems.append(str(args.chromosome + "." + str(args.workerID)))  #adding this instance's job to the completed job list
            for key1 in list(self.binCompilerJobMatrix.keys()):
                for key2 in list(self.binCompilerJobMatrix[key1].keys()):
                    if self.binCompilerJobMatrix[key1][key2]:  #check if this job is already listed as done
                        continue
                    checkName = str(key1) + "." + str(key2) + ".done"
                    if checkName in dirList:
                        self.binCompilerJobMatrix[key1][key2] = True
                    else:
                        failedName = str(key1) + "." + str(key2) + ".failed"
                        if failedName in dirList:
                            self.binCompilerJobMatrix[key1][key2] = True
                            print("Warning: Failure detected for job %s.%s                            " %(key1, key2))
                        else:
                            incomplete += 1
            print("Currently awaiting %s of %s jobs." %(incomplete, totalJobs), end = "\r")
        print("All %s parallel jobs completed.  Compiling tree structures." %(totalJobs))
        return True
       
    def createTreePickle(self):
        print("Creating tree structure.                     ")
        import os
        import pickle
        treePartsPath = self.outputDirectory + os.sep + "binMaps"
        treePartsDir = os.listdir(treePartsPath)
        treeParts = []
        for file in treePartsDir:
            if os.path.isfile(treePartsPath + os.sep + file) and file.endswith(".map"):
                treeParts.append(file)
        treeParts.sort()
        treeDumpFile = open(self.outputDirectory + os.sep + "tree.pkl", 'wb')
        treeDumpFile.write(bytes(8))  #This will be a placeholder for an 8-byte integer giving a pointer to the level1 tree pickle start
        treeLevel1 = {}  #tree level 1 will have a map of level2tree:startByte.  We can seek the byte and pickle.load it 
        for part in treeParts:
            dataFile = open(treePartsPath + os.sep + part, 'rb')
            byteMap = pickle.load(dataFile)
            dataFile.close()
            seedSequence = part[:-4]
            print("Processing tree data for sequence %s.                 " %(seedSequence), end = "\r")
            if seedSequence in treeLevel1:
                raise RuntimeError("Error: Attempting to add %s to tree structure twice.  This shouldn't be able to happen." %(seedSequence))
            treeLevel1[seedSequence] = treeDumpFile.tell()  #getting current position in the file
            pickle.dump(byteMap,treeDumpFile)
        level1StartByte = treeDumpFile.tell()
        pickle.dump(treeLevel1, treeDumpFile)
        treeDumpFile.seek(0)  #returning to overwrite the placeholder with the actual position (must be an 8 byte int)
        treeDumpFile.write(level1StartByte.to_bytes(8, "little")) #if the size of this file goes over zettabytes, I'll deal with it then.  Otherwise this int is more than big enough
        treeDumpFile.close()
                   
    def cleanup(self):
        import os
        import shutil
        # if not args.directToCompiler:
        #     os.remove(self.countFileName + ".gather")
        shutil.rmtree(self.tempDir)
        shutil.rmtree(self.outputDirectory + os.sep + "binMaps")
        
class EncodingData(object):
    
    def __init__(self, seed1, seed2, guideLength, pamLength, guideExtendLength, pamExtendLength, compressionScheme, contigEnumerationTable, contigDenumerationTable):
        self.seed1 = seed1
        self.seed2 = seed2
        self.guideLength = guideLength
        self.pamLength = pamLength
        self.guideExtendLength = guideExtendLength
        self.pamExtendLength = pamExtendLength
        self.compressionScheme = compressionScheme
        self.contigEnumerationTable = contigEnumerationTable
        self.contigDenumerationTable = contigDenumerationTable

class TargetTree(object):
    
    def __init__(self, level1, level2, packer): #initialize our target tree object.  Only thing we need to start off knowing is how many bases to make each level (ints)
        self.targetHash = {}
        self.level1 = int(level1)
        self.level2 = int(level2)
        self.packer = packer
        self.length = 0
        
    def add(self, site):
        pam, guide = site.sequence.split("_")
        if len(guide) < self.level1 + self.level2:
            raise RuntimeError("Combined bin length is greater than the set guide length.  Guide length: " + str(len(guide)) + " bins: " + str(self.level1) + ", " + str(self.level2) + ".")
        bigBin = guide[:self.level1]
        smallBin = guide[self.level1:self.level1 + self.level2]
        #sequenceString = "/".join([site.sequence, site.beforeStart, site.afterPAM])
        #writeString = "\t".join([site.contig, str(site.start), str(site.end), sequenceString, site.strand]) + "\n"
        site.beforeStart = site.beforeStart.replace("N","A")  #this is to deal with the rare case where the beforeStart goes into a run of N bases
        site.afterPAM = site.afterPAM.replace("N","A")  #this does the same for afterPAM.  It puts in some placeholder data that will not be used for matching, but may give invalid azimuth predictions if the site is used for that.  It allows the site to be properly encoded.
        site.beforeStart = site.beforeStart.replace("X","A")  #put in placeholders if we get back X in the extension (indicating we are at the end of a contig)
        site.afterPAM = site.afterPAM.replace("X","A")
        encodedSite = self.packer.packData(int(args.enumeratedContig.split(",")[1]), site.start, site.strand, site.sequence, site.beforeStart, site.afterPAM)
        try:  #try to add the leaf directly on the tree in the appropriate location
            self.targetHash[bigBin].append([smallBin, encodedSite])
        except KeyError:  #if the appropriate twig is not present, create the twig
            self.targetHash[bigBin] = []
            self.targetHash[bigBin].append([smallBin,encodedSite])
        self.length += 1
            
    def dump(self, directory, chromosome, jobID):
        import os
        import pickle
        directory = str(directory)  #almost impossible that this would come in as anything else
        jobID = str(jobID)  #quite possible that this could come in as an int type
        chromosome = str(chromosome)
        bigBins = list(self.targetHash.keys())
        written = 0
        totalFiles = len(bigBins)
        for bigBin in bigBins:
            smallBinDataList = self.targetHash[bigBin]
            if not os.path.isdir(directory + os.sep + bigBin + ".targetbin"):
                try:
                    os.mkdir(directory + os.sep + bigBin + ".targetbin")
                except OSError:  #this will happen if another process creates the bin directory during the short time between us checking for and not finding it and us trying to make it in this process
                    pass
            dumpFile = open(directory + os.sep + bigBin + ".targetbin/" + os.sep + chromosome + "." + jobID + ".dump", "ab")
            pickle.dump(smallBinDataList, dumpFile)
            dumpFile.close()
            written += 1
            print(str(written) + " of " + str(totalFiles) + " target collections written.             ", end = "\r")
        del self.targetHash
        self.targetHash = {}
        self.length = 0
        
class TargetFound(object):
    
    def __init__(self, contig, start, end, sequence, beforeStart, afterPAM, strand):
        self.contig = str(contig)
        self.start = str(start)
        self.end = str(end)
        self.sequence = sequence[::-1]
        self.afterPAM = afterPAM
        self.beforeStart = beforeStart
        self.strand = strand

class SequenceSearch(object):
    
    def __init__(self, inputFile, contigStart, contigLength, windowsize, pamList, beforeStartExtension, afterPAMextension):
        self.beforeStartExtension = int(beforeStartExtension)
        self.afterPAMextension = int(afterPAMextension)
        self.maxExtension = max(self.beforeStartExtension, self.afterPAMextension)
        self.lastGroup = 0
        self.done = False
        self.windowsize = windowsize
        self.start = 0  #start is inclusive
        self.end = self.windowsize #end is not inclusive (keeping with BED standards)
        self.pamList = pamList
        self.pamLength = len(pamList[0])  #calling the first item in the list so I don't just get the number of possible pams
        self.extendedStart = self.getExtendedStart(inputFile, contigStart)
        self.extendedEnd = self.getExtendedEnd(inputFile, contigStart, contigLength)
        inputFile.seek(int(contigStart))
        self.refSeq = inputFile.read(int(contigLength))
        self.refSeq = self.refSeq.replace("\n","")
        self.refSeq = self.refSeq.upper()
        self.refSeqLength = len(self.refSeq)

        
    def getExtendedStart(self, inputFile, contigStart):
        try:
            inputFile.seek(int(contigStart) - self.maxExtension - 20)
        except ValueError:  #if we are before the start of the file
            return False
        extension = inputFile.read(self.maxExtension + 20) #read in the (larger than we need) chunk of file from before the contig of interest
        extension = extension.replace("\n","") #get rid of end of line characters (they'll mess us up at the next step)
        for character in extension[-(self.maxExtension + 10):]:
            if character.upper() not in ['A','T','G','C','N']:  #this will trip off if we are seeing the contig name line in the extension (we won't get extensions near the start or end of the contig)
                return False
        if len(extension) < self.maxExtension:
            return False
        else:
            return extension[-self.maxExtension:]
        
    def getExtendedEnd(self, inputFile, contigStart, contigLength):
        try:
            inputFile.seek(int(contigStart) + int(contigLength))
        except ValueError:  #note that this should never actually happen unless the python standard changes.  If we seek past the end of the file, we will just keep reading a bunch of nothing (and will catch that later)
            return False
        extension = inputFile.read(self.maxExtension + 20)
        if not len(extension) < self.maxExtension:  #if we didn't read anything because we reached the end of the file
            return False
        extension = extension.replace("\n","")
        for character in extension[:self.maxExtension + 1]:  #we can use a shorter window here, since we are guaranteed to hit the > symbol denoting a new contig before we hit the contig name itself.  Contig names are unlikely, but not certain to trip this off.  The > is guaranteed to.
            if character.upper() not in ['A','T','G','C','N']:
                return False
        if len(extension) < self.maxExtension:
            return False
        else:
            return extension[:maxExtension]
        
    def nextMatch(self):
        import degenerateBaseHandle
        self.forwardMatch = False
        self.reverseMatch = False
        if self.start // 10000 > self.lastGroup and (args.verbose or not args.workerID):
            print("Tested " + str((self.start // 10000)*10000), end = "\r")
            self.lastGroup = self.start // 10000
        self.sequence = self.refSeq[self.start:self.end]
        if ">" in self.sequence:
            raise RuntimeError("Ran off end of chromosome.  > in sequence: " + self.sequence)
        if not self.sequence:
            return False
        if self.sequence[-1] == "N":
            self.nInLastPositionJump()
            return False
        if "N" in self.sequence:
            return False
        if self.sequence[-self.pamLength:].upper() in self.pamList:
            guide = self.sequence[:-self.pamLength]
            pam = self.sequence[-self.pamLength:]
            self.forwardMatch = guide + "_" + pam
            for extension in range(self.afterPAMextension,0,-1):  #Start a loop that will iterate 3, 2, 1.  It will end before hitting 0 and we will be left with an empty string value (which we will try to handle after this)
                try:  #if we have the sequence, we grab what parts of it we can here
                    self.forwardAfterPAM = self.refSeq[self.end:self.end + extension]  #if this works, we had the sequence and quit the loop
                    break
                except IndexError:  #if we were off the edge of the sequence (something that will only happen at the very beginning or end)
                    self.forwardBeforeStart = ""
                    continue  #try taking a smaller extension
            if len(self.forwardAfterPAM) != self.afterPAMextension:
                if not self.extendedEnd:
                    self.extendedEnd = "X" * self.afterPAMextension
                missingLetterCount = self.afterPAMextension - len(self.forwardAfterPAM)
                extraLetters = self.extendedEnd[:missingLetterCount]  #we should already have verified that the extension was of the proper length.  If this throws an exception, that needs to be fixed, probably at the getExtension method level
                self.forwardAfterPAM = self.forwardAfterPAM + extraLetters
            for extension in range(-self.beforeStartExtension,0):
                try:
                    self.forwardBeforeStart = self.refSeq[self.start + extension:self.start]
                    break
                except IndexError:
                    self.forwardBeforeStart = ""
                    continue
            if len(self.forwardBeforeStart) != self.beforeStartExtension:
                if not self.extendedStart:
                    self.extendedStart = "X" * self.beforeStartExtension
                missingLetterCount = self.beforeStartExtension - len(self.forwardBeforeStart)
                extraLetters = self.extendedStart[-missingLetterCount:]
                self.forwardBeforeStart = extraLetters + self.forwardBeforeStart
        else:
            self.forwardMatch = False
        revComp = str(degenerateBaseHandle.ReverseComplement(self.sequence))
        if revComp[-self.pamLength:].upper() in self.pamList:
            guide = revComp[:-self.pamLength]
            pam = revComp[-self.pamLength:]
            self.reverseMatch = guide + "_" + pam
            for extension in range(-self.afterPAMextension,0):
                try:
                    self.reverseAfterPAM = str(degenerateBaseHandle.ReverseComplement(self.refSeq[self.start + extension:self.start]))
                    break
                except IndexError:
                    self.reverseAfterPAM = ""  #this will be reset if the loop completes and will stay an empty string if we are at the end of the contig
                    continue
            if len(self.reverseAfterPAM) != self.afterPAMextension:
                if not self.extendedStart:
                    self.extendedStart = "X" * self.afterPAMextension
                missingLetterCount = self.afterPAMextension - len(self.reverseAfterPAM)
                if not "X" in self.extendedStart:
                    extraLetters = str(degenerateBaseHandle.ReverseComplement(self.extendedStart))[:missingLetterCount]
                else:
                    extraLetters = self.extendedStart[:missingLetterCount]
                self.reverseAfterPAM = self.reverseAfterPAM + extraLetters
            for extension in range(self.beforeStartExtension,0,-1):
                try:
                    self.reverseBeforeStart = str(degenerateBaseHandle.ReverseComplement(self.refSeq[self.end:self.end + extension]))
                    break
                except IndexError:
                    self.reverseBeforeStart = ""
                    continue
            if len(self.reverseBeforeStart) != self.beforeStartExtension:
                if not self.extendedEnd:
                    self.extendedEnd = "X" * self.beforeStartExtension
                missingLetterCount = self.beforeStartExtension - len(self.reverseBeforeStart)
                if not "X" in self.extendedEnd:
                    extraLetters = str(degenerateBaseHandle.ReverseComplement(self.extendedEnd))[-missingLetterCount:]
                else:
                    extraLetters = self.extendedEnd[-missingLetterCount:]
                self.reverseBeforeStart = extraLetters + self.reverseBeforeStart
        else:
            self.reverseMatch = False
        return (self.forwardMatch or self.reverseMatch)
    
    def nInLastPositionJump(self):
        self.start += self.windowsize - 1
        self.end += self.windowsize - 1
        self.done = self.end > self.refSeqLength
            
    def advance(self):
        self.start += 1
        self.end += 1
        self.done = self.end > self.refSeqLength
        
    def getNextMatch(self):
        self.first = True
        while not self.nextMatch() and not self.done or self.first:
            self.first = False
            self.advance()
        return (not self.done)
        
    
class FASTAreader(object):
    
    def __init__(self):
        self.hitCount = 0
        self.chunkStart = self.getChunkStart()
        self.outputDirectory = args.genomeListDirectory + args.sequence[::-1] + "." + args.genome + "." + args.species
        self.genCodeData = self.getGenCodeData()
        self.packer = self.instantiateEncoder()
        self.fileChromosome = self.getFileChromosome
        windowsize = len(args.sequence) - 1  #the minus 1 is because there is an underscore between the guide and pam
        guide, pam = args.sequence.split("_")
        if args.forcePamList:
            pamList = self.useForcedPamList()
        else:
            pamList = self.createPamList(pam)
        inputFile = open(args.inputfile, 'r')
        self.runSearchJob(SequenceSearch(inputFile, args.start, args.length, windowsize, pamList, args.guideExtension, args.pamExtension))
        #self.clockOut() #not needed if using a wrapper to handle the clocking out
        
    def getGenCodeData(self):
        import pickle
        import os
        genCodeDataFile = self.outputDirectory + os.sep + "genCodeData.pkl"
        if not os.path.isfile(genCodeDataFile):
            raise RuntimeError("Unable to find encoding data file at %s." %(genCodeDataFile))
        dataFile = open(genCodeDataFile, 'rb')
        data = pickle.load(dataFile)
        dataFile.close()
        return data
    
    def instantiateEncoder(self):
        import dataPacker
        guide, pam = args.sequence.split("_")
        packer = dataPacker.DataPacker(self.genCodeData.compressionScheme, len(pam), len(guide), args.guideExtension, args.pamExtension)
        return packer
                
    def useForcedPamList(self):
        import degenerateBaseHandle
        forcePamList = args.forcePamList.split(",")
        nonDegeneratePamList = []
        for site in forcePamList:
            nonDegeneratePamList += degenerateBaseHandle.NondegenerateBases(site).permutations()
        return nonDegeneratePamList
            
    def getChunkStart(self):
        lineDifference = self.getLineDifference()
        if args.workerID:
            chunkStartByte = int(args.chunkSize) * (int(args.workerID) - 1)
            chunkStart = chunkStartByte - (lineDifference * (chunkStartByte // self.lineBytes))
            #print("ChunkStartByte: " + str(chunkStartByte))
            #print("ChunkStart: " + str(chunkStart))
        else:
            chunkStart = 0
        return chunkStart
    
    def getLineDifference(self):
        inputFile = open(args.inputfile, 'r')
        characterCountCheck = inputFile.readline()
        while ">" in characterCountCheck:
            characterCountCheck = inputFile.readline()
        inputFile.close()
        self.lineBytes = len(characterCountCheck)
        lineBases = len(characterCountCheck.strip())
        lineDifference = self.lineBytes - lineBases
        #print("Line diff: " + str(lineDifference))
        return lineDifference
    
    def getFileChromosome(self):
        try:
            chromosome = int(args.chromosome)
            chromosome = str(chromosome).zfill(2)
        except ValueError:
            chromosome = args.chromosome
        if chromosome == "M":
            fileChromosome = "zM"
        else:
            fileChromosome = chromosome
        return fileChromosome
    
    def createPamList(self, pam):
        import degenerateBaseHandle
        degeneratePam = False
        for character in pam:
            if character not in ["A","T","G","C"]:
                degeneratePam = True
        if not degeneratePam:
            pamList = [pam]
        else:
            pamList = list(degenerateBaseHandle.NondegenerateBases(pam))
        return pamList
    
    def getOutputFileName(self):
        if not args.workerID:
            outputFileName = self.outputDirectory + "/" + self.fileChromosome + "c" + str(self.hitCount // 10000).zfill(9)
        else:
            outputFileName = self.outputDirectory + "/" + self.fileChromosome + "c" + str(args.workerID).zfill(3) + str(self.hitCount // 10000).zfill(9)
        return outputFileName
    
    def runSearchJob(self, searchJob):
        targetTree = TargetTree(args.treeLevel1, args.treeLevel2, self.packer) #initializing the object to store all of our found CRISPR targets
        while searchJob.getNextMatch():
            print("Found %s matches." %(self.hitCount), end = "\r")
            if searchJob.forwardMatch:
                site = TargetFound(args.chromosome, (searchJob.start + self.chunkStart + 1), (searchJob.end + self.chunkStart + 1 + 1), searchJob.forwardMatch, searchJob.forwardBeforeStart, searchJob.forwardAfterPAM, "+") # The plus 1 in the position is because chromosome data is indexed to 0 while chromosome positions are indexed to 1.  The second +1 for the end location is to account for the BED file standard end base not being inclusive (like python indexing).
                targetTree.add(site)
                self.hitCount += 1
            if searchJob.reverseMatch:
                site = TargetFound(args.chromosome, (searchJob.start + self.chunkStart + 1), (searchJob.end + self.chunkStart + 1 + 1), searchJob.reverseMatch, searchJob.reverseBeforeStart, searchJob.reverseAfterPAM, "-")
                targetTree.add(site)
                self.hitCount += 1
            if targetTree.length >= args.cacheSize:
                targetTree.dump(self.outputDirectory, args.chromosome, args.workerID)
        targetTree.dump(self.outputDirectory, args.chromosome, args.workerID)
         
    def clockOut(self):
        if not args.workerID:
            touchFile = open(args.tempDir + "/completed/" + args.chromosome, 'w')  #This is the clockout
            touchFile.close()
            countFileName = args.genomeListDirectory + "genomeData/" + args.sequence[::-1] + "." + args.genome + "." + args.species.upper() + ".gather"
            countFile = open(countFileName, 'a')
            countFile.write(args.chromosome + "\t" + str(self.hitCount) + "\n")
            countFile.close()
        else:
            self.countFileName = args.genomeListDirectory + "genomeData/" + args.sequence[::-1] + "." + args.genome + "." + args.species.upper() + ".gather"
            countFile = open(self.countFileName, 'a')
            countFile.write(args.chromosome + "\t" + args.workerID + "\t" + str(self.hitCount) + "\n")
            countFile.close()
            touchFile = open(args.tempDir + "/completed/" + args.chromosome + "." + str(args.workerID), 'w')
            touchFile.close()
            
class bigBinCompiler(object):
    
    def __init__(self):
        import os
        self.genomeDirectory = args.genomeListDirectory + os.sep + args.sequence[::-1] + "." + args.genome + "." + args.species
        self.binList = args.bins.split(",")
        processedBins = 0
        print("Processed " + str(processedBins) + " of " + str(len(self.binList)) + " level 1 bins.")
        for largeBin in self.binList:
            self.compile(largeBin)
            processedBins += 1
            print("Processed " + str(processedBins) + " of " + str(len(self.binList)) + " level 1 bins.")
        #self.clockOut()
        
    def compile(self, largeBin):
        import os
        import pickle
        binDir = self.genomeDirectory + os.sep + largeBin + ".targetbin"
        dirList = os.listdir(binDir)
        targetCollector = []
        dumpFiles = []
        for item in dirList:
            itemPath = binDir + os.sep + item
            if os.path.isfile(itemPath) and item.endswith(".dump"):
                dumpFiles.append(itemPath)
        print("Found " + str(len(dumpFiles)) + " collection files to process.")
        for file in dumpFiles:
            fileHandle = open(file, 'rb')
            targets = []
            hitEOF = False
            while not hitEOF:  #loop that will run and unpickle everything in the file.  It should be ended by a handled EOF exception
                try:
                    targets += pickle.load(fileHandle)
                except EOFError:
                    hitEOF = True
            fileHandle.close()
            targetCollector += targets
        print("Total targets: " + str(len(targetCollector)))
        outputFileHash = {}
        print("Splitting targets by level 2 sequence")
        for target in targetCollector:
            if target[0] in outputFileHash:
                outputFileHash[target[0]] += target[1]
            else:
                outputFileHash[target[0]] = target[1]
        level2Branches = list(outputFileHash.keys())
        level2Branches.sort()
        fileByteMap = {}
        currentByte = 0
        outputBytes = bytes()
        for branch in level2Branches:
            branchByteLength = len(outputFileHash[branch])
            fileByteMap[branch] = (currentByte, branchByteLength)
            currentByte += branchByteLength
            outputBytes += outputFileHash[branch]
        binarySiteFile = open(self.genomeDirectory + os.sep + "targets" + os.sep + largeBin + ".bct",'wb')  # .bct = .binary crispr targets
        byteMapFile = open(self.genomeDirectory + os.sep + "binMaps" + os.sep + largeBin + ".map",'wb')
        binarySiteFile.write(outputBytes)
        binarySiteFile.close()
        pickle.dump(fileByteMap, byteMapFile)
        byteMapFile.close()
        if not args.noCleanup:
            import shutil
            shutil.rmtree(binDir)    
            
#=====================================================Execution code===========================================================================

def main():
    import datetime
    import os
    import sys
    if not os.path.isdir("schedulerOutput"):  #Used for writing scheduler output of subprocesses to a single folder, otherwise this folder can start getting messy.  Only needed for cluster operation, not single server.
       os.mkdir("schedulerOutput")
    startTime = datetime.datetime.now()
    arguments = Args()
    global args
    args = arguments
    del arguments
    if args.mode == 'index':
        run = FASTASupervisor()
    elif args.mode == 'FASTAWorker':
        run = FASTAreader()
    elif args.mode == 'search':
        run = SearchSupervisor()
    elif args.mode == 'worker':
        run = WorkerJob()
    elif args.mode == 'selection':
        run = TargetSelection()
    elif args.mode == 'compiler':
        run = bigBinCompiler()
    runTime = datetime.datetime.now() - startTime
    print (args.mode.upper() + " run completed in " + (str(runTime)), file = sys.stderr)
    quit()
main()
