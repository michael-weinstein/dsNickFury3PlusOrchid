#!/usr/bin/env python3
import os
import pickle
import dataPacker

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

genomeDirectory = "genomes/GGN_NNNNNNNNNNNNNNNNNNNN.DM6.FRUITFLY/"
targetBin = genomeDirectory + os.sep + "targets" + os.sep + "ATATT.bct"
encodingInfoFileName = genomeDirectory + os.sep + "genCodeData.pkl"
if not os.path.isfile(encodingInfoFileName):
    raise RuntimeError("No encoding data file found at %s" %(encodingInfoFileName), end = "\r")
encodingInfoFile = open(encodingInfoFileName, 'rb')
encodingInfo = pickle.load(encodingInfoFile)
encodingInfoFile.close()
twoBitHandler = dataPacker.DataPacker(encodingInfo.compressionScheme, encodingInfo.pamLength, encodingInfo.guideLength, encodingInfo.guideExtendLength, encodingInfo.pamExtendLength)
siteBytesFile = open(targetBin, 'rb')
siteBytes = siteBytesFile.read()
siteBytesFile.close()
sites = []
siteByteLength = twoBitHandler.siteDataByteLength
position = 0
while position < len(siteBytes):
    currentSiteBytes = siteBytes[position : position + siteByteLength]
    siteData = twoBitHandler.decodeData(currentSiteBytes)
    sites.append([siteData.sequence[::-1], encodingInfo.contigDenumerationTable[siteData.enumeratedContig], str(siteData.start), str(siteData.end)])
    position += siteByteLength
for site in sites:
    print("\t".join(site))