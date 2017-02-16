-- Lua TCP Client

-- Used for sending the game info to the python Server
-- Message format will be number of enemies followed by the x y pair for each enemy

-- load namespace
local socket = require("socket")
-- create a TCP socket and bind it to the local host, at any port
local client = socket.try(socket.connect("127.0.0.1", 9998))
-- find out which port the OS chose for us
local ip, port = client:getsockname()
-- print a message informing what's up
print("Connecting to local host on port " .. port)
print("After connecting, you have 10s to enter a line to be echoed")

client:send("Hello Server!\n")
local line, err = client:receive()
-- if there was no error, send it back to the client
if not err then 
  print("Server replied: " .. line)
end
-- done with client, close the object
client:close()

-- -- loop forever waiting for clients
-- while 1 do
--   -- wait for a conection from any client
--   local client = server:accept()
--   -- make sure we don't block waiting for this client's line
--   client:settimeout(10)
--   -- receive the line
--   local line, err = client:receive()
--   -- if there was no error, send it back to the client
--   if not err then client:send(line .. "\n") end
--   -- done with client, close the object
--   client:close()
-- end