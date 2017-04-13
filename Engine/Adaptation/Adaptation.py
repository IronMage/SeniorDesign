import sys
import unittest
import numpy as np 
import neurolab as nl 
sys.path.insert(0, '../Logic')
from FuzzyLogic import *

class FuzzyAdapt():
	def setupNetwork(self,weightSize):
		networkInputRanges = []
		#minimum weight is zero (no effect), max is 100 (randomly picked)
		weightRange = [0, 100]
		numNeuronsInputLayer = weightSize * 2
		numNeuronsOutputLayer = weightSize
		for x in range(weightSize):
			networkInputRanges.append(weightRange)
		myNet = nl.net.newff(networkInputRanges, [numNeuronsInputLayer, numNeuronsOutputLayer])
		return myNet

	def __init__(self, FuzzyLogic):
		self.Fz = FuzzyLogic
		myFuzzyClass = FuzzyLogic
		self.weightSize = self.Fz.getWeightLength()
		self.currentWeights = self.Fz.get1DWeights()
		self.network = self.setupNetwork(self.weightSize)

	def trainNetwork(self, targetFuzzyChoice):
		currentFuzzyChoice = self.Fz.neuralNetworkRun()

		self.network.train(currentFuzzyChoice, targetFuzzyChoice, show = 10)
		self.currentWeights = self.Fz.get1DWeights()

		return self.currentWeights

		
		