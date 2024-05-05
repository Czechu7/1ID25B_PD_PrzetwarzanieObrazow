from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import imports

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Główne")
        self.setGeometry(100, 100, 400, 200)

        self.initUI()

    def initUI(self):
        # Tworzymy akcję dla menu
        action_exit = QAction("Wyjdź", self)
        action_exit.triggered.connect(self.close)

        # Tworzymy pasek menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Plik")
        file_menu.addAction(action_exit)
        imports.helloworld.hello_world()
        # Tworzymy powitanie
        welcome_label = QLabel("Witaj! To jest menu główne.", self)
        welcome_label.setAlignment(Qt.AlignCenter)

        # Ustawiamy layout dla okna
        layout = QVBoxLayout()
        layout.addWidget(welcome_label)

        login_button = QPushButton("Zaloguj się")
        register_button = QPushButton("Zarejestruj się")
        login_button.clicked.connect(self.openLogin)
        register_button.clicked.connect(self.openRegister)
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        # login_button.clicked.connect()

        # Tworzymy widget i ustawiamy layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def openLogin(self):
        # self.close()  # Zamknij obecne okno
        login_window = imports.SignInWindow()  # Utwórz nowe okno logowania
        login_window.userAuth.connect(self.onUserLogged)
        login_window.exec_()  # Pokaż nowe okno

    def onUserLogged(self, user):
        QMessageBox.warning(self, 'Zalogowano', 'zalogowano ' + user.getName())

    def openRegister(self):
        register_window = imports.SignUpWindow()
        register_window.exec_()