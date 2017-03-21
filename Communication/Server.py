import socket
 
class server:

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 9994
         
        self.mySocket = socket.socket()
        self.mySocket.bind((self.host,self.port))
        
        print("Awaiting connection")
        self.mySocket.listen(1)
        self.conn, self.addr = self.mySocket.accept()
        #print ("Connection from: " + str(self.addr))

    def receive(self):
        data = self.conn.recv(1024).decode()
        if not data:
            print("No data received")
        #print("received: " + str(data))
        return(str(data))

    def send(self, button):
        data = str(button + "\n")
        #print("sending: " + str(data))
        self.conn.send(data.encode())

    def __del__(self):
        self.conn.close()