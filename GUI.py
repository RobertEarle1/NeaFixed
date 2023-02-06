import pygame
import game
import time
import game
import DBM
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy, QVBoxLayout,QSlider,QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

    
class sliderWindow(QWidget):   #I instantiate this class during my game to get inputs from my user.
    def __init__(self,country1:str,country2:str,max:int,phase:str,verb:object,remains:int = None):   
        super().__init__()
        self.remains = remains
        self.function = verb #this is the function we pass in to the slider that we want it to execute when enter is pressed.
        self.country1 = country1
        self.country2 = country2
        self.phase = phase
        self.layout = QGridLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setGeometry(50,50, 200, 50)
        self.slider.setMinimum(0)
        self.slider.setMaximum(max) #max
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(2)
        self.slider.valueChanged[int].connect(self.ValueChange)
        if phase == 'Deployment':  # Deciding what messages the window should display here.
            self.label = QLabel(f'How many troops would you like to deploy to {country2}?')
        if phase == 'attack':
            self.label = QLabel(f'How many troops from {country1} would you like to attack {country2} with?')
        if phase == "invade":
            self.label = QLabel(f"How many troops from the battle would you like to invade {country2}?")
        if phase == "fortify":
            self.label = QLabel(f"How many troops from {country1} would you like to move to {country2}?")
        self.layout.addWidget(self.label,1,1,1,1)
        self.layout.addWidget(self.slider,2,1,1,1)
        self.label = QLabel(str(0))
        self.layout.addWidget(self.label,3,1,1,1)
        self.button = QPushButton("Enter")
        self.button.clicked.connect(self.enter)
        self.layout.addWidget(self.button,4,1,1,1)
        self.setLayout(self.layout)
        self.value = 0



    def enter(self): #this function is connected to the enter funciton
        self.value = self.slider.value()
        if self.remains == None:  #i.e if we are not invading
            self.function(self.country1,self.country2,self.value) 
        else: #if we are invading next.
            self.function(self.country1,self.country2,self.value,self.remains)
        self.close()
        
    def getValue(self):  #called to return the window's value
        return self.value

    def ValueChange(self,value):  #to Change the text displaying the selected amount of troops.
        try:
            self.layout.removeWidget(self.label) #this is only possible if a widget is already created
        except AttributeError:
            pass
        self.label = QLabel(f"{value}")
        self.layout.addWidget(self.label,3,1,1,1)
        self.setLayout(self.layout)


class LeaderBoardWindow(QWidget):  #Window that opens and displays the leaderboard.

    def __init__(self,GameName): #the two parameters required.
        super().__init__()
        self._gameName = GameName
        self.layout = QVBoxLayout()
        self.setWindowTitle("leaderBoard")
        scores = self.findScores()
        for i in scores:  #appending the scores one by one to the layout.
            self.label = QLabel(f"{i[0]} -- Troops : {i[1]}")
            self.layout.addWidget(self.label)
        self.button = QPushButton('Close')
        self.button.clicked.connect(self.closeW)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def closeW(self): #closes the window
        self.close()

    def calculateValue(self,player): #calculates the quantity of troops needed to display for each player.
        worth = DBM.findTotalTroops(self._gameName,player)
        return worth
  
    def findScores(self):# returns a list of all of the player's individual troopcounts.
        details = DBM.loadGame(self._gameName)
        detail = eval(details[2])
        WorthList = []
        for i in detail:

            WorthList.append((i,self.calculateValue(i)))
        return WorthList
    

       
        
        




class GameWindow(game.Game):   #This is the main gamewindow

    def __init__(self,players:list,gameMap:str='Regular',currPlayer:int = 0, phase:int = 0, gameName:str = None,restarted : bool = False,gameMode:str = None):
        super().__init__(players,gameMap,currPlayer,phase,gameName,restarted,gameMode) #inherits from the game class.

        if restarted ==False:  #create a new game if we are not restarting
            DBM.newGame(gameName,self.findinfo('countries'),gameMap,self._players,gameMode)

        self.WINDOW_SIZE = (2000,600)
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1]),pygame.RESIZABLE)
        pygame.display.set_caption("RISK")
        self.screen.fill('White')
        if gameMap == 'Regular':
            self._TextLocations = self.findinfo('text')
        else:
            self._TextLocations = {}
        self._colourDict = self.findinfo('colour') #get a dictionary of country colours mapped ot the country names.
        self._circleLocations = self.findinfo('circles') #find the correct location of the circles
        self._colourList = [(250,0,0),(0,250,0),(0,0,250),(255,250,0),(250,0,255),(0,205,255),(80,205,255),(125,205,40)] #these are the difference colours we can have for the circles.
        self.sliderOn = False # setting the slider to off.



        self._circleColours = {}
        for i in range(len(self._players)):
            self._circleColours.update({self._players[i]:self._colourList[i]})  # set the circle colours for the players.
        self.__loadMap()


    def dotext(self,text:str,locationx:int,locationy:int,size:int = 15,colour = (0,0,0)):   #this function pastes text on the map.     
        font1 = pygame.font.SysFont('freesanbold.ttf', size)
        text1 = font1.render(text, True, (colour))   
        textRect1 = text1.get_rect()
        textRect1.center = int(locationx), int(locationy)
        self.screen.blit(text1, textRect1)
    
    
    def clearSidebar(self): #this function clears the right side of the gamewindow to refresh text.
        self.screen.fill("White",(1200,0,400,600))

    def doNames(self): #print the names of the countries.
        for Country in self._TextLocations:
            locationx, locationy = self._TextLocations[Country]
            self.dotext(Country,locationx,locationy)

    def docircles(self): #paste the circles on the map.
        if self.gameMode == 'Regular':
            for Country in self._circleLocations:
                colour = self._circleColours[DBM.findOccupant(self._gameName,Country)]
                pygame.draw.circle(self.screen, colour,[int(self._circleLocations[Country][0]), int(self._circleLocations[Country][1])], 10, 0)
                self.dotext(str(DBM.findTroops(self._gameName,Country)),self._circleLocations[Country][0], self._circleLocations[Country][1])
        
        else:
            for Country in self._circleLocations:
                pygame.draw.circle(self.screen, (50,50,50), [int(self._circleLocations[Country][0]),int(self._circleLocations[Country][1])], 10, 0)
        
            for Country in self._circleLocations: # if the game is a fog of war game, hide some circles.
                Occupier = DBM.findOccupant(self._gameName,Country)
                if Occupier == self._players[self._CurrPlayer]:
                    colour = self._circleColours[DBM.findOccupant(self._gameName,Country)]
                    pygame.draw.circle(self.screen, colour,[int(self._circleLocations[Country][0]), int(self._circleLocations[Country][1])], 10, 0)
                    self.dotext(str(DBM.findTroops(self._gameName,Country)),self._circleLocations[Country][0], self._circleLocations[Country][1])
                    adj = (self.findinfo('adjacencies',Country))
                    for i in adj:
                            pygame.draw.circle(self.screen, self._circleColours[DBM.findOccupant(self._gameName,i)],[int(self._circleLocations[i][0]), int(self._circleLocations[i][1])], 10, 0)
                            self.dotext(str(DBM.findTroops(self._gameName,i)),self._circleLocations[i][0], self._circleLocations[i][1])

                
    def doPlayers(self): #print the players and their colours on the bottom right of the window.
        for i in range(len(self._players)):
            self.dotext(self._players[i],1280,500 - 50*i,40)
            colour = self._circleColours[self._players[i]]
            pygame.draw.circle(self.screen, colour,[1380,500 - 50*i],20)

    def doPhase(self):
        self.dotext(f'PHASE: {self._Phases[self._CurrPhase]}',1330, 160,30) #this writes new text

    def doTurn(self):
        self.dotext(f'TURN: {self._players[self._CurrPlayer]}',1300, 100,50) #this writes new text




    def __loadMap(self):  #load and paste the map.
        if self._map == 'Regular':
            file = "map.png"
        else:
            file = "HexMap.png"
        try:
            time.sleep(0.5)
            icon = pygame.image.load(file).convert()
            self.screen.blit(icon,(0,0))
            pygame.display.flip()
            pygame.display.set_icon(icon)
        except FileNotFoundError: #incase there is no map.
            pass



    def GuiAttack(self,country1,country2,number): #This is a function that the gameSlider executes when it is the attackphase.
        remains = self.Attack(country1,country2,number)
        if remains != None:
            self.slider = sliderWindow(country1,country2,number,'invade',self.Invade) #Create a new slider to determine the invasion size.
            self.slider.show()


            
    def MainLoop(self):  #the main game loop

        #paste the board data
        self.doNames()
        self.doTurn()
        self.countrySelect = None
        self.doPlayers()
        self.countrySelectList = []

        
        while len(self._players) > 1:  #check if a player has ran out of troops and should be removed from play.
            for i in self._players:
                if DBM.findTotalTroops(self._gameName,i) == 0:
                    self.removePlayer(i)

            #refresh the board data.
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
                    except KeyError:
                        pass


                    if self.countrySelect == 'Surrender':
                        self.removePlayer(self._players[self._CurrPlayer])
                        self.countrySelectList = []
                        self.countrySelect = None
                    
                    elif self.countrySelect == 'Help':
                        self.help = HelpWindow('defualt')
                        self.help.show()
                    
                    elif self.countrySelect == 'LeaderBoard':
                        self.leader = LeaderBoardWindow(self._gameName)
                        self.leader.show()

                    
                    elif self.countrySelect == 'NextPhase':
                        self.countrySelectList = []
                        self.ChangePhase()
                        self.countrySelect = None


                    
                    elif self._Phases[self._CurrPhase] == 'Attack':  #getting initial inputs for the attack phase
                        if len(self.countrySelectList) == 0:
                            if self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]):
                                self.countrySelectList.append(self.countrySelect)


                        elif len(self.countrySelectList) ==1:
                            if not self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]) and self.checkadjacent(self.countrySelectList[0],self.countrySelect):
                                self.countrySelectList.append(self.countrySelect)
                                self.slider = sliderWindow(self.countrySelectList[0],self.countrySelectList[1],DBM.findTroops(self._gameName,self.countrySelectList[0])-1,'attack',self.GuiAttack) #if we have enough inputs create a slider that will execute guiAttack
                                self.slider.show()
                                self.countrySelectList= []
                                
                            
                    elif self._Phases[self._CurrPhase]  == 'Fortification':  #getting initial inputs for the fortification phase.
                        if len(self.countrySelectList) == 0:
                            if self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]):
                                self.countrySelectList.append(self.countrySelect)

                        elif len(self.countrySelectList) == 1:  
                            if self.countrySelect == self.countrySelectList[0]:
                                self.countrySelectList = []
                            elif self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]) and self.depthFirstSearch(self.countrySelect,self.countrySelectList[0]) : 
                                self.countrySelectList.append(self.countrySelect) 
                                self.slider = sliderWindow(self.countrySelectList[0],self.countrySelectList[1],DBM.findTroops(self._gameName,self.countrySelectList[0])-1,'fortify',self.Fortify)  #Create a game slider that will do Fortify.
                                self.slider.show()  
                            else:
                                self.countrySelectList = [] 
                                
                        

                    
                    elif self._Phases[self._CurrPhase]  == 'Deployment' and  self.checkBelongs(self.countrySelect,self._players[self._CurrPlayer]):  #Check that the input is valid for a deploy.
                        self.slider = sliderWindow('your hand',self.countrySelect,self.getPlayerHand(),self._Phases[self._CurrPhase],self.Deploy) #Create a slider to deploy your troops.
                        self.slider.show()
                        self.countrySelectList = []
        self.winner()       






class GameCreate(QWidget):  #this window allows settings to be chosen for a new game and then is responsible for starting that gamewindow.
    def __init__(self,UsernameList:list):

        super().__init__()
        #creating the window's interface
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
        self.lineEdits['Map type'] = QLineEdit()
        self.combobox1 = QComboBox()
        self.combobox1.addItems(['Map Type','Regular','simplified'])
        self.lineEdits['Game mode'] = QLineEdit()
        self.combobox2 = QComboBox()
        self.combobox2.addItems(['Game Mode','Regular','Fog of war'])
        layout.addWidget(self.combobox1)
        layout.addWidget(self.combobox2)



        button = QPushButton("CREATE")
        button.clicked.connect(self.CreateGame) # create a button that will execute the CreateGame function on press.

        layout.addWidget(button,                  2, 3, 1, 1)

        self.pwStatus = QLabel('')
        self.pwStatus.setStyleSheet('font-size: 25px; color: red;')
        layout.addWidget(self.pwStatus, 3, 0, 1, 3)
    


    def CreateGame(self):
        if self.combobox1.currentText() != 'Map Type' and self.combobox2.currentText() != 'Game Mode':
            gameName = self.lineEdits['GameName'].text()
            self.thisGame = GameWindow(self.UsernameList,self.combobox1.currentText(),0,0,gameName,False,self.combobox2.currentText()) #Get the values from the dropdown boxes and text entry box to create a new game with.
            self.thisGame.MainLoop()
            self.close()

class LoadPassNPlayWindow(QWidget):  #This is the window we get from selecting to load a pass 'n play game.
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
        button.clicked.connect(self.reloadTheGame) #connect this button to execute the reloadTheGame function
        layout.addWidget(label)
        layout.addWidget(self.combobox)
        layout.addWidget(button)

    def reloadTheGame(self): #This function reloads the game using the gamename.
        self.close()
        chosenGame = str(self.combobox.currentText())
        details = list(DBM.loadGame(chosenGame))
        self.w = GameWindow(eval(details[2]),details[3],int(details[1]),int(details[0]),chosenGame,True,None)
        self.w.MainLoop()

        
    
        


class PassNPlayWindow(QWidget):  #This window is opened to get users to sign up or sign in before game settings are chose.
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
    
    def back(self): #back to main menu.
        self.close()
        self.w = MainMenu(self.UsernameList[1])
        self.w.show()

    def login(self): #login a player.
        self.close()
        self.w = LoginWindow(self.UsernameList)
        self.w.show()
        

    def start(self): #move on to the game settings selection window.
        self.w = GameCreate(self.UsernameList)
        self.w.show()
        self.close()


    def signup(self): #sign up a new player.
        self.close()
        self.w = SignUpWindow(self.UsernameList)
        self.w.show()
    

class HelpWindow(QWidget):  #this is the help window that can be opened from the main menu and can be opened in game.
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.layout = QVBoxLayout()
        self.label = QLabel('''What is RISK:

RISK is a multiplayer, turn-based strategy game. 
The game of RISK is played on a map that is split up into many territories. 
The objective of RISK is to defeat all opponents and control all territories on the map.\n\nRules of the game:\n\nIn each player’s turn there are three ordered phases: The deployment phase, the attack phase, and the fortification phase.\n\nThe Deployment Phase:\n\nAt the start of the deployment phase troops, dependent on the current influence the player has on the board, will be added to your hand.\nIn this phase you are allowed to deploy troops into your own territories as many or as little times as you would like.\nTroops not used in one deployment phase will be saved to be deployed in the next deployment phase. To end your deployment phase you must select the end phase button.\n\nThe Attack Phase:\n\nDuring your attack phase a player is allowed to attack a territory adjacent to one of their own with troops from their adjacent territory.\nThe player will be prompted for the number of troops they would like to attack the defending territory with.\nWith these troops the winner and troop losses of the battle can be randomly calculated with the probability of winning being biased towards the defence.\nIf the attacker wins the battle, they gain control of the territory, and can, from the remaining troops that were in the battle, select how many troops they would like to move into their new, won, territory.\nA player may attack as many, or as little times as they would like during this phase. To end your Attack phase, you must select the end phase button.\n\nThe Fortification Phase:\n\nDuring your fortification phase you may move troops from one of your countries to another, provided that these countries have a clear path through your own territories to move through.\nYou may only do this once a turn.\n\nHow to select countries:\n\nTo select countries a player must click on their screen on the country of the map that they would like to select.\nThey must select the main body of the country, not the circle on top of it.
''')

        self.layout.addWidget(self.label)
        self.setWindowTitle("Help")
        self.button = QPushButton('Back')
        self.button.clicked.connect(self.goBack)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
    
    def goBack(self):
       self.close()


class StatsWindow(QWidget): #This shows the player's stats
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
        self.layout.addWidget(self.label3)  #This has been added since the testing video. It displays the winrate as a percentage.
        self.setLayout(self.layout)


class MainMenu(QWidget): #This is the main menu.
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


class LoginWindow(QWidget):  #To allow users to log in.

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

        
        

class SignUpWindow(QWidget): #very similar to the login window. Allows users to sign in new accounts.
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

        button = QPushButton("SignUp")
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

    def UseInputs(self): #this is called on the sign up button press.
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()
        Valid = False

        Valid = DBM.SignUp(username,password)
        if Valid == True:  #if the account could be created.
            if len(self.alreadyIn)>0:
                self.alreadyIn.append(username)
                self.w = PassNPlayWindow(self.alreadyIn)
                self.w.show()
            else:
                self.w = MainMenu(username)
                self.w.show()
            self.close()
        if Valid == False: #if the account couldn't be created.
            self.pwStatus.setText('This Username is in use')

    




class SignUpSignIn(QWidget): #This is the very first window, it can create either a login or a sinup window.
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


    def login(self): #Create a login window.
        self.w = LoginWindow()
        self.w.show()
        self.close()
            

    def signup(self): #Create a signup window.
        self.w = SignUpWindow()
        self.w.show()
        self.close()


app = QApplication(sys.argv)
w = SignUpSignIn()
w.show()
app.exec()