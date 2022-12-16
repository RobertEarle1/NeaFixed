import pygame
import time
import game
import DBM
from tkinter import *
class GameWindow:

    HEIGHT = 1200
    WIDTH = 650
    WINDOW_SIZE = (HEIGHT,WIDTH)
    SKIP =  "S"     #these will be hotkeys
    QUIT = "Q"
    OPENCHAT = "/"
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1]),pygame.RESIZABLE)
        pygame.display.set_caption("RISK")
        self._TextLocations = {"Alaska":(94,63),"NorthWestTerritory":(190,65),"Alberta":(154,100),"WesternUS":(145,148),"CenteralAmerica":(131,246),"Ontario":(235,108),"Quebec":(317,106),"Greenland":(445,21),"EasternUS":(230,168),"Venezuela":(262,307),"Peru":(214,364),"Brazil":(339,374),"Argentina":(293,489),"NorthAfrica":(534,234),"Congo":(638,340),"EastAfrica":(675,276),"SouthAfrica":(639,418),"Madagascar":(731,430),"Egypt":(637,222),"MiddleEast":(717,198),"India":(846,233),"Siam":(945,274),"Indonesia":(1009,345),"NewGuinea":(1127,365),"WesternAustralia":(1010,455),"China":(965,199),"Afghanistan":(794,135),"Ural":(780,79),"Siberia":(834,41),"Yatusk":(950,59),"Kamchatka":(1077,62),"Ukraine":(689,85),"Irkutsk":(916,107),"NorthernEurope":(597,122),"Scandinavia":(608,61),"Iceland":(493,64),"GreatBritain":(530,118),"Japan":(1094,180),"Mongolia":(959,144),"EasternAustralia":(1128,453),"SouthernEurope":(615,162),"WesternEurope":(532,153),}
        self._colourDict = {'(255, 255, 255, 255)':"Ocean",'(170, 162, 4, 255)':"Alaska",'(113, 113, 55, 255)':"NorthWestTerritory",'(255, 255, 0, 255)':"Alberta",'(80, 80, 39, 255)':"WesternUS",'(255, 255, 128, 255)':"CenteralAmerica",'(148, 148, 73, 255)':"Ontario",'(227, 243, 139, 255)':"Quebec",'(204, 213, 43, 255)':"Greenland",'(128, 128, 0, 255)':"EasternUS",'(255, 128, 128, 255)':"Venezuela",'(128, 0, 0, 255)':"Peru",'(128, 64, 64, 255)':"Brazil", '(255, 0, 0, 255)':"Argentina",'(255, 145, 91, 255)':"NorthAfrica",'(98, 49, 0, 255)':"Congo",'(255, 128, 0, 255)':"EastAfrica",'(74, 37, 0, 255)':"SouthAfrica",'(174, 87, 0, 255)':"Madagascar",'(128, 64, 0, 255)':"Egypt",'(0, 128, 0, 255)':"MiddleEast",'(0, 128, 128, 255)':"India",'(128, 255, 128, 255)':"Siam",'(128, 0, 255, 255)':"Indonesia",'(255, 0, 255, 255)':"NewGuinea",'(128, 0, 64, 255)':"WesternAustralia",'(13, 120, 7, 255)':"China",'(152, 243, 139, 255)':"Afghanistan",'(6, 98, 32, 255)':"Ural",'(87, 208, 47, 255)':"Siberia",'(4, 120, 123, 255)':"Yatusk",'(0, 128, 64, 255)':"Kamchatka",'(0, 0, 128, 255)': "Ukraine",'(21, 206, 35, 255)':"Irkutsk", '(0, 0, 255, 255)':"NorthernEurope", (0, 128, 255, 255):"Scandinavia",'(4, 170, 79, 255)':"Iceland",(255, 255, 255, 255):"GreatBritain",'(128, 255, 0, 255)':"Japan",'(0, 64, 0, 255)':"Mongolia",'(64, 0, 64, 255)':"EasternAustralia",'(50, 191, 252, 255)':"Scandinavia",'(0, 72, 145, 255)':"SouthernEurope",'(0, 128, 255, 255)':"WesternEurope",}
        self._circleLocations = {"Alaska":(85,77),"NorthWestTerritory":(185,79),"Alberta":(153,120),"WesternUS":(133,174),"CenteralAmerica":(139,263),"Ontario":(240,129),"Quebec":(308,123),"Greenland":(444,42),"EasternUS":(222,192),"Venezuela":(258,325),"Peru":(270,417),"Brazil":(339,402),"Argentina":(293,515),"NorthAfrica":(555,277),"Congo":(637,362),"EastAfrica":(685,303),"SouthAfrica":(641,444),"Madagascar":(730,446),"Egypt":(640,237),"MiddleEast":(710,217),"India":(861,251),"Siam":(966,290),"Indonesia":(1008,358),"NewGuinea":(1129,381),"EasternAustralia":(1129,476),"China":(971,221),"Afghanistan":(791,160),"Ural":(796,95),"Siberia":(846,64),"Yatusk":(962,76),"Kamchatka":(1087,78),"Ukraine":(688,110),"Irkutsk":(938,119),"NorthernEurope":(588,133),"Scandinavia":(596,79),"Iceland":(493,75),"GreatBritain":(530,129),"Japan":(1080,194),"Mongolia":(950,159),"WesternAustralia":(1021,477),"SouthernEurope":(626,175),"WesternEurope":(521,166)}
        #Username = game.signedinas()
        self._colourList = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
        self._players = ["Bob","Frank"]  # this will be replaced once networking gets propperly added
        self._circleColours = {}

        for key, value in zip(self._players, self._colourList):
            self._circleColours[key] = value
        self.__loadMap()

        currentPlayer = []


    def dotext(self,text:str,locationx:int,locationy:int):        
        font1 = pygame.font.SysFont('freesanbold.ttf', 15)
        text1 = font1.render(text, True, (0, 0, 0))   
        textRect1 = text1.get_rect()
        textRect1.center = (locationx, locationy)
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
            colour = self._circleColours[DBM.findOccupant(Country)]
            pygame.draw.circle(self.screen, colour,
                   [self._circleLocations[Country][0], self._circleLocations[Country][1]], 10, 0)
            self.dotext(str(DBM.findTroops(Country)),self._circleLocations[Country][0], self._circleLocations[Country][1])
                


    def __loadMap(self):
        try:
            time.sleep(1)
            icon = pygame.image.load("map.png").convert()
            self.screen.blit(icon,(0,0))
            pygame.display.flip()
            pygame.display.set_icon(icon)

        except FileNotFoundError:
            pass
    def inputNumber():
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
                    #print(f"({mouseX},{mouseY})")
                    colourClick = str(self.screen.get_at((mouseX,mouseY)))
                    countryselect = (self._colourDict[colourClick])
                    print(countryselect)
                    if event.type == pygame.QUIT:
                        pygame.quit()         
                    else:
                        getHandleClick = game.HandleClick(countryselect)
                        if type(getHandleClick) == int():
                            self.doSlider(getHandleClick)


                          
    


    #DBM.newGame(None,Players)
    '''game.UserInterface.Deployment(Player)
    game.UserInterface.Attack(Player)
    game.UserInterface.Fortify(Player)
    game.Map.CheckLoss(self._players)
    count+=1'''

class LoginWindow():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE[0], self.WINDOW_SIZE[1]),pygame.RESIZABLE)
        pygame.display.set_caption("LOGIN")


Thisgame = GameWindow()


Thisgame.MainLoop()
