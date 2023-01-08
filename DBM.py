import hashlib
import os
import sqlite3
from contextlib import contextmanager
from random import randint
import datetime
   


pepper = b'e\x91\x83Z\xf8W\xec\xdc\xeb8\xc0\xcbj\x90\x1a\x98)<\xb8F\x1e.R,\xf8\xae\xee[\xb8\xbb\xba\x13'
countries = ["Alaska","NorthWestTerritory","Alberta","WesternUS","CenteralAmerica","Ontario","Quebec","Greenland","EasternUS","Venezuela","Peru","Brazil","Argentina","NorthAfrica","Congo","EastAfrica","SouthAfrica","Madagascar","Egypt","MiddleEast","India","Siam","Indonesia","NewGuinea","EasternAustralia","China","Afghanistan","Ural","Siberia","Yatusk","Kamchatka","Ukraine","Irkutsk","NorthernEurope","Scandinavia","Iceland","GreatBritain","Japan","Mongolia","WesternAustralia","Scandinavia","SouthernEurope","WesternEurope"]


@contextmanager
def openDB(db: str) -> sqlite3.Cursor:
    conn = sqlite3.connect(db)
    try:
        cur = conn.cursor()
        yield cur
    finally:
        conn.commit()
        conn.close()

def myHasher():
    pass    

with openDB("database.db") as db:
    db.execute(f"CREATE TABLE IF NOT EXISTS GAMES (GameName TEXT, LastSaved TEXT, UserName TEXT)")
    db.execute(f"CREATE TABLE IF NOT EXISTS GAMELOADSTATS (Gamename TEXT, Phase TEXT, PlayerTurn TEXT, Players TEXT)")
    db.execute(f"CREATE TABLE IF NOT EXISTS UserNamePassword (UserName TEXT,Password TEXT, Salt, TEXT)")

def newGame(GameName:str,countries:list, gametype: str,players : list):
    if gametype != None:
        with  openDB("database.db") as db:
            db.execute(f"CREATE TABLE IF NOT EXISTS {GameName} (CountryName TEXT,Occupier TEXT,Troops INT(255))")
            data = []
            for i in  countries:
                data.append((i,players[randint(0,len(players)-1)], randint(2,5)))
            db.executemany(f"INSERT INTO {GameName} VALUES(?,?,?)", data)

            db.execute(f"INSERT INTO GAMELOADSTATS (Gamename,Phase,PlayerTurn,Players) VALUES(?,?,?,?)",(GameName,0,0,str(players)))

            for player in players:
                db.execute(f"INSERT INTO GAMES (GameName,LastSaved,UserName) VALUES(?,?,?)",(GameName,str(datetime.datetime.now()),player))

def MoveOnPhase(GameName,nextPlayer,nextPhase,Players):
    with  openDB("database.db") as db:
        db.execute(f"UPDATE GAMELOADSTATS SET Phase = {nextPhase},Playerturn = {nextPlayer}, Players = {Players} WHERE Gamename = {GameName}")
def mergeReverseSort(alist):  
    if len(alist)>1:
        middle = len(alist)//2
        left = alist[:middle]
        right = alist[middle:]
        mergeReverseSort(left)
        mergeReverseSort(right)
        i=j=k=0
        while i < len(left) and j < len(right):
            if left[i] >= right[j]:
                alist[k]=left[i]
                i+=1
            else:
                alist[k]=right[j]
                j+=1
            k+=1
        while i < len(left):
            alist[k]=left[i]
            i+=1
            k+=1
        while j < len(right):
            alist[k]=right[j]
            j+=1
            k+=1


def findplayergames(player):   #returns a time sorted list of games (most recent first)
    with  openDB("database.db") as db:
        gameName = db.execute(f"SELECT UsernamePassword.Username, GAMES.GameName, GAMES.LastSaved FROM UsernamePassword INNER JOIN GAMES ON GAMES.UserName=UsernamePassword.UserName")
        gameName = gameName.fetchall()
        timestack = []

        for game in gameName:
            if game[0] == player:
                timestack.append([game[2],game[1]])
        mergeReverseSort(timestack)
        onlyGameNames = []
        for i in timestack:
            onlyGameNames.append(i[1])
        return onlyGameNames



        


    

def endGame(GameName):
    with  openDB("database.db") as db:
        db.execute(f"DROP TABLE { GameName};")



def changeOccupant(GameName, Country, newOccupier):
    with  openDB("database.db") as db:
        db.execute(f"UPDATE { GameName} SET Occupier = '{newOccupier}' WHERE CountryName = '{Country}'")



def changeTroops(GameName, Country,NewTroops):
    with  openDB("database.db") as db:
        db.execute( f"UPDATE {GameName} SET Troops = '{str(NewTroops)}' WHERE CountryName = '{Country}'")
        db.execute(f"UPDATE {GameName} SET TIMESAVED = '{str(datetime.datetime.now())}") #this line updates the game's the timestamp on every move



def findTroops(GameName, Country):
    with  openDB("database.db") as db:
        returned = db.execute(f"SELECT Troops FROM {GameName} WHERE CountryName = '{Country}'")
        returned= returned.fetchone()
        returned = returned[0]
    return returned




def findOccupant(GameName, Country):
    with  openDB("database.db") as db:
        returned = db.execute(f"SELECT Occupier FROM {GameName} WHERE CountryName = '{Country}'")
        returned= returned.fetchone()
        returned = returned[0]
    return returned




def checkOut(GameName, player):
    with  openDB("database.db") as db:
        returned = db.execute(f"SELECT * FROM { GameName} WHERE Occupier = '{player}'")
        returned = returned.fetchone()
        try:
            if len(returned) > 0:
                return False
        except TypeError:
            return True


#newGame('normal',["Bob","Frank"])
#changeOccupant("Madagascar", "Bob")
#changeTroops("Madagascar",7)
#endGame()




def SignUp(UserName, Password):

    salt = os.urandom(32)
    cypherpassword1 = Password.encode('utf-8')+ pepper
    cypherpassword2 = hashlib.pbkdf2_hmac('sha256', cypherpassword1,
    salt,
    100000)
    #print(f"the salt {salt}")
    with openDB('database.db') as db:
        try:
            Returned = db.execute(f"SELECT Salt, Password FROM UsernamePassword WHERE UserName = '{UserName}'  ")
            Returned = Returned.fetchone()
            Returned[0] #this throws an error if it can return a value with the given username
            return False

        
        except: 
            db.execute(f"INSERT INTO UsernamePassword (UserName, Password, Salt) VALUES (?,?,?) ",(UserName,cypherpassword2,salt))
            return True


def SignIn(UserName, PasswordTest):
    try:
        with openDB('database.db') as db:
            Returned = db.execute(f"SELECT Salt, Password FROM UsernamePassword WHERE UserName = '{UserName}'  ")
            Returned = Returned.fetchone()
            
            Salt = Returned[0]
            Password = Returned[1]

        PasswordTest = PasswordTest.encode('utf-8')+ pepper

        PasswordTest = hashlib.pbkdf2_hmac('sha256', PasswordTest,
        Salt,
        100000)
        if Password == PasswordTest:
            return True    
        else:
            return False
    except:
        return False

#SignUp('hacker','1')
#newGame('a','normal',['hacker','bill'])
