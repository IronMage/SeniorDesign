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
    def selectOutput(self):
        results = self.outputSet.getResults("CONTROLLER")
        s = self.outputSet.getSets()
        names = self.outputSet.getNames("CONTROLLER")

        maxName = ""
        maxValue = -1

        for i in range(len(results)):
            if(results[i] > maxValue):
                maxValue = results[i]
                maxName = names[i]
            else:
                continue
        return maxName

    def sendToEmulator(self, outputName):
        #insert code here
        return 0

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