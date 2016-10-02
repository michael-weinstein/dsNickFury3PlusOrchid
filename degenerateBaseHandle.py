#!/usr/bin/env python3

class ReverseComplement(object):  #declares an object class.  We capitalize the first letter (unlike variables that should start with lowercase) to avoid potential collisions with variable names
    
    def __init__(self, sequence, reverse = True, case = 'original'):
        case = case.lower()
        if not case in ['upper','lower','original']:
            raise ValueError('Case option must be set to upper, lower, or original.')
        self.case = case
        if reverse:  #we defined an optional argument "reverse" to be true.  We did this because we assume people will often want the reverse complement.  They have to specify reverse = False if they don't.
            self.inputSeq = sequence[::-1]  #Neat trick in Python to reverse the order of an iterable (string, list, etc).  Indexing goes [inclusive start:non-inclusive end:step].  A step of -1 tells it to start from the end and step backwards 1 element at a time.  This seems to run slightly more efficiently than iterating in reverse.
        else: #if the user wants a non-reverse complement
            self.inputSeq = sequence  #we store the value without reversing.  The self.[name] means that this value will be variable that can be called from anywhere within this instance of the object AND from outside the object by calling [instance].[name].  A variable that is tied to a function like this one is called an attribute. 
        if self.case == 'upper':  #now that case is being handled by the dictionary itself, we just need to change the original sequence if necessary
            self.inputSeq = self.inputSeq.upper()  
        elif self.case == 'lower':
            self.inputSeq == self.inputSeq.lower()
        self.complementTable = self.createComplementTable()  #this is defining an attribute of the object (complementTable) by calling the createComplementTable method.  Of interest, since the table is just returned by the function, a program could call the table for its own use by calling [instance].createComplementTable()
        self.complementLists = self.createComplementLists()  #same as above, but this one gets back all non-degenerate possibilities
        self.checkInput() #always good to validate inputs.  This will handle any invalid letters entered.  It will still raise an exception, but will be more specific in the error reporting.
        self.outputSeqString = self.createOutputString()  #Creates the outputString (the reverse complement).  Because this is called in the __init__ initializer method, we automatically calculate the reverse complement (why this is convenient will be covered in the __str__ overload method)
        self.outputList = False  #this initializes an attribute to False.  Why we want to do this will be covered as part of a later method.
        
        
    def __str__(self):  #this is overloading the existing str(object) method.  Normally, if I tried to print(thisObject), I would either get an exception or a bunch of rubbish back.
        return self.outputSeqString  #Instead, this says that if I try to print the entire object or turn it to a string, what I REALLY want to get back is the outputSeqString I created in the initialization function
        
    def createComplementTable(self):  #Will this work faster is we just define the values by case in our dictionary?
        complementTable =  {"A":"T",
                            "T":"A",
                            "G":"C",
                            "C":"G",
                            "Y":"R",
                            "R":"Y",
                            "S":"S",
                            "W":"W",
                            "K":"M",
                            "M":"K",
                            "B":"V",
                            "D":"H",
                            "H":"D",
                            "V":"B",
                            "N":"N",
                            "a":"t",
                            "t":"a",
                            "g":"c",
                            "c":"g",
                            "y":"r",
                            "r":"y",
                            "s":"s",
                            "w":"w",
                            "k":"m",
                            "m":"k",
                            "b":"v",
                            "d":"h",
                            "h":"d",
                            "v":"b",
                            "n":"n"}
        return complementTable
    
    def createComplementLists(self):  
        complementLists =  {"A":["T"],
                            "T":["A"],
                            "G":["C"],
                            "C":["G"],
                            "Y":["G","A"],
                            "R":["T","C"],
                            "S":["C","G"],
                            "W":["T","A"],
                            "K":["A","C"],
                            "M":["T","G"],
                            "B":["G","C","A"],
                            "D":["T","C","A"],
                            "H":["T","G","A"],
                            "V":["T","G","C"],
                            "N":["T","G","C","A"],
                            "a":["t"],
                            "t":["a"],
                            "g":["c"],
                            "c":["g"],
                            "y":["g","a"],
                            "r":["t","c"],
                            "s":["c","g"],
                            "w":["t","a"],
                            "k":["a","c"],
                            "m":["t","g"],
                            "b":["g","c","a"],
                            "d":["t","c","a"],
                            "h":["t","g","a"],
                            "v":["t","g","c"],
                            "n":["t","g","c","a"]}
        return complementLists
    
    def checkInput(self):  #Input validation
        for letter in self.inputSeq:   #iterate over the input letters
            if letter not in list(self.complementLists.keys()):  #get a list of keys from the complement table, and if a letter is in the input sequence that is not a key in the table
                raise ValueError(letter + " in " + self.inputSeq + " is not a valid DNA base.")  #Raise an exception that explicitly lists what the problem was and where.  Help the user help themselves.
            
    def createOutputString(self):  #This simple function creates our most basic output: a reverse complement string containing any degeneracy that may have been in the original
        output = ""  #intialize an empty string
        for letter in self.inputSeq:  #iterate over our input string (which, if appropriate was reversed in the initializer)
            output += self.complementTable[letter]  #add on the proper complementary base to the growing output string
        return output  #return the output
    
    def permutations(self):  #turn a sequence containing degenerate bases into a list of all possible non-degenerate sequences
        import itertools  #this library contains the code we need to create all possible permutations and probably does so more efficiently than our own code would
        if self.outputList:  #if we already have the value we are trying to create here (and we can tell because it is no longer the False value we initialized it to)
            return self.outputList  #we avoid repeating previous work and just output what we already have stored.  As will be shown in the test code below, the work required for this function can grow exponentially.  We only want to run it if it is requested AND we only ever want to run it the one time.
        letterList = []  #initialize an empty list to store a list of lists, where the outer list will correspond to the letters of the sequence and each inner list will represent all possibilities for that letter
        for letter in self.inputSeq:  #iterate over the input sequence
            letterList.append(self.complementLists[letter])  #add a list of possible bases to a growing list of possible bases at each position
        self.outputList = [''.join(letter) for letter in itertools.product(*letterList)]  #use the itertools module's product function to create the permutations (if this line seems strange to you, try looking up list comprehension in python and positional arguments, commonly called *args)
        return self.outputList #return the (potentially quite large) list
    
class RNAReverseComplement(ReverseComplement):  #declare another class called RNAReverseComplement as an extension of the ReverseComplement base class
    
    def createComplementTable(self):  #Will this work faster is we just define the values by case in our dictionary?
        complementTable =  {"A":"U",
                            "T":"A",
                            "U":"A",
                            "G":"C",
                            "C":"G",
                            "Y":"R",
                            "R":"Y",
                            "S":"S",
                            "W":"W",
                            "K":"M",
                            "M":"K",
                            "B":"V",
                            "D":"H",
                            "H":"D",
                            "V":"B",
                            "N":"N",
                            "a":"u",
                            "t":"a",
                            "u":"a",
                            "g":"c",
                            "c":"g",
                            "y":"r",
                            "r":"y",
                            "s":"s",
                            "w":"w",
                            "k":"m",
                            "m":"k",
                            "b":"v",
                            "d":"h",
                            "h":"d",
                            "v":"b",
                            "n":"n"}
        return complementTable
    
    def createComplementLists(self):  
        complementLists =  {"A":["U"],
                            "T":["A"],
                            "U":["A"],
                            "G":["C"],
                            "C":["G"],
                            "Y":["G","A"],
                            "R":["U","C"],
                            "S":["C","G"],
                            "W":["U","A"],
                            "K":["A","C"],
                            "M":["U","G"],
                            "B":["G","C","A"],
                            "D":["U","C","A"],
                            "H":["U","G","A"],
                            "V":["U","G","C"],
                            "N":["U","G","C","A"],
                            "a":["u"],
                            "t":["a"],
                            "u":["a"],
                            "g":["c"],
                            "c":["g"],
                            "y":["g","a"],
                            "r":["u","c"],
                            "s":["c","g"],
                            "w":["u","a"],
                            "k":["a","c"],
                            "m":["u","g"],
                            "b":["g","c","a"],
                            "d":["u","c","a"],
                            "h":["u","g","a"],
                            "v":["u","g","c"],
                            "n":["u","g","c","a"]}
        return complementLists

class InosineReverseComplement(ReverseComplement):
    
    def createComplementTable(self):  #Will this work faster is we just define the values by case in our dictionary?
        complementTable =  {"A":"T",
                            "T":"A",
                            "G":"C",
                            "C":"G",
                            "Y":"R",
                            "R":"Y",
                            "S":"S",
                            "W":"W",
                            "K":"M",
                            "M":"K",
                            "B":"V",
                            "D":"H",
                            "H":"D",
                            "V":"B",
                            "N":"N",
                            "I":"N",
                            "a":"t",
                            "t":"a",
                            "g":"c",
                            "c":"g",
                            "y":"r",
                            "r":"y",
                            "s":"s",
                            "w":"w",
                            "k":"m",
                            "m":"k",
                            "b":"v",
                            "d":"h",
                            "h":"d",
                            "v":"b",
                            "n":"n",
                            "i":"n"}
        return complementTable
    
    def createComplementLists(self):  
        complementLists =  {"A":["T","I"],
                            "T":["A","I"],
                            "G":["C","I"],
                            "C":["G","I"],
                            "Y":["G","A","I"],
                            "R":["T","C","I"],
                            "S":["C","G","I"],
                            "W":["T","A","I"],
                            "K":["A","C","I"],
                            "M":["T","G","I"],
                            "B":["G","C","A","I"],
                            "D":["T","C","A","I"],
                            "H":["T","G","A","I"],
                            "V":["T","G","C","I"],
                            "N":["T","G","C","A","I"],
                            "I":["A","T","G","C","I"],
                            "a":["t","i"],
                            "t":["a","i"],
                            "g":["c","i"],
                            "c":["g","i"],
                            "y":["g","a","i"],
                            "r":["t","c","i"],
                            "s":["c","g","i"],
                            "w":["t","a","i"],
                            "k":["a","c","i"],
                            "m":["t","g","i"],
                            "b":["g","c","a","i"],
                            "d":["t","c","a","i"],
                            "h":["t","g","a","i"],
                            "v":["t","g","c","i"],
                            "n":["t","g","c","a","i"],
                            "i":["a","t","g","c","i"]}
        return complementLists
       
class NondegenerateBases(ReverseComplement):
    
    def __init__(self, sequence, case = 'original'):
        case = case.lower()
        if not case in ['upper','lower','original']:
            raise ValueError('Case option must be set to upper, lower, or original.')
        self.case = case
        self.inputSeq = sequence  #we store the value without reversing.  The self.[name] means that this value will be variable that can be called from anywhere within this instance of the object AND from outside the object by calling [instance].[name].  A variable that is tied to a function like this one is called an attribute. 
        if self.case == 'upper':  #now that case is being handled by the dictionary itself, we just need to change the original sequence if necessary
            self.inputSeq = self.inputSeq.upper()  
        elif self.case == 'lower':
            self.inputSeq == self.inputSeq.lower()
        self.complementLists = self.createComplementLists()  #same as above, but this one gets back all non-degenerate possibilities
        self.checkInput() #always good to validate inputs.  This will handle any invalid letters entered.  It will still raise an exception, but will be more specific in the error reporting.
        self.outputList = self.permutations()  #this initializes an attribute to False.  Why we want to do this will be covered as part of a later method.
        
    def __str__(self, separator = "\n"):
        return separator.join(self.outputList)
    
    def __iter__(self):
        for i in range(0,len(self.outputList)):
            yield self.outputList[i]
            
    def __getitem__(self, index):
        return self.outputList[index]
    
    def __len__(self):
        return len(self.outputList)
        
    def createComplementLists(self):  
        complementLists =  {"A":["A"],
                            "T":["T"],
                            "G":["G"],
                            "C":["C"],
                            "Y":["C","T"],
                            "R":["A","G"],
                            "S":["G","C"],
                            "W":["A","T"],
                            "K":["T","G"],
                            "M":["A","C"],
                            "B":["C","G","T"],
                            "D":["A","G","T"],
                            "H":["A","C","T"],
                            "V":["A","C","G"],
                            "N":["A","C","G","T"],
                            "a":["a"],
                            "t":["t"],
                            "g":["g"],
                            "c":["c"],
                            "y":["c","t"],
                            "r":["a","g"],
                            "s":["g","c"],
                            "w":["a","t"],
                            "k":["t","g"],
                            "m":["a","c"],
                            "b":["c","g","t"],
                            "d":["a","g","t"],
                            "h":["a","c","t"],
                            "v":["a","c","g"],
                            "n":["a","c","g","t"]}
        return complementLists   

    def permutations(self):  #turn a sequence containing degenerate bases into a list of all possible non-degenerate sequences
        import itertools  #this library contains the code we need to create all possible permutations and probably does so more efficiently than our own code would
        try: #This try/except block is another way of determining if we have already calculated this list out.  I do not know which method is more efficient, but the difference is probably negligible in this context
            if self.outputList:  #if we already have the value we are trying to create here (and we can tell because it is no longer the False value we initialized it to)
                return self.outputList  #we avoid repeating previous work and just output what we already have stored.  As will be shown in the test code below, the work required for this function can grow exponentially.  We only want to run it if it is requested AND we only ever want to run it the one time.
        except (AttributeError, NameError):
            letterList = []  #initialize an empty list to store a list of lists, where the outer list will correspond to the letters of the sequence and each inner list will represent all possibilities for that letter
            for letter in self.inputSeq:  #iterate over the input sequence
                letterList.append(self.complementLists[letter])  #add a list of possible bases to a growing list of possible bases at each position
            self.outputList = [''.join(letter) for letter in itertools.product(*letterList)]  #use the itertools module's product function to create the permutations (if this line seems strange to you, try looking up list comprehension in python and positional arguments, commonly called *args)
            return self.outputList #return the (potentially quite large) list