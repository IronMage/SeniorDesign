-- Lua TCP Client

-- Used for sending the game info to the python Server
-- Message format will be number of enemies followed by the x y pair for each enemy

-- load namespace
local socket = require("socket")
-- create a TCP socket and bind it to the local host, at any port
local client = socket.try(socket.connect("127.0.0.1", 9994))
-- find out which port the OS chose for us
local ip, port = client:getsockname()
-- print a message informing what's up
-- print("Connecting to local host on port " .. port)
-- print("After connecting, you have 10s to enter a line to be echoed")

client:send("Hello Server!\n")
local line, err = client:receive()
-- if there was no error, send it back to the client
if not err then 
  print("Server replied: " .. line)
end
-- done with client, close the object
client:close()