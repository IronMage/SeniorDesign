-- load save state file, reset currentFrame, make sure no buttons are pressed
function setupRun()
    savestate.load(Filename);
    currentFrame = 0
end

-- get the game info from rom, returned message format = MarioX,MarioY,numEnemies,X,Y,X,Y,....
function getGameInfo()
    -- get marioX and marioY
    marioX = memory.read_s16_le(0x94)
    marioY = memory.read_s16_le(0x96)
    retMessage = marioX .. ',' .. marioY

    -- get number of enemies
    sprites = {}
    for slot=0,11 do
        local status = memory.readbyte(0x14C8+slot)
        if status ~= 0 then
            spritex = memory.readbyte(0xE4+slot) + memory.readbyte(0x14E0+slot)*256
            spritey = memory.readbyte(0xD8+slot) + memory.readbyte(0x14D4+slot)*256
            sprites[#sprites+1] = {["x"]=spritex, ["y"]=spritey}
        end
    end
    extended = {}
    for slot=0,11 do
        local number = memory.readbyte(0x170B+slot)
        if number ~= 0 then
            spritex = memory.readbyte(0x171F+slot) + memory.readbyte(0x1733+slot)*256
            spritey = memory.readbyte(0x1715+slot) + memory.readbyte(0x1729+slot)*256
            extended[#extended+1] = {["x"]=spritex, ["y"]=spritey}
        end
    end
    retMessage = retMessage .. ',' .. (table.getn(sprites) + table.getn(extended))

    for key, value in ipairs(sprites) do
        retMessage = retMessage .. ',' .. value["x"] .. ',' .. value["y"]
    end
    for key, value in ipairs(extended) do
        retMessage = retMessage .. ',' .. value["x"] .. ',' .. value["y"]
    end

    return retMessage
end 

-- Send game information to the Python TCP server
function sendGameInfo(msg)
    -- Lua TCP Client
    -- Used for sending the game info to the python Server
    -- Message format will be MarioX, MarioY, number of enemies, x y pair for each enemy
    -- Message is comma delimited
    client:send(msg .. '\n')
    -- local line, err = client:receive()

    -- -- if there was no error
    -- if not err then 
    --     return line
    -- else  -- if there was an error
    --     console.writeline("Error in receiving from TCP server")
    --     return "Error"
    -- end
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
showNetwork = forms.checkbox(form, "Show Map", 5, 30)

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
        -- -- get the game info from rom, returned message format = MarioX,MarioY,numEnemies,X,Y,X,Y,....
        message = getGameInfo()
        -- -- check if Mario is no longer alive
        -- if(marioX == 0 and marioY == 0) then
        --     break -- break out of inner while loop if Mario is no longer alive
        -- end
        -- -- send the game info to the Fuzzy algorithm and get the response
        sendGameInfo(message)
        -- advance the screen frame
        emu.frameadvance();
        -- keep track of the number of frames advanced through
        currentFrame = currentFrame + 1
    end
end

-- Gracefully handle unexpected exit
event.onexit(onExit)