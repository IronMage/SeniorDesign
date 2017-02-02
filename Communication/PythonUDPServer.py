#!python3
#Python UDP Server
'''
Receives the datagram from Lua UDP Client, 
decodes it,
and sends the information to defuzzifier which returns the button to be pressed,
the button is encoded,
and then returned to the Client
'''

import socket
import sys

print('Creating UDP socket')
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
#server_address = ('localhost', 10000)
#print('starting up on %s port %s' % server_address)
#sock.bind(server_address)
sock.bind(('localhost', 10000))
print('Server started')

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)
    
    print('received %s bytes from %s' % (len(data), address))
    print(data)
    
    if data:
        sent = sock.sendto(data, address)
        print('sent %s bytes back to %s' % (sent, address))

sock.close()