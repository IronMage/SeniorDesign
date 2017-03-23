#Fuzzifier
'''
Returns computed button presses to Python UDP Server
'''

#Insert distance formula, etc here.
import math
import unittest
from FuzzySet import *

class Fuzzifier:
    def __init__(self, inputSet):
        self.inputSet = inputSet
        self.currentMessage = {}
        self.lastMarioX = 0
        self.lastMarioY = 0
        self.marioX = 0
        self.marioY = 0
        self.enemyCoordinateStart = 3

    def parseMessage(self, message):
        self.currentMessage = message.split(",")
        self.lastMarioX = self.marioX
        self.lastMarioY = self.marioY
        self.marioX = int(self.currentMessage[0])
        self.marioY = int(self.currentMessage[1])

        return int(self.currentMessage[2])

    def getMario(self):
        if(self.inputSet.exists("MARIODX")):
            self.inputSet.getOwnership("MARIODX", (self.marioX - self.lastMarioX))
        else:
            raise ValueError("MARIODX does not exist in supplied input set")

    def getEnemies(self, coordinatePair):
        if(self.inputSet.exists("DX") and self.inputSet.exists("DY")):
            enemyX = int(self.currentMessage[self.enemyCoordinateStart + (2 * coordinatePair)])
            enemyY = int(self.currentMessage[self.enemyCoordinateStart + (2 * coordinatePair) + 1])
            dx = self.marioX - enemyX
            dy = self.marioY - enemyY
            #print("Enemy " + str(coordinatePair) + " dx " + str(dx) + " dy " + str(dy))
            self.inputSet.getOwnership("DX", dx)
            self.inputSet.getOwnership("DY", dy)
        else:
            raise ValueError("DX and DY do not exist in the supplied input set")

class TestFuzzifier(unittest.TestCase):
    def testFuzzifier(self):
        fz = FuzzySets()                                                        #Make an empty set to fill
        t1 = TrapazoidalGraph(3, 0, 2, 4, 6, 4, 6, 6, 8, 6, 8, 10, 12)          #Create a couple sets for the  container
        t2 = TriangularGraph(3, 0, 4, 2, 10, 8, 12)
        fz.addSet(t1, "DX")                                               #Add the first set

        fzy = Fuzzifier(fz)


        print("TESTING FUZZIFIER")
        string = "-3,2,1,0,-2"
        self.assertEqual(1, fzy.parseMessage(string))

        with self.assertRaises(ValueError):
            fzy.getEnemies(0)

if __name__ == '__main__':
    unittest.main()