import unittest
from FuzzyRules import *
from Defuzzifier import *
from Fuzzifier import *

'''
Moves mario based on the positions of surrounding enemies
'''
def distRule(inputSet, outputSet):
    xRange = inputSet.getResults("DX")
    yRange = inputSet.getResults("DY")

    xPosFar     = xRange[4]
    xPosClose   = xRange[3]
    xZero       = xRange[2]
    xNegClose   = xRange[1]
    xNegFar     = xRange[0]

    yPosFar     = yRange[4]
    yPosClose   = yRange[3]
    yZero       = yRange[2]
    yNegClose   = yRange[1]
    yNegFar     = yRange[0]


    if(xRange[0] is None or yRange[0] is None):
        return False
    #Line 3 handles all yPosFar cases
    outputSet.addToOwnership("CONTROLLER", "RIGHT", yPosFar)
    outputSet.addToOwnership("CONTROLLER", "B", yPosFar)
    #Line 8 handles all yPosClose cases
    outputSet.addToOwnership("CONTROLLER", "RIGHT", yPosClose)
    outputSet.addToOwnership("CONTROLLER", "B", yPosClose)
    #Line 13
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xPosFar * yZero)
    outputSet.addToOwnership("CONTROLLER", "B", xPosFar * yZero)
    #Line 14
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xPosClose * yZero)
    outputSet.addToOwnership("CONTROLLER", "A", xPosClose * yZero)
    #Line 15
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xZero * yZero)
    outputSet.addToOwnership("CONTROLLER", "A", xZero * yZero)
    #Line 16
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xNegClose * yZero)
    #Line 17 handles all x neg far cases
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xNegFar)
    outputSet.addToOwnership("CONTROLLER", "B", xPosFar)
    #Line 18
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xPosFar * yNegClose)
    outputSet.addToOwnership("CONTROLLER", "B", xPosFar * yNegClose)
    #Line 19
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xPosClose * yNegClose)
    #Line 20
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xZero * yNegClose)
    outputSet.addToOwnership("CONTROLLER", "A", xZero * yNegClose)
    #Line 21
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xNegClose * yNegClose)
    #Line 22
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xNegFar * yNegClose)
    outputSet.addToOwnership("CONTROLLER", "B", xNegFar * yNegClose)
    #Line 23
    outputSet.addToOwnership("CONTROLLER", "RIGHT", yNegFar)
    outputSet.addToOwnership("CONTROLLER", "B", yNegFar)
    
    
'''
Moves Mario to the right while there are no enemies around
'''
def moveMario(inputSet, outputSet):
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

    def __init__(self):
        self.inputSet = FuzzySets()
        self.outputSet = FuzzySets()
        self.setUpInputs()
        self.setUpOutputs()
        self.ruleSet = FuzzyRuleSet(self.inputSet, self.outputSet)
        self.setUpRules()
        self.fuzzifier = Fuzzifier(self.inputSet)
        self.defuzzifier = Defuzzifier(self.outputSet)

    def testingFunction(self):
        self.inputSet.getOwnership("DX", 1)
        self.inputSet.getOwnership("DY", 30)

    def run(self, message):
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

class TestFuzzyLogic(unittest.TestCase):
    def testFuzzyLogic(self):       
        fz = FuzzyLogic()

        fz.testingFunction()

        message = "2,3,4,12,-3,4,-5,-1,9,6,2"

        fz.run(message)

if __name__ == '__main__':
    unittest.main()