#!/usr/bin/env python3

class CheckArgs(object):
   
    def __init__(self):
        import argparse
        import os
        import sys
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--multitest", help = "Multitest mode", action = 'store_true')
        parser.add_argument("-t", "--table", help = "Table name")
        parser.add_argument("-p", "--partition", help = "Partition key (column)")
        parser.add_argument("-r", "--row", help = "Row key (row)")
        parser.add_argument("-a", "--attribute", help = "Attribute")
        rawArgs = parser.parse_args()
        if rawArgs.multitest:
            self.multitest = True
        else:
            self.multitest = False
            if not rawArgs.table:
               raise RuntimeError("Table name not specified")
            if not rawArgs.partition:
                raise RuntimeError("Partition key not specified")
            if not rawArgs.row:
                raise RuntimeError("Row key not specified")
            self.table = rawArgs.table
            self.partition = rawArgs.partition
            self.row = rawArgs.row
            self.attribute = rawArgs.attribute
            

class ItemGetter(object):
    
    def __init__(self, azureTableAccountName):
        print("Connecting to Azure tables for query")
        import azure.storage.table
        try:
            tableAccountKeyFile = open('azureTable.apikey','r')
        except FileNotFoundError:
            raise RuntimeError("Unable to find the key to the azure table in azureTable.apikey (file was absent)")
        tableAccountkey = tableAccountKeyFile.read().strip()
        tableAccountKeyFile.close()
        self.tableHandle = azure.storage.table.TableService(account_name=azureTableAccountName, account_key=tableAccountkey)

    def get(self, table, partitionKey, rowKey, attribute = False):
        tableCell = self.tableHandle.get_entity(table, partitionKey, rowKey)
        if not attribute:
            return tableCell
        else:
            return tableCell[attribute]
        
def multiTest():
    import azure.common  #need this for exception handling
    seqFile = open("chr21Tests.txt")
    sequences = seqFile.read().strip()
    seqFile.close()
    sequences = sequences.split("\n")
    sequences = [sequence.split("\t") for sequence in sequences]
    sequences = [(sequence[0][:20] + "_" + sequence[0][20:], sequence[1]) for sequence in sequences]
    table = ItemGetter("crispr")
    for sequence in sequences:
        try:
            print(table.get("hg38v85", sequence[1], sequence[0], "aggregatedOffTarget"))
        except azure.common.AzureMissingResourceHttpError:
            print("NOT FOUND")
     
def main():
    args = CheckArgs()
    if args.multitest:
        multiTest()
    else:
        table = ItemGetter("crispr")
        print(table.get(args.table, args.partition, args.row, args.attribute))
        
if __name__ == '__main__':
    main()