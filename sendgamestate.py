import socket
import pickle
import game
import DBM
from random import randint
import sys
import time

class Networking():

    def __init__(self,Username):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.settimeout(0.01) .   #NEED TO SORT OUT TIMIEOUT HERE
        self.host = socket.gethostname()
        self.port = 1800
        self.s.bind((self.host,self.port))
        self.Username = Username
        networkInfo = {self.s:Username}
        current = 0
        self.currentlisten: socket.socket = None



#recieve destination addresses until started. Then send out a list of ports
    def joinGame(self,IP,port):
        self.s.connect((IP, port))
        hostname=socket.gethostname()
        self.IPAddr=socket.gethostbyname(hostname)
        self.s.send(self.Username.encode())
        try:
            accepted = self.s.recv(1024).decode()
            print(accepted)
            self.networkInfo = pickle.load(self.s.recv(1024))
            print(self.networkinfo)
        except:
            pass



    def listenForPlayers(self):
        self.s.listen(4)
        c, addr = self.s.accept()
        self.PlayerDestinations.append(c)
        
        

    def StartedGameNetwork(self):
        for c in self.PlayerConnections:
            c.send(pickle.dumps(self.PlayerDestinations))
    


    def recieveStartList(self):
        self.PlayerDesitinations = self.currentlisten.recv()

    def ChangePlayerTurnNetwork(self):
        self.currentListen = self.PlayerDestinations[self.PlayerDesitinations[self.current]]
        self.current += 1

    def sendCountryStatus(self,Country: str):
        message = f"{DBM.findOccupant(Country)}#{DBM.findTroops(Country)}"
        for c in self.PlayerConnections: 
            pickle.dumps(message)
    
    def returnMessage(message):
        occupant, troops = message.split("#")
        DBM.changeOccupant(occupant)
        DBM.changeTroops(troops)

    def networkinfo(self):
            self.s.listen(5)
            while True:
                c, addr = self.s.accept()
                print("Connection accepted from " + repr(addr[1]))
                c.send(("Server approved connection\n").encode())
                therequest = c.recv(1026).decode()
                print(therequest)
                if therequest == 'occupiers':
                    #c.send(Game.sendgamestate()) # it needs to send back the return of a getfunction of occupiers
                    print('sent')
                c.close()
Session = Networking('Bob')
Session.joinGame('192.168.1.119',1248)