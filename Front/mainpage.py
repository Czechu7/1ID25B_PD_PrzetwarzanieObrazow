import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout,
                             QWidget, QStackedWidget, QFileDialog, QFrame, QApplication)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import requests
import imports
from services.authService import getLoggedUserInfo  

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Główne")
        self.setGeometry(100, 100, 900, 900)

        self.initUI()
        


    def initUI(self):
        # Tworzymy akcję dla menu
        action_exit = QAction("Wyjdź", self)
        action_exit.triggered.connect(self.close)

        # Tworzymy pasek menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Plik")
        Wylogowanie = menubar.addMenu("Wyloguj")
        Wylogowanie.hide() # Ukrywamy element menu "Wyloguj"
        file_menu.addAction(action_exit)
        imports.helloworld.hello_world()

        # Dodajemy akcję do elementu menu "Wyloguj"
        action_logout = QAction("Wyloguj", self)
        action_logout.triggered.connect(self.onLogout)
        Wylogowanie.addAction(action_logout)

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

        # Tworzymy widget i ustawiamy layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Tworzymy widget dla QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.page1 = imports.Page1()
        self.page2 = imports.Page2()
        self.page3 = imports.Page3()
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)
        layout.addWidget(self.stacked_widget)
        self.stacked_widget.hide()

        # Przyciski zarządzania stronami
        self.button_page1 = QPushButton("Strona 1")
        self.button_page1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page1))
        layout.addWidget(self.button_page1)
        self.button_page1.hide()

        self.button_page2 = QPushButton("Strona 2")
        self.button_page2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page2))
        layout.addWidget(self.button_page2)
        self.button_page2.hide()

        self.button_page3 = QPushButton("Strona 3")
        self.button_page3.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page3))
        layout.addWidget(self.button_page3)
        self.button_page3.hide()

        # Przyciski logowania i rejestracji
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
        self.login_button.clicked.connect(self.openLogin)
        self.register_button.clicked.connect(self.openRegister)
        layout.addWidget(self.label)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

    def openLogin(self):
        login_window = imports.SignInWindow() 
        login_window.userAuth.connect(self.onUserLogged)
        login_window.exec_()

    def openRegister(self):
        register_window = imports.SignUpWindow()  
        register_window.exec_()

    def onUserLogged(self, user):
        QMessageBox.information(self, 'Zalogowano', 'Zalogowano ' + user.getName())
        self.login_button.hide()
        self.register_button.hide()
        self.stacked_widget.show()
        window = imports.UserDashboard()
        window.show()
        self.label.hide()
        self.hide()


    def onLogout(self):
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany.")
        imports.authService.logout() 
        self.login_button.show()  # Ukrycie przycisku logowania
        self.register_button.show()  # Ukrycie przycisku rejestracji
        self.stacked_widget.hide()  # Ustawienie przycisku jako niewidocznego

        self.label.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())