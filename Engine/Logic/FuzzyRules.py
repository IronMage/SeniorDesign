from FuzzySet import *
import unittest
class Rule:
    def __init__(self, ruleFunction, requiredInputs, requiredOutputs):
        self.function = ruleFunction
        self.inputs = requiredInputs
        self.outputs = requiredOutputs
    def runRule(self):
        return self.function()
    def checkRule(self, inputSets, outputSets):
        for s in self.inputs:
            if(inputSets.exists(s)):
                pass
            else:
                raise ValueError("Required input set " + str(s) + " does not exist in the current master input set.")
        for s in self.outputs:
            if(outputSets.exists(s)):
                pass
            else:
                raise ValueError("Required output set " + str(s) + " does not exist in the current master output set.")

class RuleSet:
    def __init__(self, inputSets, outputSets):
        self.rules = []
        self.inputs = inputSets
        self.outputs = outputSets
    def addRule(self, newRule):
        if(isinstance(newRule, Rule)):
            self.rules.append(newRule)
        else:
            raise ValueError("Trying to add a new rule with incorrect typing." + str(type(newRule)))
    def getRules(self):
        return self.rules 
    def runRules(self):
        for r in self.rules:
            r.checkRule(self.inputs, self.outputs)
            r.runRule()
    def checkRules(self):
        for r in self.rules:
            r.checkRule(self.inputs, self.outputs)


def testingRuleFunction():
    #print("Entered testingRuleFunction")
    return True

def testingInputSetCreation():
    fz = FuzzySets()
    t1 = TrapazoidalGraph(3, 0, 2, 4, 6, 4, 6, 6, 8, 6, 8, 10, 12)
    t2 = TriangularGraph(3, 0, 4, 2, 10, 8, 12)

    fz.addSet(t1, "IN1")
    fz.addSet(t2, "IN2")

    return fz

def testingOutputSetCreation():
    fz = FuzzySets()
    t3 = TriangularGraph(3, 0, 4, 2, 10, 8, 12)

    fz.addSet(t3, "O1")

    return fz


class TestFuzzyRules(unittest.TestCase):
    def testRule(self):
        print("\nTESTING FUZZY RULES")
        r1 = Rule(testingRuleFunction, ["IN1", "IN2"], ["O1"])  #Create a rule
        inSet = FuzzySets()                                     #Empty set
        outSet = FuzzySets()

        with self.assertRaises(ValueError):                     #Check to make sure there are no false positives
            r1.checkRule(inSet, outSet)          

        inSet = testingInputSetCreation()                       #Get the actual testing set
        outSet = testingOutputSetCreation()
        r1.checkRule(inSet, outSet)                             #Check to make sure everything worked

        self.assertTrue(r1.runRule())

    def testRuleSet(self):       
        print("\nTESTING FUZZY RULES WRAPPER") 
        inSet = testingInputSetCreation()                       #Get the actual testing set
        outSet = testingOutputSetCreation()

        fzRules = RuleSet(inSet, outSet)                        #Create a rule set

        t123 = 18000                                            #Create a dummy variable to check the type checking for the rule set
        with self.assertRaises(ValueError):
            fzRules.addRule(t123)

        r1 = Rule(testingRuleFunction, ["IN1", "IN2"], ["O1"])  #Create a rule

        fzRules.addRule(r1)
        self.assertEqual(r1, fzRules.getRules()[0])             #Make sure the rule and the first rule of the set are the same

        fzRules.runRules()                                      #Make sure you can check and run the rules



if __name__ == '__main__':
    unittest.main()