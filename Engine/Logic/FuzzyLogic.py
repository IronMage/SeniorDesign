import unittest
from FuzzyRules import *
from Defuzzifier import *
from Fuzzifier import *

def distRule(inputSet, outputSet):
    xRange = inputSet.getResults("DX")
    yRange = inputSet.getResults("DY")
    print(xRange)
    print(yRange)

    #print("xRange type " + str(type(xRange)) + "yRange type " + str(type(yRange)))
    if(xRange[0] is None or yRange[0] is None):
        return False
    '''
    print("dist CURRENT VALUES:")
    print(outputSet.getNames("CONTROLLER"))
    print(outputSet.getResults("CONTROLLER"))
    '''
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[0])
    outputSet.addToOwnership("CONTROLLER", "A",     xRange[1])
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[2])

    outputSet.addToOwnership("CONTROLLER", "RIGHT", yRange[0])
    outputSet.addToOwnership("CONTROLLER", "A"    , yRange[1] * -1)
    outputSet.addToOwnership("CONTROLLER", "RIGHT", yRange[2])
    '''
    print("AFTER DIST VALUES:")
    print(outputSet.getNames("CONTROLLER"))
    print(outputSet.getResults("CONTROLLER"))
    '''

def moveMario(inputSet, outputSet):
    #print("ENTERED MOVE MARIO")
    xRange = inputSet.getResults("MARIODX")
    '''
    print("xRange type " + str(type(xRange)))

    print("move CURRENT VALUES:")
    print(outputSet.getNames("CONTROLLER"))
    print(outputSet.getResults("CONTROLLER"))
    '''
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[0] * .5)
    print(outputSet.getNames("CONTROLLER"))
    print(outputSet.getResults("CONTROLLER"))

class FuzzyLogic:
    def setUpInputs(self):
        dx = TrapazoidalGraph(3, -100, -100, -50, -25, -50, -10, 10, 50, 25, 50, 100, 100)
        dy = TrapazoidalGraph(3, -100, -100, -50, -25, -50, -50, 50, 50, 25, 50, 100, 100)
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