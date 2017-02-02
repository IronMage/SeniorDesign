--Lua UDP Client

--Sends game information to Python UDP Server,
--which returns the button to be pressed


-- change here to the host an port you want to contact
local host, port = "localhost", 10000
-- load namespace
local socket = require("socket")
-- convert host name to ip address
local ip = assert(socket.dns.toip(host))
-- create a new UDP object
local udp = assert(socket.udp())
-- contact daytime host
assert(udp:sendto("anything", ip, port))
-- retrieve the answer and print results
io.write(assert(udp:receive()))