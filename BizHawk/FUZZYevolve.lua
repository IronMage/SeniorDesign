-- Lua file that will be opened in the emulator that will send out game information to the python server
-- game information will be the number of enemies, followed by the x y pair for each enemy
-- the python server will return the buttons to be pressed

-- Intended for use with the BizHawk emulator and Super Mario World (USA) ROM.
-- For SMW, make sure you have a save state named "SMW1.state" at the beginning of "Donut Plains 1",
-- and put a copy in both the Lua folder and the root directory of BizHawk.







-- Send game information to the Python TCP server
function sendGameInfo(msg)
    -- Lua TCP Client

    -- Used for sending the game info to the python Server
    -- Message format will be number of enemies followed by the x y pair for each enemy

    print("Requireing socket")
    -- load namespace
    local socket = require("socket")
    print("Trying socket connection")
    -- create a TCP socket and bind it to the local host, at any port
    local client = socket.try(socket.connect("127.0.0.1", 9994))
    print("Getting socket names")
    -- find out which port the OS chose for us
    local ip, port = client:getsockname()
    -- print a message informing what's up
    -- print("Connecting to local host on port " .. port)
    -- print("After connecting, you have 10s to enter a line to be echoed")

    print("Sending Hello Server!")
    client:send("Hello Server!\n")
    print("Receiving from server")
    local line, err = client:receive()

    -- if there was no error
    if not err then 
        console.writeline("Server replied: " .. line)
        print("Closing socket")
        -- done with client, close the object
        client:close()
        return line
    else
        console.writeline("Error in receiving from TCP server")
        print("Closing socket")
        -- done with client, close the object
        client:close()
        return "Error"
    end
end

function onExit()
    forms.destroy(form)
end

----------------------------------------------------------
----------------------------------------------------------
--Everything above this chunk of comments are functions
-- and imports
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------
--Everything below this chunk of comments is sequentially
-- executed code
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
    console.writeline("This ROM is not Super Mario World (USA)")
    console.writeline("Please use the correct ROM to run this lua code")
end

event.onexit(onExit)

-- Create a form ----------------------------------------------------
form = forms.newform(200, 260, "Fitness")
maxFitnessLabel = forms.label(form, "Best Score: 0", 5, 8)
-- maxFitnessLabel = forms.label(form, "Max Fitness: " .. math.floor(pool.maxFitness), 5, 8)
-- showNetwork = forms.checkbox(form, "Show Map", 5, 30)
-- showMutationRates = forms.checkbox(form, "Show M-Rates", 5, 52)
-- restartButton = forms.button(form, "Restart", initializePool, 5, 77)
-- saveButton = forms.button(form, "Save", savePool, 5, 102)
-- loadButton = forms.button(form, "Load", loadPool, 80, 102)
-- saveLoadFile = forms.textbox(form, Filename .. ".pool", 170, 25, nil, 5, 148)
-- saveLoadLabel = forms.label(form, "Save/Load:", 5, 129)
-- playTopButton = forms.button(form, "Play Top", playTop, 5, 170)
-- hideBanner = forms.checkbox(form, "Hide Banner", 5, 190)

-- Lua TCP Client ---------------------------------------------------
-- Used for sending the game info to the python Server over local host
-- Message format will be number of enemies followed by the x y pair for each enemy
-- load namespace
-- local socket = require("socket")
-- -- create a TCP socket and bind it to the local host, at any port
-- local client = socket.try(socket.connect("127.0.0.1", 9994))
-- -- find out which port the OS chose for us
-- local ip, port = client:getsockname()
-- -- print("Connecting to local host on port " .. port)

local message = "message"
console.log("Returned: " .. sendGameInfo(message))