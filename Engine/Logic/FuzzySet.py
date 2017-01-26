import unittest
class TriangularGraph:
    #            self, numberOfRanges, rangeStart, rangeEnd, rangeStart, rangeEnd, etc.
    def __init__(self,*args):
        if( len(args) != (1 + (args[0] * 2)) ):
            errorString = "The format for TriangularGraph is numberOfRanges, rangeStart, rangeEnd, rangeStart, rangeEnd, etc..."
            print(errorString)
            infoString = "The length expected is " + str((1 + (args[0] * 2))) + " the total length is " + str(len(args))
            print(infoString)
            for i in range(len(args)):
                print(args[i])
            raise ValueError("The number of arguments in TriangularGraph did not match expected value.")
        self.rangeDimensions = []
        #print(self.rangeDimensions)
        self.numberOfRanges = args[0]
        self.rangeOwnership = [None] * args[0]

        for i in range(self.numberOfRanges):
            self.rangeDimensions.append([None, None])
            #print("Range " + str(i) + " start: " + str(args[i * 2 + 1]) + " end: " + str(args[i * 2 + 2]))
            self.rangeDimensions[i][0] = args[i * 2 + 1]
            self.rangeDimensions[i][1] = args[i * 2 + 2]
            #self.rangeDimensions[i] = [args[i * 2 + 1], args[i * 2 + 2]]
            #print(self.rangeDimensions)

    def getOwnership(self, value):
        for i in range(self.numberOfRanges):
            setRange = self.rangeDimensions[i]
            #print("Range " + str(i) + " start: " + str(setRange[0]) + " end: " + str(setRange[1]))
            if(value >= setRange[0] and value <= setRange[1]):
                midPoint = (setRange[0] + setRange[1]) / 2
                if(value < midPoint):
                    slope = 100 / (midPoint - setRange[0])
                    offset = value - setRange[0]
                    self.rangeOwnership[i] = (offset * slope)
                elif(value > midPoint):
                    slope = 100 / (setRange[1] - midPoint)
                    offset = value - midPoint
                    self.rangeOwnership[i] = (100 - (offset * slope))
                elif(value == midPoint):
                    self.rangeOwnership[i] = 100
            else:
                self.rangeOwnership[i] = 0
        return self.rangeOwnership

class TrapazoidalGraph:
    #            self, numberOfRanges, rangeStart, plateauStart , plateauEnd, rangeEnd, etc.
    def __init__(self,*args):
        if( len(args) != (1 + (args[0] * 4)) ):
            errorString = "The format for TriangularGraph is numberOfRanges, rangeStart, rangeEnd, rangeStart, rangeEnd, etc..."
            print(errorString)
            infoString = "The length expected is " + str((1 + (args[0] * 4))) + " the total length is " + str(len(args))
            print(infoString)
            for i in range(len(args)):
                print(args[i])
            raise ValueError("The number of arguments in TriangularGraph did not match expected value.")
        self.rangeDimensions = []
        self.numberOfRanges = args[0]
        self.rangeOwnership = [None] * args[0]

        for i in range(self.numberOfRanges):
            self.rangeDimensions.append([None, None, None, None])
            #print("Range " + str(i) + " start: " + str(args[i * 2 + 1]) + " end: " + str(args[i * 2 + 2]))
            self.rangeDimensions[i][0] = args[i * 4 + 1]
            self.rangeDimensions[i][1] = args[i * 4 + 2]
            self.rangeDimensions[i][2] = args[i * 4 + 3]
            self.rangeDimensions[i][3] = args[i * 4 + 4]
            #self.rangeDimensions[i] = [args[i * 2 + 1], args[i * 2 + 2]]
            #print(self.rangeDimensions)

    def getOwnership(self, value):
        #setRange :  [rangeStart, plateauStart, plateauEnd, RangeEnd]
        for i in range(self.numberOfRanges):
            setRange = self.rangeDimensions[i]
            #print("Range " + str(i) + " start: " + str(setRange[0]) + " end: " + str(setRange[1]))
            if(value >= setRange[0] and value <= setRange[3]):
                #midPoint = (setRange[0] + setRange[1]) / 2
                if(value < setRange[1]):
                    slope = 100 / (setRange[1] - setRange[0])
                    offset = value - setRange[0]
                    #print("Range " + str(i) + " slope " + str(slope) + " offset " + str(offset))
                    self.rangeOwnership[i] = (offset * slope)
                elif(value > setRange[2]):
                    slope = 100 / (setRange[3] - setRange[2])
                    offset = value - setRange[2]
                    #print("Range " + str(i) + " slope " + str(slope) + " offset " + str(offset))
                    self.rangeOwnership[i] = (100 - (offset * slope))
                elif(value >= setRange[1] and value <= setRange[2]):
                    self.rangeOwnership[i] = 100
            else:
                self.rangeOwnership[i] = 0
        return self.rangeOwnership

class  FuzzySets:
    def __init__(self):
        self.sets = []
        self.setNames = []
    def addSet(self, newSet, setName):
        if(isinstance(newSet, TriangularGraph) or isinstance(newSet, TrapazoidalGraph)):
            self.sets.append(newSet)
            self.setNames.append(setName)
        else:
            raise ValueError("Trying to add set of type " + str(type(newSet)) + ". Only TriangularGraph and TrapazoidalGraph allowed.")
    def getSets(self):
        return self.sets
    def exists(self, name):
        for n in self.setNames:
            if(n == name):
                return True
        return False


class TestFuzzySets(unittest.TestCase):
    def testTriangularGraph(self):
        print("\nTESTING TRIANGULAR GRAPH")
        #Case 1
        expectedResults = [[None, None, None]] * 13
        expectedResults[0] = [0, 0, 0]
        expectedResults[1] = [50, 0 ,0]
        expectedResults[2] = [100, 0, 0]
        expectedResults[3] = [50, 25, 0]
        expectedResults[4] = [0, 50, 0]
        expectedResults[5] = [0, 75, 0]
        expectedResults[6] = [0, 100, 0]
        expectedResults[7] = [0, 75, 0]
        expectedResults[8] = [0, 50, 0]
        expectedResults[9] = [0, 25, 50]
        expectedResults[10] = [0, 0, 100]
        expectedResults[11] = [0, 0, 50]
        expectedResults[12] = [0, 0, 0]

        t = TriangularGraph(3, 0, 4, 2, 10, 8, 12)
        for i in range(13):
            result = t.getOwnership(i) #Load all of the results to be checked in a minute
            self.assertEqual(result, expectedResults[i])

        #Case 2
        expectedResults = [None] * 11
        expectedResults[0] = [0, 0, 0]
        expectedResults[1] = [50, 20 ,0]
        expectedResults[2] = [100, 40, 0]
        expectedResults[3] = [50, 60, 0]
        expectedResults[4] = [0, 80, 0]
        expectedResults[5] = [0, 100, 0]
        expectedResults[6] = [0, 80, 0]
        expectedResults[7] = [0, 60, 50]
        expectedResults[8] = [0, 40, 100]
        expectedResults[9] = [0, 20, 50]
        expectedResults[10] = [0, 0, 0]

        t = TriangularGraph(3, 0, 4, 0, 10, 6, 10)
        for i in range(11):
            result = t.getOwnership(i) #Load all of the results to be checked in a minute
            self.assertEqual(result, expectedResults[i])

    def testTrapazoidalGraph(self):
        print("\nTESTING TRAPAZOIDAL GRAPH")
        #Case 1
        expectedResults = [[None, None, None]] * 13
        expectedResults[0] = [100, 0, 0]
        expectedResults[1] = [100, 0 ,0]
        expectedResults[2] = [100, 0, 0]
        expectedResults[3] = [50, 0, 0]
        expectedResults[4] = [0, 100, 0]
        expectedResults[5] = [0, 100, 0]
        expectedResults[6] = [0, 100, 0]
        expectedResults[7] = [0, 100, 50]
        expectedResults[8] = [0, 100, 100]
        expectedResults[9] = [0, 100, 100]
        expectedResults[10] = [0, 100, 100]

        t = TrapazoidalGraph(3, 0, 0, 2, 4, 3, 4, 10, 10, 6, 8, 10, 10)
        for i in range(11):
            result = t.getOwnership(i) #Load all of the results to be checked in a minute
            self.assertEqual(result, expectedResults[i])

        #Case 2
        expectedResults = [[None, None, None]] * 13
        expectedResults[0] = [0, 0, 0]
        expectedResults[1] = [50, 0 ,0]
        expectedResults[2] = [100, 0, 0]
        expectedResults[3] = [100, 0, 0]
        expectedResults[4] = [100, 0, 0]
        expectedResults[5] = [50, 50, 0]
        expectedResults[6] = [0, 100, 0]
        expectedResults[7] = [0, 50, 50]
        expectedResults[8] = [0, 0, 100]
        expectedResults[9] = [0, 0, 100]
        expectedResults[10] = [0, 0, 100]
        expectedResults[11] = [0, 0, 50]
        expectedResults[12] = [0, 0, 0]

        t = TrapazoidalGraph(3, 0, 2, 4, 6, 4, 6, 6, 8, 6, 8, 10, 12)
        for i in range(11):
            result = t.getOwnership(i) #Load all of the results to be checked in a minute
            self.assertEqual(result, expectedResults[i])

    def testFuzzySetWrapper(self):
        print("\nTESTING FUZZY SET WRAPPER")
        fz = FuzzySets()

        t1 = TrapazoidalGraph(3, 0, 2, 4, 6, 4, 6, 6, 8, 6, 8, 10, 12)
        t2 = TriangularGraph(3, 0, 4, 2, 10, 8, 12)

        fz.addSet(t1, "DISTANCE")
        self.assertEqual(t1.getOwnership(9), fz.getSets()[0].getOwnership(9))
        self.assertTrue(fz.exists("DISTANCE"))
        self.assertFalse(fz.exists("HEALTH"))

        fz.addSet(t2, "LIFE")
        self.assertEqual(t1.getOwnership(9), fz.getSets()[0].getOwnership(9))
        self.assertEqual(t2.getOwnership(9), fz.getSets()[1].getOwnership(9))
        self.assertTrue(fz.exists("LIFE"))
        self.assertFalse(fz.exists("HEALTH"))


if __name__ == '__main__':
    unittest.main()