import sys
import numpy as np 
import neurolab as nl 
import math
sys.path.insert(0, '../Engine/Logic')
from FuzzyLogic import *
sys.path.insert(0, '../Engine/Adaptation')
from Adaptation import *
import NeuralNetwork
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

def Train():
    #train the neural network and save the network information into a file
    nn = NeuralNetwork.neuralnetwork()
    for r in range(0, 1):
        with open('dataTesting2.txt') as file:
            for line in file:
                arr = line.split(',')
                y = int(arr[0])
                mariox = arr[6]
                marioy = arr[7]
                numEnemies = arr[8]

                # for 2 input neural network
                # if(int(numEnemies) != 0):
                #     x = []
                #     for i in range(0, int(numEnemies), 2):
                #         x.append(int(arr[9+i]) - int(mariox))
                #         x.append(int(arr[9+i+1]) - int(marioy))
                #     closest = []
                #     closest.append(0)
                #     closest.append(0)
                #     minDistance = 10000
                #     for j in range(0, len(x), 2):
                #         dist = math.sqrt( (x[j]*x[j]) * (x[j+1]*x[j+1]) )
                #         if(dist < minDistance):
                #             closest = []
                #             closest.append(x[j])
                #             closest.append(x[j+1])
                #             minDistance = dist
                # else:
                #     closest = []
                #     closest.append(0)
                #     closest.append(0)
                # nn.train(closest, y)

                # for 30 input neural network
                if(int(numEnemies) != 0):
                    x = []
                    for i in range(0, int(numEnemies), 2):
                        x.append(int(arr[9+i]) - int(mariox))
                        x.append(int(arr[9+i+1]) - int(marioy))
                    for j in range(len(x), 30, 1):
                        x.append(0)
                else:
                    x = []
                    for j in range(0, 30):
                        x.append(0)
                nn.train(x, y)
    nn.save()

def Play():
    #load the neural netork from the file and run the game
    nn = NeuralNetwork.neuralnetwork()
    nn.load()

    #initialize server, will wait until connection is made from FUZZYevolve client
    Server = server()
    #intialize gameInfo
    gameInfo = ""
    #initialize msg
    msg = ""
    #begin the game
    while True:
        #receive the game info from the FUZZYevolve client
        gameInfo = Server.receive()
        #format the gameInfo appropriately for neural network's 30 inputs
        arr = gameInfo.split(',')
        mariox = arr[0]
        marioy = arr[1]
        numEnemies = arr[2]

        # for 2 input neural network
        # if(int(numEnemies) != 0):
        #     x = []
        #     for i in range(0, int(numEnemies), 2):
        #         x.append(int(arr[3+i]) - int(mariox))
        #         x.append(int(arr[3+i+1]) - int(marioy))
        #     closest = []
        #     closest.append(0)
        #     closest.append(0)
        #     minDistance = 10000
        #     for j in range(0, len(x), 2):
        #         dist = math.sqrt( (x[j]*x[j]) * (x[j+1]*x[j+1]) )
        #         if(dist < minDistance):
        #             closest = []
        #             closest.append(x[j])
        #             closest.append(x[j+1])
        #             minDistance = dist
        # else:
        #     closest = []
        #     closest.append(0)
        #     closest.append(0)
        # #send nnInfo to neural network that returns a message
        # msg = nn.run(closest)

        # for 30 input neural network
        inputs = []
        for i in range(0, int(numEnemies), 2):
            inputs.append(int(arr[3+i]) - int(mariox))
            inputs.append(int(arr[3+i+1]) - int(marioy))
        for j in range(len(inputs), 30, 1):
            inputs.append(0)
        #send nnInfo to neural network that returns a message
        msg = nn.run(inputs)

        #reply to the server with message returned from neural network
        Server.send(msg)

def Random():
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

    goodWeights = False
    output = np.random.rand(fz.getWeightLength())
    print(output)
    print(myFuzzyClass.get1DWeights())
    myFuzzyClass.setWeights(output)
    while(goodWeights != True):
        #begin the game
        while True:
            #receive the game info from the FUZZYevolve client
            gameInfo = Server.receive()
            if(gameInfo == "0,0,0"):
                print("Good weights? (y or n)")
                select = input("")
                if(select == y):
                    goodWeights == True
                break;
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
    print(output, file="weightsRandom.txt")
     
if __name__ == '__main__':
    print("Select a mode:\nn - Normal\nt - Test\nr - Record\nl - Train\np - Play\nm - random")
    select = input("")
    if(select == "n"):
        Main()
    elif(select == "t"):
    	unittest.main()
    elif(select == "r"):
        DataMine()
    elif(select == "l"):
        Train()
    elif(select == "p"):
        Play()
    elif(select == "m"):
        Random()
    else:
        print("Unkown command")
        quit()
