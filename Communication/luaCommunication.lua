local socket = require "socket"
local address, port = "localhost", 10000

local entity
local world = {}
local t
local frame = 0

udp = socket.udp();
udp:setpeername(address, port);

while true do
    entity = tostring(frame);
    print(entity);
    -- udp.send(entity);
	emu.frameadvance();
end