import socket

class Networking:
    def __init__(self):
        self.ownSocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.ownSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.T_PORT = 7003
        self.TCP_IP = (socket.gethostbyname(socket.gethostname()))

    def configureHost(self):       
        self.ownSocket.bind((self.TCP_IP, self.T_PORT))

    def joinHost(self,ip):
        self.ownSocket.connect((ip,self.T_PORT))
    
    def recieveConnection(self):
        self.ownSocket.listen(1)
        self.conn, self.addr = self.ownSocket.accept()
    
    def listenForMessage(self):
        self.ownSocket.listen()
        return (self.conn.recv(2048).decode())
    def sendMessage(self,message):
        self.ownSocket.send(message.encode())
    def exit(self):
        self.ownSocket.close()
    

    




    