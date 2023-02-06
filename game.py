from random import randint
import json
from pydoc import locate
import DBM

class Map:  #This is the map class, the game class inherits from this.

    def __init__(self,map:str,gameName:str):
        self._gameName = gameName #set the gamename
        self._map = map #set the map type




    def strDictTupleDict(self,givenDict:str): #this is a function i wrote to get the informatinon from map.txt and HexMap.txt into a pythonic data structure.
        #note that givenDict is actually a string representation of a dict.
        tupledict = {}
        for pair in givenDict: 
            string = givenDict[pair]
            my_result = string.split(',')
            tuple1 = tuple(my_result)
            tupledict.update({pair:tuple1})
        return tupledict




    def findinfo(self,whatinfo:str,country:str=None): #this fucntion is called to read from the textfiles different map information.
        if self._map =="Regular":
            with open('normal.txt', 'r') as f:  #use the data from normal.txt if this is a regular game.
                dict = (json.loads(f.read()))
                mapinfo = dict[0]
                if country != None:
                    countryvalues = mapinfo[country]
                    countryvalues = countryvalues.split(' ')
                    value = countryvalues.pop(0)

        else:
            with open('HexMap.txt', 'r') as f:  #use the data from HexMap.txt otherwise.
                dict = (json.loads(f.read()))
                mapinfo = dict[0]
                if country != None:
                    countryvalues = mapinfo[country]
                    countryvalues = countryvalues.split(' ')
                    value = 4
                    self.text = []
                    
                

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
            return mapinfo.keys()
            

    def checkadjacent(self,country1:str,country2:str): #uses the findinfo function above to find the adjacencies of a given country.
        if country2 in self.findinfo('adjacencies',country1):
            return True
    
    ##########################
    ##### CLASS A SKILL ######
    ### DEPTH FIRST SEARCH ###
    ##########################

    def depthFirstSearch(self,country1:str,country2:str): #this checks that there is a clear path for fortified troops to move through.
        adjacencies = self.findinfo('adjacencies',country1)
        searched = []
        occupier = DBM.findOccupant(self._gameName,country1)
        for country in adjacencies:
            if country == country2:
                return True #if their is a path return true, else return None
            else:
                searched.append(country)
                for adj in self.findinfo('adjacencies',country):
                    if adj not in searched:
                        if DBM.findOccupant(self._gameName, adj) == occupier:
                            adjacencies.append(adj)

   

class Game(Map): #This is the main game, it inherits from the above map class and is inherited by the GameWindow class.
    def __init__(self,players,gamemap:str,currPlayer:int=0,phase:str=0,gameName:str = None,restarted:bool = False,gameMode:str = None):
        super().__init__(gamemap,gameName) #thses are the attributes is passes to map.
        self._players = players
        self.gameMode = gameMode
        if restarted:
            self._hands = DBM.getHands(self._gameName)
        else:
            self._hands = []
            for i in self._players:
                self._hands.append(8)
        self._Phases = ["Deployment","Attack","Fortification"]
        self._CurrPlayer = currPlayer #sets the current player
        self._CurrPhase = phase #sets the current phase
        self._gameName = gameName #sets the game name



    def removePlayer(self,player:str): #remove a player from the game and increase their losses.
        playerindex = self._players.index(player)
        self._hands.pop(playerindex)
        DBM.splitPlayerTroops(self._gameName,playerindex,self._players) #spread out their territories if they have any left(surrender)
        DBM.removeplayer(self._gameName,self._hands,self._players)
        DBM.increaseLoss(player)
        

    def winner(self): #increase the winner's wins and delete the game.
        DBM.increaseWon(self._players[0])
        DBM.endGame(self._gameName)


        
    def Attack(self,attacker:str,defender:str,attackforce:int): #this is the attack function.
        startAttackForce = attackforce
    
        

        #############################
        ####### CLASS A SKILL #######
        ###### LIST OPERATIONS ######
        #############################

        defenceforce = DBM.findTroops(self._gameName,defender) #find the size of the defence to beat.
        while defenceforce != 0 and attackforce != 0: 
            IndividualDefender = randint(1,6)
            IndividualAttacker = randint(1,6)
            if IndividualDefender >= IndividualAttacker:
                attackforce -= 1
            else:
                defenceforce -=1
        attackloss = startAttackForce-attackforce
        #Here we modify the database accordingly to how the attack went.
        DBM.changeTroops(self._gameName,attacker,DBM.findTroops(self._gameName,attacker)-(attackloss))
        DBM.changeTroops(self._gameName,defender,defenceforce)
        if defenceforce == 0:
            DBM.changeOccupant(self._gameName,defender,DBM.findOccupant(self._gameName,attacker))
            DBM.changeTroops(self._gameName,defender,0)
            return attackforce
        

        
        
        


    def DeploymentStart(self): #Increase the player's hands based on their troops.
        Player = self._players[self._CurrPlayer]
        if  DBM.findTotalTroops(self._gameName,Player)//3 < 3:
            self._hands[self._CurrPlayer] += 3
        else:
            self._hands[self._CurrPlayer] +=  DBM.findTotalTroops(self._gameName,Player)//3


    def Deploy(self,filler,country:str,howMany:int): #this is the logic for a deployment
        current = DBM.findTroops(self._gameName,country)
        DBM.changeTroops(self._gameName,country,current+howMany) #lose troops from your hand.
        self._hand = DBM.getHands(self._gameName,self._CurrPlayer) - howMany
        self._hands[self._CurrPlayer] -= howMany
        DBM.sethands(self._gameName,self._hands) #set the new hands.
        
    
 




   
    

    def Fortify(self,country1:str,country2:str,Quantity:int): #this is the logic to fortify a territory.
        if self.depthFirstSearch(country1,country2):
            DBM.changeTroops(self._gameName,country1,DBM.findTroops(self._gameName,country1)-Quantity)
            DBM.changeTroops(self._gameName,country2,DBM.findTroops(self._gameName,country2)+Quantity)
            self.countrySelect = None
            self.countSelectList = []
            self.ChangePhase()
            
    def Invade(self,country1:str,country2:str,number:int): #the logic to invade a territory.
        DBM.changeTroops(self._gameName,country1,DBM.findTroops(self._gameName,country1)-number)
        DBM.changeTroops(self._gameName,country2,DBM.findTroops(self._gameName,country2)+number)




    def NextPlayer(self): #moves on to the next player
        self._CurrPlayer = (self._CurrPlayer+1)%len(self._players)
        DBM.MoveOnTurn(self._gameName,self._CurrPlayer)
        
    
 
    def getPlayerHand(self):  #returns the hand of a player.
        return DBM.getHands(self._gameName,self._CurrPlayer)
        


    def checkBelongs(self,country,player):  #checks a country belongs to a player.
        if DBM.findOccupant(self._gameName,country) == player:
            return True
        else:
            pass

    def ChangePhase(self): #moves onto the next phase
        self._CurrPhase = (self._CurrPhase + 1)%3
        DBM.MoveOnPhase(self._gameName,self._CurrPhase)
        if self._Phases[self._CurrPhase] == "Deployment": 
            self.NextPlayer() #if this causes the player's turn to end. i.e. this happened during a fortification.
            self.DeploymentStart()
        
        
