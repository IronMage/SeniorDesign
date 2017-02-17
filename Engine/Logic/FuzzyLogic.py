import unittest
from FuzzyRules import *

def distRule():
    

class FuzzyLogic:
    def __init__(self):
        self.inputSet = FuzzySets()
        self.outputSet = FuzzySets()
        self.ruleSet = FuzzyRuleSet(self.inputSet, self.outputSet)
        #self.fuzzifier = Fuzzifier()
        #sel.defuzzifier = Defuzzifier()
    
    def setUpInputs(self):
        dx = TrapaziodalGraph(3, -100, -100, -50, -25, -50, -10, 10, 50, 25, 50, 100, 100)
        dy = TrapaziodalGraph(3, -100, -100, -50, -25, -50, -10, 10, 50, 25, 50, 100, 100)
        self.inputSet.addSet(dx, "DX")
        self.inputSet.addSet(dy, "DY")

    def setUpOutputs(self):
        controller = BarGraph(6, "A", "B", "UP", "DOWN", "LEFT", "RIGHT")
        self.outputSet.addSet(controller, "CONTROLLER")

    def setUpRules(self):
        distRule = FuzzyRule(["DX", "DY"], ["CONTROLLER"])

    def run(self):
        #self.fuzzifier.getInput(inputSet)
        self.ruleSet.runRules()
        #self.fuzzifier.doOutput(outputSet)