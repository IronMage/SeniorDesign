-- Lua file that will be opened in the emulator that will send out game information to the python server
-- game information will be the number of enemies, followed by the x y pair for each enemy
-- the python server will return the button(s) to be pressed

-- Intended for use with the BizHawk emulator and Super Mario World (USA) ROM.
-- For SMW, make sure you have a save state named "SMW1.state" at the beginning of "Donut Plains 1",
-- and put a copy in both the Lua folder and the root directory of BizHawk.


function setupRun()
    savestate.load(Filename);
    currentFrame = 0
    clearJoypad()
end

-- clear the controller to prepare for next move
function clearJoypad()
    controller = {}
    for b = 1,#ButtonNames do
        controller["P1 " .. ButtonNames[b]] = false
    end
    joypad.set(controller)
end

-- get the game info from rom, returned message format = MarioX,MarioY,numEnemies,X,Y,X,Y,....
function getGameInfo()
    marioX = memory.read_s16_le(0x94)
    marioY = memory.read_s16_le(0x96)
    retMessage = marioX .. ',' .. marioY
    return retMessage
end 

-- Send game information to the Python TCP server
function sendGameInfo(msg)
    -- Lua TCP Client
    -- Used for sending the game info to the python Server
    -- Message format will be MarioX, MarioY, number of enemies, x y pair for each enemy
    -- Message is comma delimited
    client:send(msg .. '\n')
    local line, err = client:receive()

    -- if there was no error
    if not err then 
        return line
    else  -- if there was an error
        console.writeline("Error in receiving from TCP server")
        return "Error"
    end
end

--set the joypad to push the button returned from the Fuzzy Algorithm
function pushButton(message)
    if msgReturned == "RIGHT" then
        -- console.log("RIGHT Returned")
        button = "Right"
    elseif msgReturned == "LEFT" then
        button = "Left"
    elseif msgReturned == "UP" then
        button = "Up"
    elseif msgReturned == "DOWN" then
        button = "Down"
    elseif msgReturned == "A" then
        button = "A"
    elseif msgReturned == "B" then
        button = "B"
    elseif msgReturned == "X" then
        button = "X"
    elseif msgReturned == "Y" then
        button = "Y"
    else
        button = ""
    end

    for b = 1,#ButtonNames do
        if ButtonNames[b] == button then
            controller["P1 " .. ButtonNames[b]] = true
        else
            controller["P1 " .. ButtonNames[b]] = false
        end
    end
    joypad.set(controller)
end

-- Gracefully handle unexpected exit
function onExit()
    forms.destroy(form)
    client:close()
end

----------------------------------------------------------
----------------------------------------------------------
--Only functions above------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
--Only sequentially executed code below-------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------

if gameinfo.getromname() == "Super Mario World (USA)" then
    Filename = "SMW1.state"
    ButtonNames = {
        "A",
        "B",
        "X",
        "Y",
        "Up",
        "Down",
        "Left",
        "Right",
    }
else
    console.writeline("The ROM is not Super Mario World (USA)")
    console.writeline("Please use the correct ROM to run this lua code")
end

-- Create a form ----------------------------------------------------
form = forms.newform(200, 260, "Fitness")
maxFitnessLabel = forms.label(form, "Best Score: 0", 5, 8)

-- Lua TCP Client ---------------------------------------------------
-- Used for sending the game info to the python Server over local host
-- load namespace
socket = require("socket")
-- create a TCP socket and bind it to the local host, at any port
client = socket.try(socket.connect("127.0.0.1", 9994))
-- find out which port the OS chose for us
ip, port = client:getsockname()

-- run the algorithm on the game
while true do
    -- initialize a new run
    setupRun()
    while true do
        -- get the game info from rom, returned message format = MarioX,MarioY,numEnemies,X,Y,X,Y,....
        message = getGameInfo()
        -- check if Mario is no longer alive
        if(marioX == 0 and marioY == 0) then
            break -- break out of inner while loop if Mario is no longer alive
        end
        -- send the game info to the Fuzzy algorithm and get the response
        msgReturned = sendGameInfo(message)
        -- set the joypad to press the button returned by the algorithm
        pushButton(msgReturned)
        -- advance the screen frame
        emu.frameadvance();
        -- keep track of the number of frames advanced through
        currentFrame = currentFrame + 1
    end
end

-- Gracefully handle unexpected exit
event.onexit(onExit)