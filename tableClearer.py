#!/usr/bin/env python3

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

class CheckArgs():  #class that checks arguments and ultimately returns a validated set of arguments to the main program
    
    def __init__(self):
        import argparse
        import os
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--user", help = "user name")
        parser.add_argument("-t", "--table", help = "table to delete")
        rawArgs = parser.parse_args()
        if not rawArgs.table or not rawArgs.user:
            raise RuntimeError("Missing either user or table name to delete (or both)")
        self.table = rawArgs.table
        self.user = rawArgs.user
     
def main():
    import time
    args = CheckArgs()
    if not yesAnswer("Are you sure you want to delete table \"%s\"" %(args.table)):
        quit("Goodbye.")
    print("Please confirm that you want to delete %s by typing its name" %(args.table))
    tableCheck = input(">>")
    if not tableCheck.upper() == args.table.upper():
        quit("Table name check did not pass.  Quitting.")
    import azure.storage.table
    try:
        tableAccountKeyFile = open('azureTable.apikey','r')
    except FileNotFoundError:
        raise RuntimeError("Unable to find the key to the azure table in azureTable.apikey (file was absent)")
    tableAccountkey = tableAccountKeyFile.read().strip()
    tableAccountKeyFile.close()
    tableHandle = azure.storage.table.TableService(account_name=args.user, account_key=tableAccountkey)
    deleted = tableHandle.delete_table(args.table)
    if deleted:
        print("Deleted table")
    else:
        print("Unable to delete table")
    recreated = False
    attempts = 0
    while not recreated:
        recreated = tableHandle.create_table(args.table)
        if not recreated:
            time.sleep(5)
            attempts += 1
            if attempts > 10:
                raise RuntimeError("Unable to recreate table")
    print("Recreated table")
main()
