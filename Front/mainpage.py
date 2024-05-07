from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import imports as imports

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
        file_menu.addAction(action_exit)
        
        # Tworzymy powitanie
        self.welcome_label = QLabel("Witaj! Zanim zaczniemy, Zaloguj się!.", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Ustawiamy layout dla okna
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)

        # Tworzymy widget i ustawiamy layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.login_button = QPushButton("Zaloguj się")  # Przypisanie do atrybutu
        self.register_button = QPushButton("Zarejestruj się")  # Przypisanie do atrybutu
        self.login_button.clicked.connect(self.openLogin)
        self.register_button.clicked.connect(self.openRegister)
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
        register_window.exec_()
