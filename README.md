#SeniorDesign

LET'S PLAY WITH MACHINE LEARNING

Python and Lua code that utilizes Machine Learning to autonomously learn to play NES games

##Communication

TCP connection between a Lua client and a Python server

###/Logic/LuaTCPClient.lua

The Lua TCP Client that will send game info to the python TCP Server

###/Logic/PythonTCPServer.py

The Python TCP Server that will take the game info from the Lua TCP Client, compute the move to make, and send the buttons to be pressed back to the Lua TCP Client

Emulator - Lua Console - Raw Data <=> Raw Data - AI - Adaptation

      (A,B,up,down,left,right) <- <=> -> Sprite Data (#enemies followed by x y pairs for each enemy)

##Engine

###/Logic/FuzzyRules.py

Rules class

###/Logic/FuzzySet.py

Produces Triangular and Trapezoidal graphs

##Main