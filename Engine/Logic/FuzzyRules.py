from FuzzySet import *
import unittest
class FuzzyRule:
    def __init__(self, ruleFunction, requiredInputs, requiredOutputs):
        self.function = ruleFunction
        self.inputs = requiredInputs
        self.outputs = requiredOutputs
    def runRule(self, inputSets, outputSets, weights):
        return self.function(inputSets, outputSets, weights)
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
    def getName(self):
        return self.function.__name__

class FuzzyRuleSet:
    def __init__(self, inputSets, outputSets, weights):
        self.rules = []
        self.inputs = inputSets
        self.outputs = outputSets
        self.weights = weights
    def addRule(self, newRule):
        if(isinstance(newRule, FuzzyRule)):
            self.rules.append(newRule)
        else:
            raise ValueError("Trying to add a new rule with incorrect typing." + str(type(newRule)))
    def getRules(self):
        return self.rules 
    def runRules(self):
        #print(self.rules)
        names = []
        returnValues = []
        for x in range(len(self.rules)):
            names.append(self.rules[x].getName())
            self.rules[x].checkRule(self.inputs, self.outputs)
            returnValues.append(self.rules[x].runRule(self.inputs, self.outputs, self.weights))
        #print("RAN " + str(names))
        return returnValues
    def checkRules(self):
        for x in range(len(self.rules)):
            self.rules[x].checkRule(self.inputs, self.outputs)


def testingRuleFunction(inputSets, outputSets, weights):
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
        r1 = FuzzyRule(testingRuleFunction, ["IN1", "IN2"], ["O1"])  #Create a rule
        inSet = FuzzySets()                                     #Empty set
        outSet = FuzzySets()

        with self.assertRaises(ValueError):                     #Check to make sure there are no false positives
            r1.checkRule(inSet, outSet)          

        inSet = testingInputSetCreation()                       #Get the actual testing set
        outSet = testingOutputSetCreation()
        r1.checkRule(inSet, outSet)                             #Check to make sure everything worked
        weights = []

        self.assertTrue(r1.runRule(inSet, outSet, weights))

    def testFuzzyRuleSet(self):       
        print("\nTESTING FUZZY RULES WRAPPER") 
        inSet = testingInputSetCreation()                       #Get the actual testing set
        outSet = testingOutputSetCreation()
        weights = []

        fzRules = FuzzyRuleSet(inSet, outSet, weights)                        #Create a rule set

        t123 = 18000                                            #Create a dummy variable to check the type checking for the rule set
        with self.assertRaises(ValueError):
            fzRules.addRule(t123)

        r1 = FuzzyRule(testingRuleFunction, ["IN1", "IN2"], ["O1"])  #Create a rule

        fzRules.addRule(r1)
        self.assertEqual(r1, fzRules.getRules()[0])             #Make sure the rule and the first rule of the set are the same

        self.assertEqual(fzRules.runRules()[0], r1.runRule(inSet, outSet, weights))                                  #Make sure you can check and run the rules



if __name__ == '__main__':
    unittest.main()