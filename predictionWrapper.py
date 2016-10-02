class Azimuth:
    
    def __init__(self, skipTest = False):  #may take a list of on target sequences or a single one.  Multiples should be comma separated
        import azimuth.model_comparison
        import numpy
        self.testedOnLoad = False
        if not skipTest:
            self.testModel()
            
    def validateSeq(self, seq):
        if not len(seq) == 30:
            raise PredictionError("Error with sequence %s, required sequence length for Azimuth prediction is 30 and this was length %s." %(seq, len(seq)))
        if not seq[25] == "G" and not seq[26] == "G":
            raise PredictionError("Error with sequence %s, a 'GG' PAM site is required." %(seq))
        for letter in seq:
            if not letter in "ATGC":
                raise PredictionError("Error with sequence %s, invalid character '%s'." %(seq, letter))
        return True
    
    def predict(self, onTargetSeqs):
        import azimuth.model_comparison  #should be redundant due to cached objects, keeping this here for portability
        import numpy  #same as above, keeping this here for portability
        onTargetSeqs = onTargetSeqs.replace("_","")  #cleans up any passed underscores
        onTargetSeqs = onTargetSeqs.upper()
        onTargetSeqs = onTargetSeqs.split(",")  #turns it into a list
        results = []
        for seq in onTargetSeqs:
            validated = self.validateSeq(seq)
        npSeqs = numpy.array(onTargetSeqs)
        negativeOnes = [-1] * len(onTargetSeqs)
        npResults = (azimuth.model_comparison.predict(npSeqs, numpy.array(negativeOnes), numpy.array(negativeOnes)))
        results = list(npResults)
        return results
    
    def testModel(self):
        testData = "GGGGATGCATGCATGCATGCATGCAGGAAA,AAAAATGCATGCATGCATGCATGCAGGGGG,GGGGATGCACGGATGCATGCATGCAGGAAA,GGGGATGCATGGGAGCATGCATGCAGGAAA,GGGGATGCATGCATGCAATGCTGCAGGAAA"
        expectedResult = [0.57222971207902751, 0.4944950744560187, 0.56998596931646772, 0.57108382789604972, 0.53155122847615977]
        toleranceRange = 0.001
        testResult = self.predict(testData)
        #print(testResult)
        testData = testData.split(",")  #splitting this here for error reporting
        for i in range(0, len(testResult)):
            if testResult[i] > expectedResult[i] + toleranceRange or testResult[i] < expectedResult[i] - toleranceRange:
                raise PredictionError("Azimuth model test failed.  Please check installation and model.  Failed on sequence number %s %s, testResult: %s, expected: %s" %(i, testData[i], testResult[i], expectedResult[i]))
        return True
    

class Elevation:
    
    def __init__(self, skipTest = False):
        import sys
        import os
        elevationPath = os.getcwd() + os.sep + "elevation"
        sys.path.append(elevationPath)
        elevationPath += os.sep + "elevation"
        sys.path.append(elevationPath)
        elevationPath += os.sep + "cmds"
        sys.path.append(elevationPath)
        import predict as elevation
        self.model = elevation.Predict()
        #touchFile = open("progressCounter/modelLoaded.progress", 'w')
        #touchFile.close()
        if not skipTest:
            self.testModel()
            
    def predict(self, onTarget, offTargets, blockSize = 0):
        import numpy
        onTarget = onTarget.replace("_","")
        offTargets = offTargets.replace("_","")
        onTarget = onTarget.upper()
        offTargets = offTargets.upper()
        validated = self.validateSeq(onTarget)
        offTargetList = offTargets.split(",")
        for seq in offTargetList:
            validated = self.validateSeq(seq)
        results = []
        counter = 0
        if blockSize < 1:
            blockSize = len(offTargetList)
        while offTargetList:
            offTargetBlock = offTargetList[0 : blockSize]
            #touchFile = open("progressCounter/start" + str(counter) + ".progress", 'w')
            #touchFile.close()
            print()
            npResults = self.model.execute([onTarget] * len(offTargetBlock), offTargetBlock)
            #touchFile = open("progressCounter/ran" + str(counter) + ".progress", 'w')
            #touchFile.close()
            del offTargetList[0 : blockSize]
            if not len(npResults["CFD"]) == len(npResults["linear-raw-stacker"]):
                raise RuntimeError("CFD result and stacker result should have the same number of elements.")
            for i in range(0,len(npResults["CFD"])):
                results.append((npResults["CFD"][i][0],npResults["linear-raw-stacker"][i]))  #append a tuple
            #touchFile = open("progressCounter/incorporated" + str(counter) + ".progress", 'w')
            #touchFile.close()
            counter += 1
        return results
        
    def validateSeq(self, seq):
        if not len(seq) == 23:
            raise PredictionError("Error with sequence %s, required sequence length for Azimuth prediction is 30 and this was length %s." %(seq, len(seq)))
        for letter in seq:
            if not letter in "ATGC":
                raise PredictionError("Error with sequence %s, invalid character '%s'." %(seq, letter))
        return True
    
    def testModel(self):
        onTarget = "ATGCATGCATGCATGCATGCAGG"
        offTargets = "ATGCATGCATGCTTGCATGCAGG,ATGCATCAATGCATGCATGCAGG,ATGCATGCATGCATGCGTGCAGG,ATGCATGCATGAATGCATGCAGG,ATGCATGCATGCATTCATGCAGG,ATGCCTGCATGCATGCATGCAGG,ATGCATAAATGCATGCATGCAGG,ATGCATGCATGCATGCATTTAGG,ATGCATGCACATATGCATGCAGG"
        expectedResult = [(0.29999999999999999, 0.35629573065038556), (0.44687500000000002, 0.058179509859210256), (0.176470588235, 0.24613468821874313), (0.71428571428599996, 0.5077846707094904), (0.14285714285699999, 0.22173111174356214), (0.5, 0.34317325393211062), (0.65000000000000002, 0.13330255841852942), (0.20000000000010001, 0.025756948041335392), (0.28717948717955383, 0.0093815891213724391)]
        toleranceRange = 0.001
        testResult = self.predict(onTarget, offTargets)
        #print(testResult)
        testData = offTargets.split(",")  #splitting this here for error reporting
        for i in range(0, len(testResult)):
            for j in range(0, len(testResult[i])):
                if testResult[i][j] > expectedResult[i][j] + toleranceRange or testResult[i][j] < expectedResult[i][j] - toleranceRange:
                    raise PredictionError("Elevation model test failed.  Please check installation and model.  Failed on sequence number %s %s, testResult: %s, expected: %s" %(i, testData[i], testResult[i], expectedResult[i]))
        print("Elevation Test Passed")
        return True
    
        
class Aggregation:
    
    def __init__(self, skipTest = False):
        import os
        import sys
        aggregationPath = os.getcwd() + os.sep + "aggregation"
        sys.path.append(aggregationPath)
        import aggregation
        import numpy
        import cPickle
        aggregationModelFileName = aggregationPath + os.sep + "aggregation_model.pkl"
        aggregationModelFile = open(aggregationModelFileName, 'rb')
        try:
            self.model, theOtherThing = cPickle.load(aggregationModelFile)
        except:
            import pickle
            aggregationModelFile.seek(0)
            self.model, theOtherThing = pickle.load(aggregationModelFile)
        aggregationModelFile.close()
        self.testedOnLoad = False
        if not skipTest:
            self.testModel()
            
    def validateElevationScores(self, scores):
        try:
            for score in scores:
                test = float(score.strip())
        except:  #this really should be a catch-all for anything not converting properly
            raise PredictionError("Error in elevation score list. Score %s was not a valid float." %(score))
        return True
    
    def validateGenicValues(self, genicValues):
        for value in genicValues:
            if not value.strip() in ["TRUE", "FALSE"]:
                raise PredictionError("Error in genic value list. Value %s was neither true nor false." %(score))
            
    def predict(self, stackerScores, elevationScores, genicValues):
        import aggregation
        import numpy
        stackerScoreList = stackerScores.split(",")
        stackerScoreList = [element.strip() for element in stackerScoreList]
        stackerScoreList = [float(element) for element in stackerScoreList]
        elevationScoreList = elevationScores.split(",")
        elevationScoreList = [element.strip() for element in elevationScoreList]
        self.validateElevationScores(elevationScoreList)
        elevationScoreList = [float(element) for element in elevationScoreList]
        genicValues = genicValues.upper()
        genicValuesStringList = genicValues.split(",")
        genicValuesStringList = [element.strip() for element in genicValuesStringList]
        self.validateGenicValues(genicValuesStringList)
        genicValuesList = []
        for value in genicValuesStringList:
            if value == "TRUE":
                genicValuesList.append(True)
            elif value == "FALSE":
                genicValuesList.append(False)
            else:
                raise PredictionError("Got an invalid genic value during prediction.  This should not have gotten through validation. Value: %s" %(value))
        # print(stackerScoreList)
        # print(elevationScoreList)
        # print(genicValuesList)
        npResults = aggregation.get_aggregated_score(numpy.array(stackerScoreList), numpy.array(elevationScoreList), numpy.array(genicValuesList), self.model)
        results = list(npResults)
        return results
    
    def testModel(self):
        stacker = "0.1,0.2,0.03"
        scores = "0.05,0.06,0.07"
        genicValues = "True,False,False"
        expectedResult = [0.72225885]
        toleranceRange = 0.001
        testResult = self.predict(stacker, scores, genicValues)
        #print(testResult)
        scores = scores.split(",")
        genicValues = genicValues.split(",")  #splitting this here for error reporting
        for i in range(0, len(testResult)):
            if testResult[i] > expectedResult[i] + toleranceRange or testResult[i] < expectedResult[i] - toleranceRange:
                raise PredictionError("Elevation model test failed.  Please check installation and model.  Failed on sequence number %s %s %s, testResult: %s, expected: %s" %(i, scores[i], genicValues[i], testResult[i], expectedResult[i]))
        return True


class PredictionError(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return repr(self.message)
    

def main():
    import sys
    import json
    args = sys.argv
    if len(args) == 1:
        aggregation = Aggregation()
        print("Aggregation loaded")
        del aggregation
        azimuth = Azimuth()
        print("Azimuth loaded")
        del azimuth
        elevation = Elevation()
        print("Elevation loaded")
        del elevation
        quit()
    if not len(args) == 2:
        raise PredictionError("This wrapper takes exactly one argument (the model to use). Any data shoudl be passed via STDIN. Found %s arguments." %(len(args) - 1))
    predictionModel = args[1].upper()
    data = sys.stdin.read().decode().strip().split(" ")
    if predictionModel == "AZIMUTH":
        if not len(data) == 1:
            raise PredictionError("Azimuth takes only one data string, %s were given: %s" %(len(data), data))
        azimuth = Azimuth()
        results = azimuth.predict(data[0])
    elif predictionModel == "ELEVATION":
        if not len(data) == 2:
            raise PredictionError("Elevation takes exactly two data strings, %s were given: %s" %(len(data), data))
        elevation = Elevation()
        results = elevation.predict(data[0], data[1])
    elif predictionModel == "AGGREGATION":
        if not len(data) == 3:
            raise PredictionError("Aggregation takes exactly three data strings, %s were given: %s" %(len(data), data))
        aggregation = Aggregation()
        results = aggregation.predict(data[0], data[1], data[2])
    else:
        raise PredictionError("No valid prediction model was listed. Options: azimuth, elevation, or aggregation. Passed value: %s." %(predictionModel))
    outputString = "<BEGIN_RESULTS>"
    outputString += json.dumps(results)
    outputString += "<END_RESULTS>"
    sys.stderr.write(outputString)
    sys.stderr.close()  #not sure if this is necessary, but it probably won't hurt
    print("")
    quit()

if __name__ == '__main__':
    main()