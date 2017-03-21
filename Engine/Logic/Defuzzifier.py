#Defuzzifier
#
'''
Receives information from the Python UDP Client
Begins computing which button to press
'''

#Insert current state saving here.
import unittest
from FuzzySet import *

class Defuzzifier:
    def __init__(self, outputSet):
        self.outputSet = outputSet
        self.lastSelected = ["",""]*5

    def shiftLeftList(self):
        length = len(self.lastSelected)
        for x in range(length - 1):
            self.lastSelected[length - x] = self.lastSelected[length - 1 - x] 

    def limitA(self, n1, n2):
        allAs = True
        for x in range(len(self.lastSelected)):
            if (self.lastSelected[x] != "A"):
                allAs = False
                break
            else:
                continue
        if(not allAs):
            return n1, n2
        elif(n1 == "A"):
            n1 = n2
            n2 = None
            return n1, n2
        else:
            return n1, None
        
    def checkConflicting(self, n1, n2):
        n1,n2 = limitA(n1,n2)
        if(n2 is None):
            return True
        if((n1 == "RIGHT" and n2 == "LEFT") or (n1 == "LEFT" and n2 == "RIGHT")):
            return True
        else if((n1 == "UP" and n2 == "DOWN")  or (n1 == "DOWN" and n2 == "UP")):
            return True
        else:
            return False

    def selectOutput(self):
        results = self.outputSet.getResults("CONTROLLER")
        s = self.outputSet.getSets()
        names = self.outputSet.getNames("CONTROLLER")

        maxName = ""
        maxValue = -1
        runnerUpName = ""
        runnerUpValue = -1;

        for i in range(len(results)):
            if(results[i] > runnerUpValue and results[i] > maxValue):
                runnerUpValue = maxValue
                runnerUpName = maxName
                maxValue = results[i]
                maxName = names[i]
            else if(results[i] > runnerUpValue):
                runnerUpValue = results[i]
                runnerUpName = names[i]
            else:
                continue
        if(checkConflicting(maxName, runnerUpName)):
            return maxName, None
        else:
            return maxName,runnerUpName


from random import randint
class TestDefuzzifier(unittest.TestCase):
    def testFuzzySetWrapper(self):
        print("\nTESTING DEFUZZIFIER")
        fz = FuzzySets()                                                        #Make an empty set to fill

        controller = BarGraph(6, "A", "B", "UP", "DOWN", "LEFT", "RIGHT")
        fz.addSet(controller, "CONTROLLER")
        A = randint(0,9)
        B = randint(0,9)
        UP = randint(0,9)
        DWN = randint(0,9)
        LFT = randint(0,9)
        RGT = randint(0,9)

        myList = [A, B, UP, DWN, LFT, RGT]
        myNames = ["A", "B", "UP", "DOWN", "LEFT", "RIGHT"]

        dFz = Defuzzifier(fz)

        fz.addToOwnership("CONTROLLER", "A", A)
        fz.addToOwnership("CONTROLLER", "B", B)
        fz.addToOwnership("CONTROLLER", "UP", UP)
        fz.addToOwnership("CONTROLLER", "DOWN", DWN)
        fz.addToOwnership("CONTROLLER", "LEFT", LFT)
        fz.addToOwnership("CONTROLLER", "RIGHT", RGT)

        ret = dFz.selectOutput()
        value = 0
        for i in range(len(myList)):
            if(ret == myNames[i]):
                value = myList[i]
            else:
                continue

        self.assertEqual(value, max(myList))

if __name__ == '__main__':
    unittest.main()