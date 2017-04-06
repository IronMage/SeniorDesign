import unittest
import numpy as np
from FuzzyRules import *
from Defuzzifier import *
from Fuzzifier import *

'''
Moves mario based on the positions of surrounding enemies
'''

def distRule(inputSet, outputSet, weights):
    xRange = inputSet.getResults("DX")
    yRange = inputSet.getResults("DY")

    # xPosFar     = xRange[4]
    # xPosClose   = xRange[3]
    # xZero       = xRange[2]
    # xNegClose   = xRange[1]
    # xNegFar     = xRange[0]

    # yPosFar     = yRange[4]
    # yPosClose   = yRange[3]
    # yZero       = yRange[2]
    # yNegClose   = yRange[1]
    # yNegFar     = yRange[0]


    if(xRange[0] is None or yRange[0] is None):
        return False


    choices = ["A", "B", "UP", "DOWN", "LEFT", "RIGHT"]
    xIdx = 0
    for x in xRange:
        yIdx = 0
        for y in yRange:
            cIdx = 0
            for c in choices:
                #print(str(xIdx) + " " + str(yIdx) + " " + c + " " + str(weights[xIdx][yIdx][cIdx]))
                outputSet.addToOwnership("CONTROLLER", c, x * y * (weights[xIdx][yIdx][cIdx])) 
                cIdx += 1
            yIdx += 1
        xIdx += 1
'''
Moves Mario to the right while there are no enemies around
'''
def moveMario(inputSet, outputSet, weights):
    #print("ENTERED MOVE MARIO")
    xRange = inputSet.getResults("MARIODX")
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[0] * .5)
    '''
    print(outputSet.getNames("CONTROLLER"))
    print(outputSet.getResults("CONTROLLER"))
    '''

class FuzzyLogic:
    def setUpInputs(self):
        #Number of ranges, start point, start plateau point, end plateau point, end point
        dx = TrapazoidalGraph(5, -200, -200, -150, -120, -150, -120, -80, -30, -80, -50, 30, 80, 30, 80, 120, 150, 120, 150, 200, 200)
        dy = TrapazoidalGraph(5, -200, -200, -150, -120, -150, -120, -80, -30, -80, -30, 30, 80, 30, 80, 120, 150, 120, 150, 200, 200)
        self.inputSet.addSet(dx, "DX")
        self.inputSet.addSet(dy, "DY")
        marioDx = TrapazoidalGraph(1, -10, -10, 10, 10)
        self.inputSet.addSet(marioDx, "MARIODX")

    def setUpOutputs(self):
        controller = BarGraph(6, "A", "B", "UP", "DOWN", "LEFT", "RIGHT")
        self.outputSet.addSet(controller, "CONTROLLER")

    def setUpRules(self):
        dRule = FuzzyRule(distRule, ["DX", "DY"], ["CONTROLLER"])
        #print("SET UP " + dRule.getName())
        self.ruleSet.addRule(dRule)
        mRule = FuzzyRule(moveMario, ["MARIODX"], ["CONTROLLER"])
        #print("SET UP " + mRule.getName())
        self.ruleSet.addRule(mRule)

    def setupDefaultWeights(self):        
        xIdx = 0
        yIdx = 0
        with open('weightDefaults.txt', 'r') as txt:
            for line in txt:
                if(yIdx > 4):
                    yIdx = 0
                    xIdx += 1
                tokens = line.split(" ")
                cIdx = 0
                for element in tokens:
                    self.weights[xIdx][yIdx][cIdx] = int(element)
                    cIdx += 1
                yIdx += 1
        txt.close()

    def __init__(self):
        self.inputSet = FuzzySets()
        self.outputSet = FuzzySets()
        self.setUpInputs()
        self.setUpOutputs()
        self.weights = [[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
                        [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],
                        [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]],[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]]
        self.setupDefaultWeights()
        self.ruleSet = FuzzyRuleSet(self.inputSet, self.outputSet, self.weights)
        self.setUpRules()
        self.fuzzifier = Fuzzifier(self.inputSet)
        self.defuzzifier = Defuzzifier(self.outputSet)
        self.currentMessage = ""
    def testingFunction(self):
        self.inputSet.getOwnership("DX", 1)
        self.inputSet.getOwnership("DY", 30)

    def run(self, message):
        self.currentMessage = message
        numEnemies = self.fuzzifier.parseMessage(message)
        self.fuzzifier.getMario()
        if(numEnemies > 0):
            for x in range(numEnemies):
                self.fuzzifier.getEnemies(x)
                self.ruleSet.runRules()
        else:
            self.ruleSet.runRules()
        out1, out2 = self.defuzzifier.selectOutput()
        self.outputSet.clearOwnership("CONTROLLER")
        return out1, out2

    def neuralNetworkRun(self):
        s1, s2 = self.run(self.currentMessage)
        names = ["A", "B", "UP", "DOWN", "LEFT", "RIGHT"]
        array = [0, 0, 0, 0, 0, 0]
        if(s2 is not None):
            for i in range(len(names)):
                if(s1 == names[i] or s2 == names[i]):
                    array[i] = 1
                else:
                    continue
        else:
            for i in range(len(names)):
                if(s1 == names[i]):
                    array[i] = 1
        numpyArray = np.array(array)
        return numpyArray

    def getWeightLength(self):
        numRows = len(self.weights)
        numCols = len(self.weights[0])
        numElements = len(self.weights[0][0])
        return (numRows * numCols * numElements)

    def get1DWeights(self):
        tmpArray = []
        for x in range(len(self.weights)):
            for y in range(len(self.weights[0])):
                for w in range(len(self.weights[0][0])):
                    tmpArray.append(self.weights[x][y][w])
        #print(tmpArray)
        npTmp = np.array(tmpArray)
        return npTmp

    def setWeights(self, oneDWeights):
        currentIdx = 0
        for x in range(len(self.weights)):
            for y in range(len(self.weights[0])):
                for w in range(len(self.weights[0][0])):
                    self.weights[x][y][w] = oneDWeights[currentIdx]
                    currentIdx += 1


class TestFuzzyLogic(unittest.TestCase):
    def testFuzzyLogic(self):       
        fz = FuzzyLogic()

        fz.testingFunction()

        message = "2,3,4,12,-3,4,-5,-1,9,6,2"

        fz.run(message)

        #print(fz.get1DWeights())

if __name__ == '__main__':
    unittest.main()