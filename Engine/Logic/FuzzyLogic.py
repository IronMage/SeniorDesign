import unittest
from FuzzyRules import *

def distRule(inputSet, outputSet):
    xRange = inputSet.getResults("DX")
    yRange = inputSet.getResults("DY")

    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[0] * 5)
    outputSet.addToOwnership("CONTROLLER", "A"    , xRange[1] * 20)
    outputSet.addToOwnership("CONTROLLER", "RIGHT", xRange[2] * 10)

    outputSet.addToOwnership("CONTROLLER", "RIGHT", yRange[0] * 5)
    outputSet.addToOwnership("CONTROLLER", "A"    , yRange[1] * 10)
    outputSet.addToOwnership("CONTROLLER", "RIGHT", yRange[2] * 10)

    p = ["A", "B", "UP", "DOWN", "LEFT", "RIGHT"]
    #print(p)
    #print(outputSet.getResults("CONTROLLER"))


class FuzzyLogic:
    def __init__(self):
        self.inputSet = FuzzySets()
        self.outputSet = FuzzySets()
        self.ruleSet = FuzzyRuleSet(self.inputSet, self.outputSet)
        #self.fuzzifier = Fuzzifier()
        #sel.defuzzifier = Defuzzifier()
    
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

    def testingFunction(self):
        self.inputSet.getOwnership("DX", 1)
        self.inputSet.getOwnership("DY", 30)

    def run(self):
        #self.fuzzifier.getInput(inputSet)
        self.ruleSet.runRules()
        #self.fuzzifier.doOutput(outputSet)

class TestFuzzyLogic(unittest.TestCase):
    def testFuzzyLogic(self):       
        fz = FuzzyLogic()
        fz.setUpInputs()
        fz.setUpOutputs()
        fz.setUpRules()

        fz.testingFunction()

        fz.run()

if __name__ == '__main__':
    unittest.main()