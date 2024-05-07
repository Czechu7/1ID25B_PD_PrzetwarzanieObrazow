from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt
import imports as imports

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Główne")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        # Tworzymy akcję dla menu
        action_exit = QAction("Wyjdź", self)
        action_exit.triggered.connect(self.close)
               
        # Tworzymy pasek menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Plik")
        file_menu.addAction(action_exit)

        # Ustawiamy tło
        self.setStyleSheet("MainMenu { background-image: url(bg.png); background-position: center; background-repeat: no-repeat; background-attachment: fixed;}")

        # Tworzymy overlay
        self.overlay = QFrame(self)
        self.overlay.setStyleSheet("background-color: rgba(45, 54, 81, 0.8);")
        self.overlay.setGeometry(0, menubar.height(), self.width(), self.height() - menubar.height())

        layout = QVBoxLayout(self.overlay)

        # Text
        self.label = QLabel("Witaj! Zanim zaczniemy, Zaloguj się!", self)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: white; font-size: 24px; background-color: none ") 
        self.label.setAlignment(Qt.AlignCenter)

        # Tworzymy przyciski oraz style do nich
        self.login_button = QPushButton("Zaloguj się") 
        self.login_button.setStyleSheet('''
            QPushButton {
                color: white;
                font-size: 16px;
                padding: 0.5em 1em;
                border: 2px solid white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        ''')

        self.register_button = QPushButton("Zarejestruj się")  
        self.register_button.setStyleSheet('''
           QPushButton {
                color: white;
                font-size: 16px;
                padding: 0.5em 1em;
                border: 2px solid white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        ''')

        # Actions do przycisków
        self.login_button.clicked.connect(self.openLogin)
        self.register_button.clicked.connect(self.openRegister)

        layout.addWidget(self.label)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

    def openLogin(self):
        login_window = imports.SignInWindow()  # Utwórz nowe okno logowania
        login_window.userAuth.connect(self.onUserLogged)
        login_window.exec_()  # Pokaż nowe okno

    def onUserLogged(self, user):
        QMessageBox.warning(self, 'Zalogowano', 'zalogowano ' + user.getName())
        window = imports.UserDashboard() # Jeśli użytkownik jest zalogowany, wyświetl okno nawigacji użytkownika
        window.show()
        self.close()
        
    def openRegister(self):
        register_window = imports.SignUpWindow()
        register_window.userAuth.connect(self.onUserLogged)  # Połącz z sygnałem userAuth z okna rejestracji
        register_window.exec_()
