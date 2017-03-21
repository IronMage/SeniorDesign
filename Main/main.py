import sys
sys.path.insert(0, '../Engine/Logic')
from FuzzyLogic import *
sys.path.insert(0, '../Communication')
from Server import *


def Main():
    #initialize server, will wait until connection is made from FUZZYevolve client
    Server = server()
    #instatiate FuzzyLogic class
    fz = FuzzyLogic()
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
        	print(buttonToPress + otherButton)
        else:
        	print(buttonToPress)
        #send buttonToPress back to FUZZYevolve client
        Server.send(buttonToPress)
     
if __name__ == '__main__':
	#unittest.main()
	Main()