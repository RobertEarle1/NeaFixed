from random import randint
import json
from pydoc import locate
import DBM


class Player:
    def __init__(self,name):
        self._playerName = name
        self._playerTerritories= {}
        self._playerCards= []
        self._connection = None
        
        
    def getConnection(self):
        return self._connection
    
    def setConnection(self, conn):
        self._connection = conn
    
    def getName(self):
        return self._playerName

    

class Map:
    def __init__(self,map):
        self._map = map
        self._countries = DBM.countries

    def getcountries(self):
        return self._countries





    def findinfo(map,country,whatinfo):
        if map =="normal":
            with open('Normal.txt', 'r') as f:
                mydict = json.loads(f.read())
                countryinfo = mydict[country]
                countryinfo = countryinfo.split(" ")
                adjacencies = []
                for i in range(len(countryinfo)):
                    if i == 0:
                        value = countryinfo[0]
                    else:
                        adjacencies.append(countryinfo[i])
        if whatinfo == 'value':
            return value
        if whatinfo == 'adjacencies':
            return adjacencies
        if whatinfo == "all":
            return value,adjacencies

    def CheckLoss(Players):
        for player in Players:
            if DBM.checkOut(player) is True:
                Players.remove(player)

    def CheckEnd(Players):
        if len(Players) == 1:
            return Players[0]
        else:
            return False




    def checkadjacent(country1,country2):
        if country2 in Map.findinfo("normal",country1,'adjacencies'):
            return True
   



    def checkenough(country,force):
        if force < DBM.findTroops(country):
            return True


      




    def ModifyOccupiers(aggressor,attackloss,destination,defenceloss):    #writes to the occupiers
        DBM.changeOccupant(destination, DBM.findOccupant(aggressor))
        DBM.changeTroops(aggressor,(DBM.findTroops(aggressor)-attackloss))
        DBM.changeTroops(destination, (DBM.findTroops(destination)-defenceloss))


class Game:
    def __init__(self):
        self._CurrPhase
        self._Players = []
        self._Phases = ["Deployment","Attack","Fortify"]
        self._CurrPlayer = None
        self._CurrPlayer = 0
        self._CurrPhase = 0

        
    def addPlayer(self,player:object):
        self._Players.append(player)
        
    def attackremains(attacker,attackforce,defender,defenceforce):
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
        map.ModifyOccupiers(attacker, attackloss, defender, defenceloss) # completes the ModifyOccupiers function


    def Deployment(player):
        '''with open('occupiers.txt', 'r+') as f:
            filecontents = json.loads(f.read())
            countries = []
            for i in filecontents:
                if filecontents[i][0].find(player):
                    countries.append(i)
            troopsdeployable = int(len(countries)/3)
            Deployto = input(f"{chr(10)}{chr(10)}{chr(10)}{player} you have {troopsdeployable} to deploy in {countries} {chr(10)} Where would you like to deploy these {troopsdeployable} to?")
            filecontents[Deployto][1] += troopsdeployable
            f.read()
            f.seek(0)
            f.truncate(0)
            json.dump(filecontents, f)
            f.close()'''


    def Attack(player):
        Over = False
        print(f"{chr(10)}{chr(10)}{chr(10)}{chr(10)} Attack Phase")
        while Over == False:
            if ThisGame.gametype == 'terminal':
                attack = input("(attacker, agressor) or x x x")
            else:
                #attack = GUI.GetInput('attack')
                pass

            attacker, defender, force = attack.split(" ")
            defenceforce = DBM.findTroops(defender)
            if attack == 'x x x':
                Over = True
            else:
                if Map.checkadjacent(attacker,defender) and Map.checkenough(attacker,force):    
                    ThisGame.attackremains(attacker,force,defender,defenceforce)

   
    def Fortify(player):
        pass

        
    
    def addPlayer(self,NewPlayer):
        self._Players.append(NewPlayer)
    
    def getPhase(self):
        return self._CurrPhase

    def getPlayer(self):
        return self._CurrPlayer
    
    def NextPhase(self):
        self._CurrPhase+=1
        self._CurrPhase = self._Phases(self._CurrPhase)

    def NextPlayer(self):
        self._CurrPlayer = self._Players[self._CurrPlayer+1]



    



Players = []
CurrPlayer = 0
ThisGame = Game

def HandleClick():
    pass

def initiatePlayer(name):
    NewPlayer = Player(name)
    ThisGame.addPlayer(NewPlayer)


inputs = []

def checkInput(input): 
    if Players[CurrPlayer].getName() == DBM.findOccupant(input):
        return True
    else:
        return False

def requestNumber():
    return "GetInputNum"

def HandleClick(userInput):

    inputType = checkInput()

    if inputType:
        inputs.append(userInput)

    if len(inputs) == 2:
        requestNumber()
        
    if len(inputs) == 3:
        if ThisGame.getPhase() == "Deployment":
            ThisGame.Deployment(inputs[0],inputs[1],inputs[2])
        if ThisGame.getPhase() == "Attack":
            ThisGame.Attack(inputs[0],inputs[1],inputs[2])
        if ThisGame.getPhase() == "Fortify":
            ThisGame.Fortify(inputs[0],inputs[1],inputs[2])
    

    


