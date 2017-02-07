--Lua UDP Server

--Used for testing Lua UDP Client

local socket = require("socket")
host = "127.0.0.1"
port = 10000

print("Binding to host '" ..host.. "' and port " ..port.. "...")
udp = assert(socket.udp())
assert(udp:setsockname(host, port))
assert(udp:settimeout(5))
-- udp:setsockname(host, port)
-- udp:settimeout(5)
ip, port = udp:getsockname()
assert(ip, port)
print("Waiting packets on " .. ip .. ":" .. port .. "...")

while 1 do
    dgram, ip, port = udp:receivefrom()
    if dgram then
        print("Echoing '" .. dgram .. "' to " .. ip .. ":" .. port)
        udp:sendto(dgram, ip, port)
    else
        print(ip)
    end
end