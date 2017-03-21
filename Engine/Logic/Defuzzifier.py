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
        self.lastSelected = [""]*8

    def shiftLeftList(self):
        length = len(self.lastSelected)
        for x in range(length - 2):
            self.lastSelected[x] = self.lastSelected[x+1] 

    def enterList(self, n1, n2):
        length = len(self.lastSelected)
        if(n2 is None):
            self.lastSelected[length - 2] = n1
            self.lastSelected[length - 1] = ""
        else:
            self.lastSelected[length - 2] = n1
            self.lastSelected[length - 1] = n2

    def limitA(self, n1, n2):
        countAs = 0
        for x in range(len(self.lastSelected)):
            if (self.lastSelected[x] == "A"):
                countAs += 1
            else:
                continue
        #print("COUNTED " + str(countAs) + " NUMBER OF A'S")
        if(countAs < (len(self.lastSelected) / 2)):
            #print("RETURNING " + n1 + " AND " + n2)
            return n1, n2
        elif(n1 == "A"):
            n1 = n2
            n2 = None
            #print("RETURNING " + n1 + " AND None")
            return n1, n2
        else:
            #print("RETURNING " + n1 + " AND None")
            return n1, None
        
    def checkConflicting(self, n1, n2):
        #print("LAST SELECTED OUTPUTS:")
        #print(self.lastSelected)
        if(n2 is None):
            return True
        if((n1 == "RIGHT" and n2 == "LEFT") or (n1 == "LEFT" and n2 == "RIGHT")):
            return True
        elif((n1 == "UP" and n2 == "DOWN")  or (n1 == "DOWN" and n2 == "UP")):
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
            elif(results[i] > runnerUpValue):
                runnerUpValue = results[i]
                runnerUpName = names[i]
            else:
                continue
        if(self.checkConflicting(maxName, runnerUpName)):
            maxName, runnerUpName = self.limitA(maxName, runnerUpName)
            self.shiftLeftList()
            self.shiftLeftList()
            self.enterList(maxName, None)
            return maxName, None
        else:
            maxName, runnerUpName = self.limitA(maxName, runnerUpName)
            self.shiftLeftList()
            self.shiftLeftList()
            self.enterList(maxName,runnerUpName)
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

        ret1, ret2 = dFz.selectOutput()
        value = 0
        for i in range(len(myList)):
            if(ret1 == myNames[i]):
                value = myList[i]
            else:
                continue
        #print(myList)
        self.assertEqual(value, max(myList))

if __name__ == '__main__':
    unittest.main()