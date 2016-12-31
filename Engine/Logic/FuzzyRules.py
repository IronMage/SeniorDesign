class Rule:
    def __init__(self, ruleFunction, requiredInputs, requiredOutputs):
        self.function = ruleFunction
        self.inputs = requiredInputs
        self.outputs = requiredOutputs
    def runRule(self):
        self.function()
    def checkRule(self, inputSets, outputSets):
        for s in self.inputs:
            if(inputSets.exists(s)):
                pass
            else:
                raise Exception("Required input set " + str(s) + " does not exist in the current master input set.")
        for s in self.outputs:
            if(outputSets.exists(s)):
                pass
            else:
                raise Exception("Required output set " + str(s) + " does not exist in the current master output set.")

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
            r.runRule()
    def checkRules(self):
        for r in self.rules:
            r.checkRule(self.inputs, self.outputs)
