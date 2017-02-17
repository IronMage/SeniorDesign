-- Lua file that will be opened in the emulator that will send out game information to the python server
-- game information will be the number of enemies, followed by the x y pair for each enemy
-- the python server will return the buttons to be pressed

-- Intended for use with the BizHawk emulator and Super Mario World (USA) ROM.
-- For SMW, make sure you have a save state named "SMW1.state" at the beginning of "Donut Plains 1",
-- and put a copy in both the Lua folder and the root directory of BizHawk.












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