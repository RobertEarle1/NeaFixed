from random import randint
import json
from pydoc import locate
import DBM

class Map:
    def __init__(self,map:str,Players:list,gameName:str):
        self._gameName = gameName
        self._map = map

    def getcountries(self):
        return self._countries


    def strDictTupleDict(self,givenDict):
        tupledict = {}
        for pair in givenDict:
            string = givenDict[pair]
            my_result = string.split(',')
            tuple1 = tuple(my_result)
            tupledict.update({pair:tuple1})
        return tupledict




    def findinfo(self,whatinfo:str,country:str='Alaska'):
        if self._map =="normal":
            with open('normal.txt', 'r') as f:
                dict = (json.loads(f.read()))
                mapinfo = dict[0]
                countryvalues = mapinfo[country]
                countryvalues = countryvalues.split(' ')
                value = countryvalues.pop(0)
                

        if whatinfo == 'value':
            return value
        elif whatinfo == 'adjacencies':
            return countryvalues
        elif whatinfo == "all":
            return value,countryvalues
        elif whatinfo == "text":
            return self.strDictTupleDict(dict[1])
        elif whatinfo == "colour":
            return self.strDictTupleDict(dict[2])
        elif whatinfo == 'circles':
            return self.strDictTupleDict(dict[3])
        elif whatinfo == 'countries':
            pass
            return mapinfo.keys()
            



    
  


    def CheckEnd(self):
        if len(self._Players) == 1:
            return self._players[0]
        else:
            return False




    def checkadjacent(self,country1,country2):
        #print(self.findinfo('adjacencies',country1))
        if country2 in self.findinfo('adjacencies',country1):
            return True
   

class Game(Map):
    def __init__(self,players,gamemap:str,currPlayer:int=0,phase:str=0,gameName:str = None,restarted:bool = False):
        super().__init__(gamemap,players,gameName)
        self._players = players
        if restarted:
            self._hands = DBM.getHands(self._gameName)
        else:
            self._hands = []
            for i in self._players:
                self._hands.append(0)
        self._Phases = ["Deployment","Attack","Fortification"]
        self._CurrPlayer = currPlayer
        self._CurrPhase = phase
        self._gameName = gameName
        self._gamemap = gamemap
        self.currInputs = []
        self.nextInput = 0
        if restarted == False:
            #print(self.findinfo('countries'))
            DBM.newGame(self._gameName,self.findinfo('countries'),self._gamemap,self._players)


    def findplayers(self):
        players = list(DBM.findPlayers(self._gameName))  
        players = "".join(a for a in players if a not in "' []")
        players = players.split(",")
        return players
    

    def removePlayer(self,player:str):

        playerindex = self._players.index(player)
        self._hands.pop(playerindex)
        DBM.splitPlayerTroops(self._gameName,playerindex,self._players)
        DBM.removeplayer(self._gameName,self._hands,self._players)
        

        
    def Attack(self,attacker,attackforce,defender):

        startAttackForce = attackforce
    
        

        #############################
        ####### CLASS A SKILL #######
        ###### LIST OPERATIONS ######
        #############################
        defenceforce = DBM.findTroops(self._gameName,defender)

        while defenceforce != 0 and attackforce != 0: 

            IndividualDefender = randint(1,6)
            IndividualAttacker = randint(1,6)
            if IndividualDefender >= IndividualAttacker:
                attackforce -= 1
            else:
                defenceforce -=1

        DBM.changeTroops(self._gameName,attacker,DBM.findTroops(self._gameName,attacker)-(startAttackForce-attackforce))
        if defenceforce == 0:
            DBM.changeOccupant(self._gameName,defender,DBM.findOccupant(self._gameName,attacker))
            DBM.changeTroops(self._gameName,defender,0)
            self.countrySelectList = []
            return attackforce
        
        
        


    def DeploymentStart(self):
        Player = self._players[self._CurrPlayer]
        if  DBM.findTotalTroops(self._gameName,Player)//3 < 3:
            self._hands[self._CurrPlayer] += 3
        else:
            self._hands[self._CurrPlayer] +=  DBM.findTotalTroops(self._gameName,Player)//3
        
    def GetHandAmount(self):
        return self._hands[self._CurrPlayer]
        

    def Deploy(self,howMany,country):
        current = DBM.findTroops(self._gameName,country)
        DBM.changeTroops(self._gameName,country,current+howMany)
        self._hand = DBM.getHands(self._gameName,self._CurrPlayer) - howMany
        self._hands[self._CurrPlayer] -= howMany
        DBM.sethands(self._gameName,self._hands)
        self.ChangePhase()
    
    ##########################
    ##### CLASS A SKILL ######
    ### DEPTH FIRST SEARCH ###
    ##########################



    def depthFirstSearch(self,country1,country2):
        adjacencies = self.findinfo('adjacencies',country1)
        for country in adjacencies:
            if country == country2:
                return True
            else:
                adjacencies.append(self.findinfo('adjacencies',country))
        return False
        
   
    def Fortify(self,country1,country2,Quantity):
        if self.depthFirstSearch(country1,country2):
            DBM.changeTroops(DBM.findTroops(self._gameName,country1)-Quantity)
            DBM.changeTroops(DBM.findTroops(self._gameName,country1)+Quantity)
            self.ChangePhase()
            

        
            

        
    
    def addPlayer(self,NewPlayer):
        self._players.append(NewPlayer)
    

    def getPlayer(self):
        return self._CurrPlayer
    


    def NextPlayer(self):
        self._CurrPlayer = (self._CurrPlayer+1)%len(self._players)
        
        


    

    def checkInput(self,input): 
        if self.Players[self.CurrPlayer].getName() == self.findOccupant(self._gameName,input):
            return True
        else:
            return False

 
    def getPlayerHand(self):
        return DBM.getHands(self._gameName,self._CurrPlayer)
        
    
    def getCountryTroops(self,country):
        return DBM.findTroops(self._gameName, country)

    def checkBelongs(self,country,player):
        if DBM.findOccupant(self._gameName,country) == player:
            return True
        else:
            print(DBM.findOccupant(self._gameName,country))


    def NextInput(self):
        return self.nextInput

    def ChangePhase(self):
        self._CurrPhase = (self._CurrPhase + 1)%3
        DBM.MoveOnPhase(self._gameName,self._CurrPhase,self._players)
        if self._Phases[self._CurrPhase] == "Deployment":
            self.NextPlayer()
            self.DeploymentStart()
        
        

    def getTroops(self,country):
        return DBM.findTroops(self._gameName,country)

            
        

            
            
            
            
            



        



