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
-- if there was no error, send it back to the client
if not err then 
  print("Server replied: " .. line)
end
print("Closing socket")
-- done with client, close the object
client:close()