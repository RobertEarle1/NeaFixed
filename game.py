from random import randint
import json
from pydoc import locate
import DBM

class Map:
    def __init__(self,map:str,Players:list,gameName:str):
        self._gameName = gameName
        self._map = map
        self._Players = Players

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
                value = countryvalues[0]
                adjacencies = countryvalues.remove(value)

        if whatinfo == 'value':
            return value
        elif whatinfo == 'adjacencies':
            return adjacencies
        elif whatinfo == "all":
            return value,adjacencies
        elif whatinfo == "text":
            return self.strDictTupleDict(dict[1])
        elif whatinfo == "colour":
            return self.strDictTupleDict(dict[2])
        elif whatinfo == 'circles':
            return self.strDictTupleDict(dict[3])
        elif whatinfo == 'countries':
            pass
            return mapinfo.keys()
            
        


  
  

    def CheckLoss(self):
        for player in self.players:
            if DBM.checkOut(self._gameName, player) is True:
                self._Players.remove(player)

    def CheckEnd(self):
        if len(self._Players) == 1:
            return self._Players[0]
        else:
            return False




    def checkadjacent(self,country1,country2):
        if country2 in self.findinfo('adjacencies',country1):
            return True
   



    def checkenough(self,country,force):
        if force < DBM.findTroops(self._gameName, country):
            return True


      




    def ModifyOccupiers(self,aggressor,attackloss,destination,defenceloss):    #writes to the occupiers
        DBM.changeOccupant(self._gameName,destination, DBM.findOccupant(self._gameName,aggressor))
        DBM.changeTroops(self._gameName,aggressor,(DBM.findTroops(self._gameName,aggressor)-attackloss))
        DBM.changeTroops(self._gameName,destination, (DBM.findTroops(self._gameName,destination)-defenceloss))



class Game(Map):
    def __init__(self,players,gamemap:str,currPlayer:int=0,phase:str=0,gameName:str = None,restarted:bool = False):
        super().__init__(gamemap,players,gameName)
        self._Players = players
        self._hands = []
        for i in self._Players:
            self._hands.append(30)
        self._Phases = ["Deployment","Attack","Fortification"]
        self._CurrPlayer = currPlayer
        self._CurrPhase = phase
        self._gameName = gameName
        self._gamemap = gamemap
        self.inputs = []
        self.nextInput = 0
        if restarted == False:
            #print(self.findinfo('countries'))
            DBM.newGame(self._gameName,self.findinfo('countries'),self._gamemap,self._Players)



        
    def addPlayer(self,player:object):
        self._Players.append(player)
        
    def attackremains(self,attacker,attackforce,defender,defenceforce):
        annhilation = False
        count = 0
        while annhilation == False:
            winner = False
            attackarray = []
            defencearray = []
            for i in range(attackforce):
                attackarray.append(randint(1,6))
           
            for i in range(defenceforce):
                defencearray.append(randint(1,6))  
           
            attackarray.sort(reverse=True)
            defencearray.sort(reverse=True)  

            while winner == False:
                    if attackarray[count] > defencearray[count]:
                        defenceforce -=1 #kill a defender
                        if defenceforce <= 0:
                            annhilation = 'attack win'
                            winner = True
                    elif defencearray[count] > attackarray[count]:
                        attackforce -=1
                        if attackforce <= 0:
                            annhilation = 'defence win'
                            winner = True
                    elif defencearray[count] == attackarray[count]:
                        attackforce -=1
                        if attackforce <= 0:
                            annhilation = 'defence win'
                            winner = True          
        attackloss = attackforce - len(attackarray)
        defenceloss = defenceforce - len(defencearray)
        self.ModifyOccupiers(attacker, attackloss, defender, defenceloss) # completes the ModifyOccupiers function for its map

    def DeploymentStart(self):
        Player = self._Players[self._CurrPlayer]
        if  DBM.findTotalTroops(self._gameName,Player)//3 < 3:
            self._hands[self._CurrPlayer] += 3
        else:
            self._hands[self._CurrPlayer] +=  DBM.findTotalTroops(self._gameName,Player)//3
        
    def GetHandAmount(self):
        return self._hands[self._CurrPlayer]
        

    def Deploy(self,howMany,country):
            current = DBM.findTroops(self._gameName,country)
            DBM.changeTroops(self._gameName,country,current+howMany)


    def Attack(self,player):
        Over = False
        print(f"{chr(10)}{chr(10)}{chr(10)}{chr(10)} Attack Phase")
        while Over == False:
            if self.gametype == 'terminal':
                attack = input("(attacker, agressor) or x x x")
            else:
                #attack = GUI.GetInput('attack')
                pass

            attacker, defender, force = attack.split(" ")
            defenceforce = DBM.findTroops(self._gameName,defender)
            if attack == 'x x x':
                Over = True
            else:
                if self.checkadjacent(attacker,defender) and self.checkenough(attacker,force):    
                    self.attackremains(attacker,force,defender,defenceforce)

   
    def Fortify(player):
        pass

        
    
    def addPlayer(self,NewPlayer):
        self._Players.append(NewPlayer)
    
    def getPhase(self):
        return self._Phases[self._CurrPhase]

    def getPlayer(self):
        return self._CurrPlayer
    
    def NextPhase(self):
        self._CurrPhase+=1
        self._CurrPhase = self._Phases(self._CurrPhase)

    def NextPlayer(self):
        self._CurrPlayer = self._Players[self._CurrPlayer+1]


    

    def initiatePlayer(self,name):
        NewPlayer = Player(name)
        self.addPlayer(NewPlayer)


    

    def checkInput(self,input): 
        if self.Players[self.CurrPlayer].getName() == self.findOccupant(self._gameName,input):
            return True
        else:
            return False

    def requestNumber(self):
        return "GetInputNum"
    
    def getSliderInfo(self):
        if len(self.inputs) == 2:
            return self.inputs[0],self.inputs[1], DBM.findTroops(self._gameName, self.inputs[0]), self.getPhase()
        else:
            return 'your hand', self.inputs[0], self.GetHandAmount(), self.getPhase()
        

    def HandleClick(self,userInput):
        phase = self.getPhase()
        
        if phase == "Attack":
            if len(self.inputs) ==2:
                self.Attack()

            if len(self.inputs) == 1:
                if DBM.findOccupant(self._gameName,userInput) != self._Players[self._CurrPlayer]:
                    self.nextInput = 'num'
                    self.inputs.append(userInput)
                    print(f'{userInput} is attack')
                
            if len(self.inputs) == 0:
                self.nextInput = None
                if DBM.findOccupant(self._gameName,userInput) == self._Players[self._CurrPlayer]:
                    self.inputs.append(userInput)
                    print(f'{userInput} is defend')


        elif phase == "Fortification":
            if DBM.findOccupant(self._gameName,userInput) == self._Players[self._CurrPlayer]:
                if len(self.inputs) == 1:
                    self.nextInput = 'num'
                self.inputs.append(userInput)
                print(f'fortifying {userInput}')
        else:
            if DBM.findOccupant(self._gameName,userInput) == self._Players[self._CurrPlayer]:
                print(f'deploying to {userInput}')
                self.inputs.append(userInput)
                self.nextInput = 'num'
                print('slider')
        

    def NextInput(self):
        return self.nextInput

    def ChangePhase(self):
        self._CurrPhase +=1
        if self._Phases[self._CurrPhase] == "Deployment":
            self._CurrPlayer+=1
            self.DeploymentStart()
        



            
            
            
            
            



        



