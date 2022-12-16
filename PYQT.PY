import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy, QVBoxLayout,QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import DBM



class JoinGame(QWidget):
    def __init__(self,Username):
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

        joingamebutton = QPushButton("Join")
        joingamebutton.clicked.connect(self.joingame)
        layout.addWidget(joingamebutton)

        hostgamebutton = QPushButton("Host")
        hostgamebutton.clicked.connect(self.creategame)
        layout.addWidget(hostgamebutton)


        settings = QPushButton("Settings")
        settings.clicked.connect(self.dosettings)
        layout.addWidget(settings)


        help = QPushButton("Help")
        help.clicked.connect(self.dohelp)
        layout.addWidget(help)



    def joingame(self):
        self.w = JoinGame(self.Username)
        self.w.show()
        self.close()
    def creategame():
        pass
    def dosettings():
        pass
    def dohelp():
        pass


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RISK LOGIN')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)

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
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()
        Valid = DBM.SignIn(username,password)
        if Valid == True:
            self.close()
            self.w = MainMenu(username)
            self.w.show()

        elif Valid == False:
            self.pwStatus.setText('Incorrect credentials')
        else:
            raise ValueError
    

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RISK SIGNUP')
        self.setWindowIcon(QIcon(''))
        self.window_width, self.window_height = 600, 200
        self.setFixedSize(self.window_width, self.window_height)

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
        Valid = DBM.SignUp(username,password)
        if Valid == True:
            self.close()
            self.w = MainMenu(username)
            self.w.show()
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
        self.classOptions = {SignUpSignIn:{LoginWindow,SignUpWindow},LoginWindow:{MainMenu,SignUpSignIn},SignUpWindow:{MainMenu,SignUpSignIn}}
        self.window = SignUpSignIn()







app = QApplication(sys.argv)
w = SignUpSignIn()
w.show()
app.exec()