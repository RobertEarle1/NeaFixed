
#----- A simple TCP client program in Python using send() function -----

import socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("192.168.1.119",1247))
data = "Hello Server!"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode())
 