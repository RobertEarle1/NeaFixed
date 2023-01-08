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

class GameInfo:

    def __init__(self):
        self.Players = []
        self.gameType = ''
        self.hostIP = None
        self.clientIp = []
    def AddPlayer(self,player:str):
        self.Players.append(player)
    def GetPlayers(self):
        return self.Players
    def SetGameType(self,Type:str):
        self.gameType = Type
    def SetHostIp(self,HostIp:int):
        self.hostIP = HostIp
    def SetClientIp(self,ClientIP:int):
        self.clientIp.append(ClientIP)
    
class sliderWindow(QWidget):
    def __init__(self,country1:str,country2:str,max:int,phase:str):
        super().__init__()
        self.layout = QGridLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setGeometry(50,50, 200, 50)
        self.slider.setMinimum(0)
        self.slider.setMaximum(max)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(2)
        self.slider.valueChanged[int].connect(self.ValueChange)
        self.label = QLabel(f'How many troops from {country1} would you like to use to {phase} {country2}?')
        self.layout.addWidget(self.label,1,1,1,1)
        self.layout.addWidget(self.slider,2,1,1,1)
        self.label = QLabel(str(0))
        self.layout.addWidget(self.label,3,1,1,1)
        self.button = QPushButton("Enter")
        self.button.clicked.connect(self.enter)
        self.layout.addWidget(self.button,4,1,1,1)
        self.setLayout(self.layout)
        
        

    def enter(self):
        return self.slider.value()
        

    def ValueChange(self,value):
        try:
            self.layout.removeWidget(self.label) #this is only possible if a widget is already created
        except:
            pass
        self.label = QLabel(str(value))
        self.layout.addWidget(self.label,3,1,1,1)
        self.setLayout(self.layout)

 


class GameWindow(game.Game):

    HEIGHT = 1200
    WIDTH = 650
    WINDOW_SIZE = (HEIGHT,WIDTH)
    SKIP =  "S"     #these will be hotkeys
    QUIT = "Q"
    OPENCHAT = "/"
    
    def __init__(self,players:list,gameMap:str='normal',currPlayer:int = 0, phase:int = 0, gameName:str = None):
        
        super().__init__(players,gameMap,currPlayer,phase,gameName)

        self.GameName = gameName
        self._players = players
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1]),pygame.RESIZABLE)
        pygame.display.set_caption("RISK")
        self._TextLocations = self.findinfo('text')

        self._colourDict = self.findinfo('colour')

        self._circleLocations = self.findinfo('circles')
        self._colourList = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]




        self._circleColours = {}

        for key, value in zip(self._players, self._colourList):
            self._circleColours[key] = value
        self.__loadMap()

        currentPlayer = []


    def dotext(self,text:str,locationx:int,locationy:int):        
        font1 = pygame.font.SysFont('freesanbold.ttf', 15)
        text1 = font1.render(text, True, (0, 0, 0))   
        textRect1 = text1.get_rect()
        textRect1.center = int(locationx), int(locationy)
        self.screen.blit(text1, textRect1)
    

    
        

    
    

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
        for Country in self._circleLocations:
            colour = self._circleColours[DBM.findOccupant(self.GameName,Country)]
            pygame.draw.circle(self.screen, colour,
                   [int(self._circleLocations[Country][0]), int(self._circleLocations[Country][1])], 10, 0)
            self.dotext(str(DBM.findTroops(self.GameName,Country)),self._circleLocations[Country][0], self._circleLocations[Country][1])
                


    def __loadMap(self):
        try:
            time.sleep(1)
            icon = pygame.image.load("map.png").convert()
            self.screen.blit(icon,(0,0))
            pygame.display.flip()
            pygame.display.set_icon(icon)

        except FileNotFoundError:
            pass
    def inputNumber(self,country1,country2,max):
        
        while True:
            pass



    def MainLoop(self):
        self.doNames()
        countryselect = None
        while countryselect != "Ocean":
            self.docircles()
            pygame.display.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mouseX,mouseY = pygame.mouse.get_pos()
                    colourClick = str(self.screen.get_at((mouseX,mouseY))).strip("()")
                    countryselect = (self._colourDict[colourClick])[0]
                    print(countryselect)

                    if event.type == pygame.QUIT:
                        pygame.quit()         
                    elif self.NextInput() == 'num':
                        Country1, Country2, Max, Phase = self.getSliderInfo()
                        app = QApplication(sys.argv)
                        self.w = sliderWindow(Country1,Country2,Max,Phase)
                        self.w.show()
                        
                        
                    else:
                        self.HandleClick(countryselect)



                          
    
x = GameWindow(['bill','agua'],'normal',0,0,'athma')
x.MainLoop()

class JoinGame(QWidget):
    def __init__(self,Username:str):
        super().__init__()
        self.Username = Username
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Host IP'] = QLabel('Host IP')
        labels['Host IP'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.lineEdits['Host IP'] = QLineEdit()
        layout.addWidget(labels['Host IP'],            0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Host IP'],    0, 1, 1, 3)
        button = QPushButton("Enter")
        button.clicked.connect(self.Connect)
        layout.addWidget(button,                  2, 3, 1, 1)
        self.pwStatus = QLabel('')
        self.pwStatus.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.pwStatus, 3, 0, 1, 3)

    def Connect(self):
        IP = self.lineEdits['Host IP'].text()
        print(IP)

class GameCreate(QWidget):
    def __init__(self,UsernameList:list):
        super().__init__()
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

        button = QPushButton("CREATE")
        button.clicked.connect(self.CreateGame)

        layout.addWidget(button,                  2, 3, 1, 1)

        self.pwStatus = QLabel('')
        self.pwStatus.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.pwStatus, 3, 0, 1, 3)
    


    def CreateGame(self):
        gameName = self.lineEdits['GameName'].text()
        self.thisGame = GameWindow(self.UsernameList,'normal',0,0,gameName)
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
        combobox = QComboBox()
        combobox.addItems(DBM.findplayergames(Username))
        button = QPushButton("SELECT")
        button.clicked.connect(self.loadgame)
        layout.addWidget(label)
        layout.addWidget(combobox)
        layout.addWidget(button)

    def loadgame(self):
        self.close()
        self.w = LoginWindow()


class PassNPlayWindow(QWidget):
    def __init__(self,UsernameList:list):
        super().__init__()
        self.UsernameList = UsernameList
        self.setWindowTitle(f"Pass 'N Play")
        self.setWindowIcon(QIcon(''))
        layout = QGridLayout()
        self.setLayout(layout)
        button = QPushButton("LOGIN")
        button.clicked.connect(self.login)
        layout.addWidget(button)

        button1 = QPushButton("SIGNUP")
        button1.clicked.connect(self.signup)
        layout.addWidget(button1)

        if len(UsernameList) > 1:
            button2 = QPushButton("START GAME")
            button2.clicked.connect(self.start)
            layout.addWidget(button2)



        for name in self.UsernameList:
            self.label = QLabel(name)
            layout.addWidget(self.label)

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
        joingamebutton = QPushButton("Join Onlne")
        joingamebutton.clicked.connect(self.joingame)
        layout.addWidget(joingamebutton)

        hostgamebutton = QPushButton("Host Online")
        hostgamebutton.clicked.connect(self.creategame)
        layout.addWidget(hostgamebutton)

        passNplay = QPushButton("New Pass 'n play")
        passNplay.clicked.connect(self.PassNPlay)
        layout.addWidget(passNplay)

        LoadpassNplay = QPushButton("Load Pass 'n play")
        LoadpassNplay.clicked.connect(self.LoadpassNPlay)
        layout.addWidget(LoadpassNplay)


        settings = QPushButton("Settings")
        settings.clicked.connect(self.dosettings)
        layout.addWidget(settings)


        help = QPushButton("Help")
        help.clicked.connect(self.dohelp)
        layout.addWidget(help)



    def joingame(self):
        self.w= JoinGame(self.Username)
        self.w.show()
        self.close()
        

    def creategame(self):
        pass


    def dosettings(self):
        pass
    
    def LoadpassNPlay(self):
        self.w = LoadPassNPlayWindow(self.Username)
        self.w.show()
        self.close()

    def PassNPlay(self):
        self.w = PassNPlayWindow([self.Username])
        self.w.show()
        self.close()

    def dohelp():
        pass


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

        self.pwStatus = QLabel('')
        self.pwStatus.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.pwStatus, 3, 0, 1, 3)

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
            if Valid == True:
                self.alreadyIn.append(username)
                self.close()
                self.w = PassNPlayWindow(self.alreadyIn) # reopen the PassNPlay window but with more usernames signed in.
                self.w.show()
        
        elif Valid == False:
            self.pwStatus.setText('Incorrect credentials')
        else:
            raise ValueError
        
        

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
        elif Valid == False:
            self.pwStatus.setText('This Username is in use')
        else:
            raise ValueError
    




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


class UI():
    def __init__(self):
        self.Username = None
        self.prevWindows = []
    
    def createLoginWindow(self):
        pass



app = QApplication(sys.argv)
w = SignUpSignIn()
w.show()
app.exec()
