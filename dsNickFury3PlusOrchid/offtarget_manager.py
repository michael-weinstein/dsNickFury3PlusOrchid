import re, os
import subprocess

import pandas as pd

import settings
import utils

class OfftargetManager(object):

    def __init__(self, filename, mismatchTolerance=6, endClip=0, mismatchLimit=40000):
        # self.azureAccount = settings.azure_account
        # self.tableName = settings.table_name

        self.mismatchTolerance = mismatchTolerance
        self.endClip = endClip
        self.mismatchLimit = mismatchLimit
        self.params_str = "_MM%d_end%d_lim%d" % (self.mismatchTolerance, self.endClip, self.mismatchLimit)

        self.filename = filename
        self.filename_noext = ".".join(filename.split(".")[:-1])
        self.filename_ext = filename.split(".")[-1]

        self.targets = []
        self.filenames = []
        self.commands = []

    def extract_targets(self, func, delim=None, sheetname=0):
        ext = self.filename_ext
        targets = []
        if ext == "xlsx" or ext == "xls":
            df = pd.read_excel(self.filename)
        else:
            df = pd.read_csv(self.filename, delimiter=delim)
        for row in df.iterrows():
            targets.append(func(row[1].values))
        return targets

    def set_targets(self, targets, sort=True):
        if sort:
            self.targets = sorted(targets, key=lambda x: x[1]+"_"+x[2])
        else:
            self.targets = targets

    def get_guide_filename(self, target):
        gene, guide, pam = target
        targetSeq = guide + "_" + pam
        output_fn = self.filename_noext + self.params_str + "".join(map(lambda x: "_" + x, [gene, targetSeq])) + ".txt"
        return output_fn

    def fix_filenames(self):
        for target in self.targets:
            gene, guide, pam = target
            targetSeq = guide + "_" + pam

            curr_filename = self.get_guide_filename(target)

            old1 = self.filename_noext + "_MM%d_end%d" % (self.mismatchTolerance, self.endClip) + "_".join([gene, targetSeq]) + ".txt"
            if os.path.exists(old1):
                os.rename(old1, curr_filename)

            old2 = self.filename_noext + self.params_str + "_".join([gene, targetSeq]) + ".txt"
            if os.path.exists(old2):
                os.rename(old2, curr_filename)

    def generate_command_list(self, output_to_file=True, network_root=None):
        filename = self.filename
        self.filenames = []
        self.commands = []

        mismatchTolerance = self.mismatchTolerance
        mismatchLimit = self.mismatchLimit
        endClip = self.endClip

        for target in self.targets:
            gene, guide, pam = target
            targetSeq = guide + "_" + pam
            if output_to_file:
                output_fn = self.get_guide_filename(target)
                if network_root is not None:
                    output_fn = "\\".join([network_root] + output_fn.split("\\")[1:])
                self.filenames.append(output_fn)
                output_fn = '"'+output_fn+'"'
                dsNickFuryPath = "dsNickFury3.2.py"
                command_str = settings.python3_bin + " " + dsNickFuryPath + " -m search -g hg38 -s " + targetSeq + " --matchSiteCutoff " + str(mismatchLimit) + " --endClip " + str(endClip) + " --noElevation" + " -t " + str(mismatchTolerance) + " --outputToFile " + output_fn
            else:
                azureTableInfo = [self.azureAccount, self.tableName, gene, targetSeq]
                azureTableInfo = [re.sub('\W', "_", item) for item in azureTableInfo]
                azureTableString = ",".join(azureTableInfo)
                command_str = settings.python3_bin + " dsNickFury3.2.py -m search -g hg38 -s " + targetSeq + " --matchSiteCutoff " + str(mismatchLimit) + " --endClip " + str(endClip) + " --noElevation" + " -t " + str(mismatchTolerance) + " --azureTableOut " + azureTableString
            self.commands.append(command_str)

        return self.commands

    def merge_output_files(self):
        filename_noext = self.filename_noext
        fh = open(self.filename_noext + self.params_str + "_merged.txt", "w")
        for target in self.targets:
            output_fn = self.get_guide_filename(target)
            fh.write(open(output_fn).read())

    def write_hdf5(self, filter_func=None):
        filename = self.filename_noext + self.params_str + "_merged.txt"
        data = utils.read_dsnf(filename).rename(index=str, columns={
            'ontarget': '30mer',
            'offtarget': '30mer_mut',
        })
        filename_hdf = self.filename_noext + self.params_str + ".hdf5"
        data.to_hdf(filename_hdf, 'allsites', format='table')

    def get_hdf5(self):
        filename_hdf = self.filename_noext + self.params_str + ".hdf5"
        return pd.read_hdf(filename_hdf, 'allsites')

    def write_commands(self):
        commands_file = self.filename_noext + self.params_str + ".commands.txt"
        with open(commands_file, "w") as fh:
            for command in self.commands:
                fh.write(command + "\n")

    def execute_commands(self):
        for i in range(len(self.commands)):
            filename = self.filenames[i]
            if os.path.exists(filename):
                print("SKIPPING", filename)
                continue

            command = self.commands[i]
            print(command)
            subprocess.call(command, shell=True)
