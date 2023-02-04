import pygame
import game
import time
import game
import DBM
from tkinter import *
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy, QVBoxLayout,QSlider,QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from numpy import random

    
class sliderWindow(QWidget):
    def __init__(self,country1:str,country2:str,max:int,phase:str,verb:object,remains:int = None):
        super().__init__()
        self.remains = remains
        self.function = verb
        self.country1 = country1
        self.country2 = country2
        self.layout = QGridLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setGeometry(50,50, 200, 50)
        self.slider.setMinimum(0)
        self.slider.setMaximum(max) #max
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(2)
        self.slider.valueChanged[int].connect(self.ValueChange)
        self.label = QLabel(f'How many troops from {self.country1} would you like to use to {phase} {self.country2}?')
        self.layout.addWidget(self.label,1,1,1,1)
        self.layout.addWidget(self.slider,2,1,1,1)
        self.label = QLabel(str(0))
        self.layout.addWidget(self.label,3,1,1,1)
        self.button = QPushButton("Enter")
        self.button.clicked.connect(self.enter)
        self.layout.addWidget(self.button,4,1,1,1)
        self.setLayout(self.layout)
        self.value = 0



    def enter(self):
        self.value = self.slider.value()
        if self.remains == None:
            self.function(self.country1,self.country2,self.value)
        else:
            self.function(self.country1,self.country2,self.value,self.remains)
        self.close()
        
    def getValue(self):
        return self.value


    def ValueChange(self,value):
        try:
            self.layout.removeWidget(self.label) #this is only possible if a widget is already created
        except:
            pass
        self.label = QLabel(str(value))
        self.layout.addWidget(self.label,3,1,1,1)
        self.setLayout(self.layout)


       

 


class GameWindow(game.Game):

    def __init__(self,players:list,gameMap:str='Regular',currPlayer:int = 0, phase:int = 0, gameName:str = None,restarted : bool = False,gameMode:str = None):
        super().__init__(players,gameMap,currPlayer,phase,gameName,restarted,gameMode)
        if restarted ==False:
            DBM.newGame(gameName,self.findinfo('countries'),gameMap,self._players)
        self.WINDOW_SIZE = (2000,600)
        self.gameMode = gameMode
        self.GameName = gameName
        self._players = players
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1]),pygame.RESIZABLE)
        pygame.display.set_caption("RISK")
        self.screen.fill('White')
        self._TextLocations = self.findinfo('text')
        self._colourDict = self.findinfo('colour')
        self._circleLocations = self.findinfo('circles')
        self._colourList = [(250,0,0),(0,250,0),(0,0,250),(255,250,0),(250,0,255),(0,205,255),(80,205,255),(125,205,40)]
        self.sliderOn = False



        self._circleColours = {}
        for i in range(len(self._players)):
            self._circleColours.update({self._players[i]:self._colourList[i]})
        self.__loadMap()

        currentPlayer = []




    def dotext(self,text:str,locationx:int,locationy:int,size:int = 15,colour = (0,0,0)):        
        font1 = pygame.font.SysFont('freesanbold.ttf', size)
        text1 = font1.render(text, True, (colour))   
        textRect1 = text1.get_rect()
        textRect1.center = int(locationx), int(locationy)
        self.screen.blit(text1, textRect1)
    
    
    def clearSidebar(self):
        self.screen.fill("White",(1200,0,400,600))

    def doNames(self):
        for Country in self._TextLocations:
            locationx, locationy = self._TextLocations[Country]
            self.dotext(Country,locationx,locationy)



    def get_colours(self,colour):
        return self._colourDict[colour]



    def findButton(self,colour):
        try: return self.get_colours(colour)
        except: raise NotImplementedError



    def docircles(self):
        if self.gameMode == 'Regular':
            for Country in self._circleLocations:
                colour = self._circleColours[DBM.findOccupant(self.GameName,Country)]
                pygame.draw.circle(self.screen, colour,[int(self._circleLocations[Country][0]), int(self._circleLocations[Country][1])], 10, 0)
                self.dotext(str(DBM.findTroops(self.GameName,Country)),self._circleLocations[Country][0], self._circleLocations[Country][1])
        
        else:
            for Country in self._circleLocations:
                pygame.draw.circle(self.screen, (50,50,50), [int(self._circleLocations[Country][0]),int(self._circleLocations[Country][1])], 10, 0)
        
            for Country in self._circleLocations:
                Occupier = DBM.findOccupant(self.GameName,Country)
                if Occupier == self._players[self._CurrPlayer]:
                    colour = self._circleColours[DBM.findOccupant(self.GameName,Country)]
                    pygame.draw.circle(self.screen, colour,[int(self._circleLocations[Country][0]), int(self._circleLocations[Country][1])], 10, 0)
                    self.dotext(str(DBM.findTroops(self.GameName,Country)),self._circleLocations[Country][0], self._circleLocations[Country][1])
                    adj = (self.findinfo('adjacencies',Country))
                    for i in adj:
                            pygame.draw.circle(self.screen, self._circleColours[DBM.findOccupant(self.GameName,i)],[int(self._circleLocations[i][0]), int(self._circleLocations[i][1])], 10, 0)
                            self.dotext(str(DBM.findTroops(self.GameName,i)),self._circleLocations[i][0], self._circleLocations[i][1])

                
    def doPlayers(self):
        for i in range(len(self._players)):
            self.dotext(self._players[i],1280,500 - 50*i,40)
            colour = self._circleColours[self._players[i]]
            pygame.draw.circle(self.screen, colour,[1380,500 - 50*i],20)

    def doPhase(self):
        self.dotext(f'PHASE: {self._Phases[self._CurrPhase]}',1330, 160,30) #this writes new text

    def doTurn(self):
        self.dotext(f'TURN: {self._players[self._CurrPlayer]}',1300, 100,50) #this writes new text




    def __loadMap(self):
        if self._gamemap == 'Regular':
            file = "map.png"
        else:
            file = "HexMap.png"
        try:
            time.sleep(1)
            icon = pygame.image.load(file).convert()
            self.screen.blit(icon,(0,0))
            pygame.display.flip()
            pygame.display.set_icon(icon)

        except FileNotFoundError:
            pass



    def GuiAttack(self,country1,country2,number):
        remains = self.Attack(country1,country2,number)
        self.slider = sliderWindow(country1,country2,number,'invade',self.Invade,remains)
        self.slider.show()


            
    def MainLoop(self):
        self.doNames()
        self.doTurn()
        self.countrySelect = None
        self.doPlayers()
        self.countrySelectList = []

        
        while len(self._players) > 1:
        
            if len(self._players) ==1:
                pass
            self.clearSidebar()
            self.docircles()
            self.doTurn()
            self.doPhase()
            self.doPlayers()
            pygame.display.update()
            events = pygame.event.get()
            invading = False
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
       
                    mouseX,mouseY = pygame.mouse.get_pos()
                    colourClick = str(self.screen.get_at((mouseX,mouseY))).strip("()")
                    try:
                        self.countrySelect = (self._colourDict[colourClick])[0]
                    except:
                        pass


                    if self.countrySelect == 'Surrender':

                        self.removePlayer(self._players[self._CurrPlayer])
                        self.countrySelectList = []
                        self.countrySelect = None
                    
                    
                    elif self.countrySelect == 'NextPhase':
                        self.countrySelectList = []
                        self.ChangePhase()
                        self.countrySelect = None


                    
                    elif self._Phases[self._CurrPhase] == 'Attack':  #getting initial inputs
                        if len(self.countrySelectList) == 0:
                            if self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]):
                                self.countrySelectList.append(self.countrySelect)

                        elif len(self.countrySelectList) ==1:
                            if not self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]):
                                self.countrySelectList.append(self.countrySelect)
                                print(self.countrySelectList)
                                self.slider = sliderWindow(self.countrySelectList[0],self.countrySelectList[1],DBM.findTroops(self._gameName,self.countrySelectList[0])-1,'Attack',self.GuiAttack)
                                self.slider.show()
                                self.countrySelectList= []
                                
                                
                
                            
                    elif self._Phases[self._CurrPhase]  == 'Fortification':  #getting initial inputs
                        if len(self.countrySelectList) == 0:
                            if self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]):
                                self.countrySelectList.append(self.countrySelect)

                        elif len(self.countrySelectList) == 1:
                            if self.countrySelect == self.countrySelectList[0]:
                                self.countrySelectList = []
                            elif self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]) and self.depthFirstSearch(self.countrySelect,self.countrySelectList[0]) : 
                                self.countrySelectList.append(self.countrySelect) 
                                self.slider = sliderWindow(self.countrySelectList[0],self.countrySelectList[1],DBM.findTroops(self.GameName,self.countrySelectList[0])-1,'fortify',self.Fortify)
                                self.slider.show()  
                            else:
                                self.countrySelectList = [] 
                                
                        

                    
                    elif self._Phases[self._CurrPhase]  == 'Deployment' and  self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]):
                        self.slider = sliderWindow('your hand',self.countrySelect,self.getPlayerHand(),self._Phases[self._CurrPhase],self.Deploy)
                        self.slider.show()
                        self.countrySelectList = []


                    



                    
                    
        self.winner()       






class GameCreate(QWidget):
    def __init__(self,UsernameList:list,connection:object = None):
        super().__init__()
        self.connection = connection
        self.UsernameList = UsernameList
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)
        layout = QGridLayout()
        self.setLayout(layout)
        labels = {}
        self.lineEdits = {}
        labels['GameName'] = QLabel('Game Name:')
        labels['GameName'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.lineEdits['GameName'] = QLineEdit()
        layout.addWidget(labels['GameName'],            0, 0, 1, 1)
        layout.addWidget(self.lineEdits['GameName'],    0, 1, 1, 3)

        self.combobox1 = QComboBox()
        self.combobox1.addItems(['Regular','simplified'])

        self.combobox2 = QComboBox()
        self.combobox2.addItems(['Regular','Fog of war'])
        
        layout.addWidget(self.combobox1)
        layout.addWidget(self.combobox2)



        button = QPushButton("CREATE")
        button.clicked.connect(self.CreateGame)

        layout.addWidget(button,                  2, 3, 1, 1)

        self.pwStatus = QLabel('')
        self.pwStatus.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.pwStatus, 3, 0, 1, 3)
    


    def CreateGame(self):
        gameName = self.lineEdits['GameName'].text()
        self.thisGame = GameWindow(self.UsernameList,self.combobox1.currentText(),0,0,gameName,False,self.combobox2.currentText())
        self.thisGame.MainLoop()
        self.close()

class LoadPassNPlayWindow(QWidget):
    def __init__(self,Username:str):
        super().__init__()
        self.Username = Username
        self.setWindowTitle(f"LOAD GAME")
        label = QLabel('SELECT GAME')
        layout = QGridLayout()
        self.setLayout(layout)
        self.combobox = QComboBox()
        self.combobox.addItems(DBM.findplayergames(Username))
        button = QPushButton("SELECT")
        button.clicked.connect(self.reloadTheGame)
        layout.addWidget(label)
        layout.addWidget(self.combobox)
        layout.addWidget(button)

    def reloadTheGame(self):
        self.close()
        chosenGame = str(self.combobox.currentText())
        details = list(DBM.loadGame(chosenGame))
        self.w = GameWindow(eval(details[2]),details[3],int(details[1]),int(details[0]),chosenGame,True,None)
        self.w.MainLoop()

        
    
        


class PassNPlayWindow(QWidget):
    def __init__(self,UsernameList:list):
        super().__init__()
        self.UsernameList = UsernameList
        self.setWindowTitle(f"Pass 'N Play")
        self.setWindowIcon(QIcon(''))
        layout = QGridLayout()
        self.setLayout(layout)
        button = QPushButton("Login")
        button.clicked.connect(self.login)
        layout.addWidget(button)

        button1 = QPushButton("Signup")
        button1.clicked.connect(self.signup)
        layout.addWidget(button1)

        button2 = QPushButton("Back")
        button2.clicked.connect(self.back)
        layout.addWidget(button2)

        if len(UsernameList) > 1:
            button2 = QPushButton("START GAME")
            button2.clicked.connect(self.start)
            layout.addWidget(button2)



        for name in self.UsernameList:
            self.label = QLabel(name)
            layout.addWidget(self.label)
    
    def back(self):
        self.close()
        self.w = MainMenu(self.UsernameList[1])
        self.w.show()

    def login(self):
        self.close()
        self.w = LoginWindow(self.UsernameList)
        self.w.show()
        

    def start(self):
        self.w = GameCreate(self.UsernameList)
        self.w.show()
        self.close()


    def signup(self):
        self.close()
        self.w = SignUpWindow(self.UsernameList)
        self.w.show()
    

class HelpWindow(QWidget):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.layout = QVBoxLayout()
        self.label = QLabel("RISK: THE RULES: RULES WILL BE INSERTED HERE CLOSER TO GAME COMPLETION\nRISK: THE RULES: RULES WILL BE INSERTED HERE CLOSER TO GAME COMPLETION\nRISK: THE RULES: RULES WILL BE INSERTED HERE CLOSER TO GAME COMPLETION\nRISK: THE RULES: RULES WILL BE INSERTED HERE CLOSER TO GAME COMPLETION\nRISK: THE RULES: RULES WILL BE INSERTED HERE CLOSER TO GAME COMPLETION\nRISK: THE RULES: RULES WILL BE INSERTED HERE CLOSER TO GAME COMPLETION\nRISK: THE RULES: RULES WILL BE INSERTED HERE CLOSER TO GAME COMPLETION\n")

        self.layout.addWidget(self.label)
        self.setWindowTitle("Help")
        self.button = QPushButton('Back')
        self.button.clicked.connect(self.goBack)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
    
    def goBack(self):
       self.w = MainMenu(self.username)
       self.w.show()
       self.close()


class StatsWindow(QWidget):
    def __init__(self,username):
        super().__init__()
        self.layout = QVBoxLayout()
        stats = DBM.findStats(username)
        self.label0 = QLabel(f"User: {username}")
        self.label1 = QLabel(f"Games Lost: {stats[0]}")
        self.label2 = QLabel(f"Games won: {stats[1]}")
        self.label3 = QLabel(f"Winrate: {int(stats[1])/int(stats[0])} ")
        self.layout.addWidget(self.label0)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.setLayout(self.layout)


class MainMenu(QWidget):
    def __init__(self,Username):
        super().__init__()
        self.Username = Username
        self.setWindowTitle(f'Risk Menu                                                                  Username  = {Username}')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)
        self.lineEdits = {}


        passNplay = QPushButton("New Pass 'n play")
        passNplay.clicked.connect(self.PassNPlay)
        layout.addWidget(passNplay)

        LoadpassNplay = QPushButton("Load Pass 'n play")
        LoadpassNplay.clicked.connect(self.LoadpassNPlay)
        layout.addWidget(LoadpassNplay)

        statsOpen = QPushButton("Stats")
        statsOpen.clicked.connect(self.statsOpen)
        layout.addWidget(statsOpen)


        help = QPushButton("Help")
        help.clicked.connect(self.dohelp)
        layout.addWidget(help)





    def statsOpen(self):
        self.w = StatsWindow(self.Username)
        self.w.show()
        self.close()
    
    def LoadpassNPlay(self):
        self.w = LoadPassNPlayWindow(self.Username)
        self.w.show()
        self.close()

    def PassNPlay(self):
        self.w = PassNPlayWindow([self.Username])
        self.w.show()
        self.close()

    def dohelp(self):
        self.w = HelpWindow(self.Username)
        self.w.show()


class LoginWindow(QWidget):

    def __init__(self,alreadyIn=[]):
        super().__init__()
        self.setWindowTitle('RISK LOGIN')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)

        self.alreadyIn = alreadyIn

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel('Username')
        labels['Password'] = QLabel('Password')
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Username'],            0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Username'],    0, 1, 1, 3)

        layout.addWidget(labels['Password'],            1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'],    1, 1, 1, 3)

        button = QPushButton("Login")
        button.clicked.connect(self.CheckInputs)
        layout.addWidget(button,                  2, 3, 1, 1)

        button = QPushButton("Back")
        button.clicked.connect(self.back)
        layout.addWidget(button,                  2, 1, 1, 1)

        self.pwStatus = QLabel('')
        self.pwStatus.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.pwStatus, 3, 0, 1, 3)

    def back(self): # this function is called by the back button and opens the previous window
        if self.alreadyIn == []:
            self.w = SignUpSignIn()
            self.w.show()
        else:
            self.w = PassNPlayWindow(self.alreadyIn) # reopen the PassNPlay window but with more usernames signed in.
            self.w.show()
        self.close()
            

    def CheckInputs(self):
        Valid = False
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()
        Valid = DBM.SignIn(username,password)
        if self.alreadyIn == []:    #if no one is signed in yet.
            if Valid == True:
                self.close()
                self.w = MainMenu(username)
                self.w.show()
        elif self.alreadyIn != []:    #if someone is already signed in.
            if Valid == True and username not in self.alreadyIn:
                self.alreadyIn.append(username)
                self.close()
                self.w = PassNPlayWindow(self.alreadyIn) # reopen the PassNPlay window but with more usernames signed in.
                self.w.show()
        
        if Valid == False:
            self.pwStatus.setText('Incorrect credentials')

        
        

class SignUpWindow(QWidget):
    def __init__(self, alreadyIn = []):
        super().__init__()
        self.setWindowTitle('RISK SIGNUP')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)
        self.alreadyIn = alreadyIn

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel('Username')
        labels['Password'] = QLabel('Password')
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Username'],            0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Username'],    0, 1, 1, 3)

        layout.addWidget(labels['Password'],            1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'],    1, 1, 1, 3)

        button = QPushButton("Login")
        button.clicked.connect(self.UseInputs)

        layout.addWidget(button,                  2, 3, 1, 1)

        self.pwStatus = QLabel('')
        self.pwStatus.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.pwStatus, 3, 0, 1, 3)

        button = QPushButton("Back")
        button.clicked.connect(self.back)
        layout.addWidget(button,                  2, 1, 1, 1)



    def back(self):  # this function is called by the back button and opens the previous window
        if self.alreadyIn == []:
            self.w = SignUpSignIn()
            self.w.show()
        else:
            self.w = PassNPlayWindow(self.alreadyIn) # reopen the PassNPlay window but with more usernames signed in.
            self.w.show()
        self.close()

    def UseInputs(self):
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()
        Valid = False

        Valid = DBM.SignUp(username,password)
        if Valid == True:
            if len(self.alreadyIn)>0:
                self.alreadyIn.append(username)
                self.w = PassNPlayWindow(self.alreadyIn)
                self.w.show()
            else:
                self.w = MainMenu(username)
                self.w.show()
            self.close()
        if Valid == False:
            self.pwStatus.setText('This Username is in use')

    




class SignUpSignIn(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("RISK")

 
        layout = QVBoxLayout()
        self.setLayout(layout)
 
        self.label = QLabel("RISK")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        layout.addWidget(self.label)
 
        button = QPushButton("LOGIN")
        button.clicked.connect(self.login)
        layout.addWidget(button)
 
        button1 = QPushButton("SIGNUP")
        button1.clicked.connect(self.signup)
        layout.addWidget(button1)


    def login(self):
        self.w = LoginWindow()
        self.w.show()
        self.close()
            

    def signup(self):
        self.w = SignUpWindow()
        self.w.show()
        self.close()





app = QApplication(sys.argv)
#w = GameWindow(['1','2'],'Regular',0,0,'skitzo',True) #SignUpSignIn()
w = SignUpSignIn()
#w.MainLoop()
w.show()
app.exec()