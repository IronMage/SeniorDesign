local socket = require "socket"
local address, port = "localhost", 10000

local entity
local world = {}
local t
local frame = 0

tcp = socket.tcp()
tcp:setpeername(address, port)

while true do
    entity = tostring(frame)
	emu.frameadvance();
end