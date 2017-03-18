-- Lua file that will be opened in the emulator that will send out game information to the python server
-- game information will be the number of enemies, followed by the x y pair for each enemy
-- the python server will return the button(s) to be pressed

-- Intended for use with the BizHawk emulator and Super Mario World (USA) ROM.
-- For SMW, make sure you have a save state named "SMW1.state" at the beginning of "Donut Plains 1",
-- and put a copy in both the Lua folder and the root directory of BizHawk.

-- load save state file, reset currentFrame, make sure no buttons are pressed
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
function pushButton()
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

-- display the map of sprites relative to mario
function displaySprites()
    -- initialize variables
    local cells = {}
    local i = 1
    local cell = {}
    -- define the space traversed for enemies relative to mario at (0,0)
    local BoxRadius = 100
    for dy=-BoxRadius,BoxRadius do
        for dx=-BoxRadius,BoxRadius do
            cell = {}
            -- (0,0) is the top left of the box that will be drawn
            -- To center mario in the box, add 75 to each x and y
            cell.x = dx+75
            cell.y = dy+75
            -- set value to 0 in case of no mario or sprite
            cell.value = 0
            -- if mario (center)
            if dy == 0 and dx == 0 then
                -- set sell to gray
                cell.value = 127
            else
                -- for all sprites
                for key, value in ipairs(sprites) do
                    -- if sprite is within the space traversed
                    -- if (((value["x"]-marioX) == dx) and ((value["y"]-marioY) == dy)) then
                    -- if sprite is within the space traversed times two (To see further)
                    if ((((value["x"]-marioX) == dx*2) or ((value["x"]-marioX) == dx*2-1)) and
                        (((value["y"]-marioY) == dy*2) or ((value["y"]-marioY) == dy*2-1))) then
                        --set cell to white
                        cell.value = 255
                    end
                end
                -- for all extended sprites
                for key, value in ipairs(extended) do
                    -- if sprite is within the space traversed
                    -- if (((value["x"]-marioX) == dx) and ((value["y"]-marioY) == dy)) then
                    -- if sprite is within the space traversed times two (To see further)
                    if ((((value["x"]-marioX) == dx*2) or ((value["x"]-marioX) == dx*2-1)) and
                        (((value["y"]-marioY) == dy*2) or ((value["y"]-marioY) == dy*2-1))) then
                        --set cell to white
                        cell.value = 255
                    end
                end
            end
            -- add cell just defined to list of all cells
            cells[i] = cell
            i = i + 1
        end
    end
    -- draw the whole box on the emulator's screen
    gui.drawBox(-BoxRadius*1.5,-BoxRadius*1.5,BoxRadius*1.5,BoxRadius*1.5,0xFF000000, 0x80808080)
    -- for all cells
    for n,cell in pairs(cells) do
        -- if cell has mario or sprite (not equal to 0)
        if cell.value ~= 0 then
            local color = cell.value
            -- safety checks
            if color > 255 then color = 255 end
            if color < 0 then color = 0 end
            local opacity = 0xFF000000
            if cell.value == 0 then
                opacity = 0x50000000
            end
            color = opacity + color*0x10000 + color*0x100 + color
            -- draw small box representing mario or sprite
            gui.drawBox(cell.x-2,cell.y-2,cell.x+2,cell.y+2,opacity,color)
        end
    end
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
        -- get the game info from rom, returned message format = MarioX,MarioY,numEnemies,X,Y,X,Y,....
        message = getGameInfo()
        -- check if Mario is no longer alive
        if(marioX == 0 and marioY == 0) then
            break -- break out of inner while loop if Mario is no longer alive
        end
        -- check if sprite display is desired
        if forms.ischecked(showNetwork) then
            displaySprites()
        end
        -- send the game info to the Fuzzy algorithm and get the response
        msgReturned = sendGameInfo(message)
        -- set the joypad to press the button returned by the algorithm
        pushButton()
        -- advance the screen frame
        emu.frameadvance();
        -- keep track of the number of frames advanced through
        currentFrame = currentFrame + 1
    end
end

-- Gracefully handle unexpected exit
event.onexit(onExit)