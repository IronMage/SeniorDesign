#!python3
#Python UDP Client
'''Used for testing Python UDP Server'''

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
#message = 'This is the message.  It will be repeated.'

while True:
    message = input('Enter message to send: ')
    # Send data
    print('sending "%s"' % message)
    sent = sock.sendto(message.encode(), server_address)

    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received "%s"' % data)

print('closing socket')
sock.close()