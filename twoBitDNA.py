#!/usr/bin/env python3

#By Michael Weinstein, 2016... still testing this version.  Please credit if used.

class TwoBitDNA(object):
    
    def __init__(self):
        import sys
        self.byteOrder = "little"
        self.byteLength = 8
        self.encodingKey = {"A":0,"C":1,"G":2,"T":3}  #mapping base to bit value
        self.decodingKey = {}  
        for base in list(self.encodingKey.keys()):  #reverse map of the above
            self.decodingKey[self.encodingKey[base]] = base
        self.cachedEncodingData = {}
        
    def validSeq(self, dna):   #Makes sure that the DNA seq submitted is upper case and only valid letters.  4-bit coding of degenerate sequence may be available in the future, but not planned.
        for letter in dna:
            if letter not in "ATGC":
                return False
        return True
    
    def encode(self, dna):
        dna = dna.upper()
        if not self.validSeq(dna):
            raise RuntimeError("DNA sequence for 2 bit conversion must only consist of ATGC")
        encoded = 0
        for letter in dna[::-1]:
            encoded = encoded << 2
            encoded += self.encodingKey[letter]
        return encoded
    
    def calculateBitLength(self, dna): #determines how many bits will be required based on sequence length (counted from a passed sequence or an integer) and returns a tuple of how many sequence bytes are needed and how many extra packing bytes are needed to get it to a multiple of 8 for storage
        try:
            dna = int(dna)
            dna = "T" * dna
        except ValueError:
            pass
        return len(dna) * 2
    
    def calculateByteLength(self, dna):
        try:
            dna = int(dna)
            dna = "T" * dna
        except ValueError:
            pass
        if len(dna) in self.cachedEncodingData:
            return self.cachedEncodingData[len(dna)]
        else:
            dnaByteLength = -1 * (-self.calculateBitLength(dna) // self.byteLength) #short cut for ceiling division with the double negatives
            self.cachedEncodingData[len(dna)] = dnaByteLength
            return dnaByteLength
    
    def decode(self, encodedDna, seqLength):
        if type(encodedDna) == list or type(encodedDna) == tuple:  #if the passed value was a list of packed values directly from a the struct, unpack them
            encodedDna = self.unpack(encodedDna, seqLength)
        if type(encodedDna) == bytes:
            encodedDna = int.from_bytes(encodedDna, self.byteOrder)
        decodedDna = ""
        checkBits = 3
        for i in range(0, seqLength):
            currentBaseValue = encodedDna & checkBits
            decodedDna += self.decodingKey[currentBaseValue]
            encodedDna = encodedDna >> 2
        return decodedDna
    
    def countMismatches(self, seq1, seq2, shortestSeqLength, endClip = 0, alreadyComparedBases = 0, alreadyFoundMismatches = 0): #can either take the unpacked sequence (preferred) or a list or tuple containing packed seq and seq length in that order
        if type(seq1) == bytes:
            seq1 = int.from_bytes(seq1, self.byteOrder)
        if type(seq2) == bytes:
            seq2 = int.from_bytes(seq2, self.byteOrder)
        variations = seq1 ^ seq2  #doing an xor on the two sequences will generate one or two 1 values where they differ and a pair of zeros where they match
        #peekvar = bin(variations)
        checkBits = 3 << alreadyComparedBases * 2  #just a binary 11, but by shifting it over two positions, we can do an AND operation that will return at least a single 1 value (evaluates to True) if there was a mismatch between the sequences at that doublet
        basesToCheck = shortestSeqLength - alreadyComparedBases - endClip
        mismatches = alreadyFoundMismatches
        if not variations: #handles the rare perfect match quickly
            return 0
        for i in range(0, basesToCheck):  #will check either the entire length of the shortest of the two sequences or that length minus the endClip
            #peekCheck = bin(checkBits)
            #peekRes = bin(variations & checkBits)
            if variations & checkBits:  #this does the AND operation on the moving check bits and variations to test each bit doublet for mismatching
                mismatches += 1
            checkBits = checkBits << 2
        return mismatches
    
    def countMismatches2(self, seq1, seq2, shortestSeqLength, endClip = 0): #can either take the unpacked sequence (preferred) or a list or tuple containing packed seq and seq length in that order
        if type(seq1) == bytes:
            seq1 = int.from_bytes(seq1, self.byteOrder)
        if type(seq2) == bytes:
            seq2 = int.from_bytes(seq2, self.byteOrder)
        variations = seq1 ^ seq2  #doing an xor on the two sequences will generate one or two 1 values where they differ and a pair of zeros where they match
        #peekvar = bin(variations)
        checkBits = 3  #just a binary 11, but by shifting it over two positions, we can do an AND operation that will return at least a single 1 value (evaluates to True) if there was a mismatch between the sequences at that doublet
        basesToCheck = shortestSeqLength - endClip
        mismatches = 0
        if not variations: #handles the rare perfect match quickly
            return 0
        for i in range(0, basesToCheck):  #will check either the entire length of the shortest of the two sequences or that length minus the endClip
            #peekCheck = bin(checkBits)
            #peekRes = bin(variations & checkBits)
            if variations & checkBits:  #this does the AND operation on the moving check bits and variations to test each bit doublet for mismatching
                mismatches += 1
            variations = variations >> 2
        return mismatches
    
    def withinMismatchTolerance(self, seq1, seq2, shortestSeqLength, mismatchTolerance, endClip = 0, alreadyComparedBases = 0, alreadyFoundMismatches = 0): #does the exact same thing as mismatch counting, except this will stop if a mismatch threshold is reached and return False, otherwise it will return True.  Optimized operation for filtering.
        if type(seq1) == bytes:
            seq1 = int.from_bytes(seq1, self.byteOrder)
        if type(seq2) == bytes:
            seq2 = int.from_bytes(seq2, self.byteOrder)  
        variations = seq1 ^ seq2
        #peekvar = bin(variations)
        checkBits = 3 << alreadyComparedBases * 2 #binary will be "11"
        basesToCheck = shortestSeqLength - alreadyComparedBases - endClip
        mismatches = alreadyFoundMismatches
        if not variations: #handles the rare perfect match quickly
            return True
        if variations and mismatchTolerance == 0:
            return False
        for i in range(0, basesToCheck):
            #peekCheck = bin(checkBits)
            #peekRes = bin(variations & checkBits)
            if variations & checkBits:
                mismatches += 1
                if mismatches > mismatchTolerance:
                    return False
            checkBits = checkBits << 2
        return True
    
    def withinMismatchToleranceAndCount(self, seq1, seq2, shortestSeqLength, mismatchTolerance, endClip = 0, alreadyComparedBases = 0, alreadyFoundMismatches = 0): #does the exact same thing as mismatch counting, except this will stop if a mismatch threshold is reached and return False, otherwise it will return True.  Optimized operation for filtering.
        if type(seq1) == bytes:
            seq1 = int.from_bytes(seq1, self.byteOrder)
        if type(seq2) == bytes:
            seq2 = int.from_bytes(seq2, self.byteOrder)
        variations = seq1 ^ seq2
        # peekCvar = bin(variations)
        checkBits = 3 #binary will be "11"
        #checkBits = checkBits << (endClip * 2)
        basesToCheck = shortestSeqLength - alreadyComparedBases
        mismatches = alreadyFoundMismatches
        mismatchesForQualification = alreadyFoundMismatches
        if not variations: #handles the rare perfect match quickly
            return 0
        if variations and mismatchTolerance == 0:
            return -1
        for i in range(0, basesToCheck):
            # peekARef = bin(seq1)
            # peekBProb = bin(seq2)
            # peekDCheck = bin(checkBits)
            # peekERes = bin(variations & checkBits)
            if variations & checkBits:
                mismatches += 1
                if i < basesToCheck - endClip:
                    mismatchesForQualification += 1
                if mismatchesForQualification > mismatchTolerance:
                    return -1
            checkBits = checkBits << 2
        return mismatches
    
def stringComp(seq1, seq2, length):
    mismatches = 0
    for i in range(0, length):
        if not seq1[i] == seq2[i]:
            mismatches += 1
    return mismatches
    
def testCode():
    import datetime
    import struct
    import io
    import pickle
    seq = "ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT"
    seq2 = "ATGTTCCTACGTACGTACCT"


#testCode()
