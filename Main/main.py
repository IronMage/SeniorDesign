import sys
sys.path.insert(0, '../Engine/Logic')
from FuzzyLogic import *
sys.path.insert(0, '../Communication')
from Server import *


def Main():
    Server = server()
    while True:
        Server.receive()
        Server.send("RIGHT")
     
if __name__ == '__main__':
    Main()