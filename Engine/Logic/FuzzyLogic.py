import unittest
from FuzzyRules import *
from Defuzzifier import *
from Fuzzifier import *

def distRule(inputSet, outputSet):
    xRange = inputSet.getResults("DX")
    yRange = inputSet.getResults("DY")

    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[0] * 5)
    outputSet.addToOwnership("CONTROLLER", "A", xRange[1] * 20)
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[2] * 10)

    outputSet.addToOwnership("CONTROLLER", "RIGHT", yRange[0] * 5)
    outputSet.addToOwnership("CONTROLLER", "A"    , yRange[1] * 10)
    outputSet.addToOwnership("CONTROLLER", "RIGHT", yRange[2] * 10)

class FuzzyLogic:
    def setUpInputs(self):
        dx = TrapazoidalGraph(3, -100, -100, -50, -25, -50, -10, 10, 50, 25, 50, 100, 100)
        dy = TrapazoidalGraph(3, -100, -100, -50, -25, -50, -10, 10, 50, 25, 50, 100, 100)
        self.inputSet.addSet(dx, "DX")
        self.inputSet.addSet(dy, "DY")

    def setUpOutputs(self):
        controller = BarGraph(6, "A", "B", "UP", "DOWN", "LEFT", "RIGHT")
        self.outputSet.addSet(controller, "CONTROLLER")

    def setUpRules(self):
        dRule = FuzzyRule(distRule, ["DX", "DY"], ["CONTROLLER"])
        self.ruleSet.addRule(dRule)

    def __init__(self):
        self.inputSet = FuzzySets()
        self.outputSet = FuzzySets()
        self.ruleSet = FuzzyRuleSet(self.inputSet, self.outputSet)
        self.fuzzifier = Fuzzifier(self.inputSet)
        self.defuzzifier = Defuzzifier(self.outputSet)
        self.setUpInputs()
        self.setUpOutputs()
        self.setUpRules()

    def testingFunction(self):
        self.inputSet.getOwnership("DX", 1)
        self.inputSet.getOwnership("DY", 30)

    def run(self, message):
        numEnemies = self.fuzzifier.parseMessage(message)
        for x in range(numEnemies):
            self.fuzzifier.getInput(x)
            self.ruleSet.runRules()
        selectedOutput = self.defuzzifier.selectOutput()
        self.outputSet.clearOwnership("CONTROLLER")
        return selectedOutput


class TestFuzzyLogic(unittest.TestCase):
    def testFuzzyLogic(self):       
        fz = FuzzyLogic()

        fz.testingFunction()

        message = "2,3,4,12,-3,4,-5,-1,9,6,2"

        fz.run(message)

if __name__ == '__main__':
    unittest.main()