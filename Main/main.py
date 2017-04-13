import sys
import numpy as np 
import neurolab as nl 
sys.path.insert(0, '../Engine/Logic')
from FuzzyLogic import *
sys.path.insert(0, '../Engine/Adaptation')
from Adaptation import *
sys.path.insert(0, '../Communication')
from Server import *

#Set up the custom nuerolab error functions
myFuzzyClass = None

def myError(self, target, output):
    print("Entered custom error")
    #update weights
    myFuzzyClass.setWeights(output)
    newOutput = myFuzzyClass.neuralNetworkRun()
    e = target - newOutput
    v = .5 * np.sum(np.square(e))
    return v

def myErrorDeriv(self, target, output):
    print("Entered custom error deriv")
    #update weights
    myFuzzyClass.setWeights(output)
    newOutput = myFuzzyClass.neuralNetworkRun()
    return target - newOutput

nl.error.SSE.__call__ = myError
nl.error.SSE.deriv = myErrorDeriv


def Main():
    #initialize server, will wait until connection is made from FUZZYevolve client
    Server = server()
    #instatiate FuzzyLogic class
    fz = FuzzyLogic()
    myFuzzyClass = fz

    fzAdapt = FuzzyAdapt(fz)

    #intialize gameInfo
    gameInfo = ""
    #initialize buttonToPress
    buttonToPress = ""
    #begin the game
    while True:
        #receive the game info from the FUZZYevolve client
        gameInfo = Server.receive()
        #send gameInfo to FUZZYevolve, assigning the returned button to buttonToPress
        buttonToPress, otherButton = fz.run(gameInfo)
        if(otherButton is not None):
	        #send buttonToPress back to FUZZYevolve client
	        msg = buttonToPress + " " + otherButton
        	#print(msg)
	        Server.send(msg)
        else:
        	#print(buttonToPress)
	        #send buttonToPress back to FUZZYevolve client
	        Server.send(buttonToPress)

def DataMine():
    #initialize server, will wait until connection is made from FUZZYevolve client
    Server = server()
    while True:
        #receive the game info from the FUZZYevolve client
        gameInfo = Server.receive()
        with open('dataTesting.txt', 'a') as file:
            if(gameInfo != ""):
                print(gameInfo)
                file.write(gameInfo)
        Server.send("OK")
     
if __name__ == '__main__':
    print("Select a mode:\nn - Normal\nt - Test\nr - Record")
    select = input("")
    if(select == "n"):
        Main()
    elif(select == "t"):
    	unittest.main()
    elif(select == "r"):
        DataMine()
    else:
        print("Unkown command")
        quit()
