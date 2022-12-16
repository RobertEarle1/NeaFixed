import hashlib
import os
import sqlite3
from contextlib import contextmanager
from random import randint
   


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



def newGame(gametype: str,players : list,GameName):
    if gametype != None:
        with openDB("database.db") as db:
            db.execute(f"CREATE TABLE IF NOT EXISTS {GameName} (CountryName TEXT,Occupier TEXT,Troops INT(255))")
            data = []
            for i in countries:
                data.append((i,players[randint(0,len(players)-1)], randint(2,5)))
            db.executemany("INSERT INTO Game VALUES(?,?,?)", data)



def endGame():
    with openDB("database.db") as db:
        db.execute("DROP TABLE Game;")



def changeOccupant(Country, newOccupier):
    with openDB("database.db") as db:
        db.execute(f"UPDATE Game SET Occupier = '{newOccupier}' WHERE CountryName = '{Country}'")



def changeTroops(Country,NewTroops):
    with openDB("database.db") as db:
        db.execute( f"UPDATE Game SET Troops = '{str(NewTroops)}' WHERE CountryName = '{Country}'")



def findTroops(Country):
    with openDB("database.db") as db:
        returned = db.execute(f"SELECT Troops FROM Game WHERE CountryName = '{Country}'")
        returned= returned.fetchone()
        returned = returned[0]
    return returned




def findOccupant(Country):
    with openDB("database.db") as db:
        returned = db.execute(f"SELECT Occupier FROM Game WHERE CountryName = '{Country}'")
        returned= returned.fetchone()
        returned = returned[0]
    return returned




def checkOut(player):
    with openDB("database.db") as db:
        returned = db.execute(f"SELECT * FROM Game WHERE Occupier = '{player}'")
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


def CreateAccounts():
    pass



def SignUp(UserName, Password):

    salt = os.urandom(32)
    cypherpassword1 = Password.encode('utf-8')+pepper
    cypherpassword2 = hashlib.pbkdf2_hmac('sha256', cypherpassword1,
    salt,
    100000)
    #print(f"the salt {salt}")
    with openDB('accounts.db') as db:
        try:
            Returned = db.execute(f"SELECT Salt, Password FROM UsernamePassword WHERE UserName = '{UserName}'  ")
            Returned = Returned.fetchone()
            Returned[0]
            return False

        
        except: 
            print('works')
            db.execute(f"INSERT INTO UsernamePassword (UserName, Password, Salt) VALUES (?,?,?) ",(UserName,cypherpassword2,salt))
            return True


def SignIn(UserName, PasswordTest):
    try:
        with openDB('accounts.db') as db:
            Returned = db.execute(f"SELECT Salt, Password FROM UsernamePassword WHERE UserName = '{UserName}'  ")
            Returned = Returned.fetchone()
            
            Salt = Returned[0]
            Password = Returned[1]

        PasswordTest = PasswordTest.encode('utf-8')+pepper

        PasswordTest = hashlib.pbkdf2_hmac('sha256', PasswordTest,
        Salt,
        100000)
        if Password == PasswordTest:
            return True    
        else:
            return False
    except:
        return False


    


        

#
#SignUp("Rob","MyPassword")
#SignIn("Rob","MyPassword")
 