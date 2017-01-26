import unittest
from FuzzyRules import *

class FuzzyLogic:
    def __init__(self):
        self.inputSet = FuzzySet()
        self.outputSet = FuzzySet()
        self.ruleSet = FuzzyRuleSet()
        #self.fuzzifier = Fuzzifier()
        #sel.defuzzifier = Defuzzifier()
    
    def setUpInputs(self):
        #Insert input set creation here
        print("in")

    def setUpOutputs(self):
        #Insert output set creation here
        print("out")

    def setUpRules(self):
        #Insert rules creation here
        print("rule")

    def run(self):
        #self.fuzzifier.getInput(inputSet)
        self.ruleSet.runRules()
        #self.fuzzifier.doOutput(outputSet)