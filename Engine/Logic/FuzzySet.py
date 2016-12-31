class TriangularGraph:
    #            self, numberOfRanges, rangeStart, rangeEnd, rangeStart, rangeEnd, etc.
    def __init__(self,*args):
        if( len(args) != (1 + (args[0] * 2)) ):
            errorString = "The format for TriangularGraph is numberOfRanges, rangeStart, rangeEnd, rangeStart, rangeEnd, etc..."
            print(errorString)
            infoString = "The length expected is " + str((1 + (args[0] * 2))) + " the total length is " + str(len(args))
            print(infoString)
            for i in xrange(len(args)):
                print args[i]
            raise ValueError("The number of arguments in TriangularGraph did not match expected value.")
        self.rangeDimensions = []
        #print(self.rangeDimensions)
        self.numberOfRanges = args[0]
        self.rangeOwnership = [None] * args[0]

        for i in xrange(self.numberOfRanges):
            self.rangeDimensions.append([None, None])
            #print("Range " + str(i) + " start: " + str(args[i * 2 + 1]) + " end: " + str(args[i * 2 + 2]))
            self.rangeDimensions[i][0] = args[i * 2 + 1]
            self.rangeDimensions[i][1] = args[i * 2 + 2]
            #self.rangeDimensions[i] = [args[i * 2 + 1], args[i * 2 + 2]]
            #print(self.rangeDimensions)

    def getOwnership(self, value):
        for i in xrange(self.numberOfRanges):
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
            for i in xrange(len(args)):
                print args[i]
            raise ValueError("The number of arguments in TriangularGraph did not match expected value.")
        self.rangeDimensions = []
        self.numberOfRanges = args[0]
        self.rangeOwnership = [None] * args[0]

        for i in xrange(self.numberOfRanges):
            self.rangeDimensions.append([None, None, None, None])
            #print("Range " + str(i) + " start: " + str(args[i * 2 + 1]) + " end: " + str(args[i * 2 + 2]))
            self.rangeDimensions[i][0] = args[i * 4 + 1]
            self.rangeDimensions[i][1] = args[i * 4 + 2]
            self.rangeDimensions[i][2] = args[i * 4 + 3]
            self.rangeDimensions[i][3] = args[i * 4 + 4]
            #self.rangeDimensions[i] = [args[i * 2 + 1], args[i * 2 + 2]]
            print(self.rangeDimensions)

    def getOwnership(self, value):
        #setRange :  [rangeStart, plateauStart, plateauEnd, RangeEnd]
        for i in xrange(self.numberOfRanges):
            setRange = self.rangeDimensions[i]
            #print("Range " + str(i) + " start: " + str(setRange[0]) + " end: " + str(setRange[1]))
            if(value >= setRange[0] and value <= setRange[3]):
                #midPoint = (setRange[0] + setRange[1]) / 2
                if(value < setRange[1]):
                    slope = 100 / (setRange[1] - setRange[0])
                    offset = value - setRange[0]
                    print("Range " + str(i) + " slope " + str(slope) + " offset " + str(offset))
                    self.rangeOwnership[i] = (offset * slope)
                elif(value > setRange[2]):
                    slope = 100 / (setRange[3] - setRange[2])
                    offset = value - setRange[2]
                    print("Range " + str(i) + " slope " + str(slope) + " offset " + str(offset))
                    self.rangeOwnership[i] = (100 - (offset * slope))
                elif(value >= setRange[1] and value <= setRange[2]):
                    self.rangeOwnership[i] = 100
            else:
                self.rangeOwnership[i] = 0
        return self.rangeOwnership

class FuzzySets:
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