import sys
sys.path.insert(0, '../Engine/Logic')
from FuzzyLogic import *
sys.path.insert(0, '../Communication')
from Server import *


def Main():
    #initialize server, will wait until connection is made from FUZZYevolve client
    Server = server()
    #intialize gameInfo
    gameInfo = ""
    #initialize buttonToPress
    buttonToPress = ""
    #begin the game
    while True:
        #receive the game info from the FUZZYevolve client
        gameInfo = Server.receive()
        #send gameInfo to FUZZYevolve, assigning the returned button to buttonToPress
        #send buttonToPress back to FUZZYevolve client
        Server.send("RIGHT")
     
if __name__ == '__main__':
    Main()