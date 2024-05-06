from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtCore import Qt
import imports
from views.page1 import Page1
from views.page2 import Page2
from views.page3 import Page3

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
        welcome_label = QLabel("Witaj! Zanim zaczniemy, Zaloguj się!.", self)
        welcome_label.setAlignment(Qt.AlignCenter)

        # Ustawiamy layout dla okna
        layout = QVBoxLayout()
        layout.addWidget(welcome_label)

        # Tworzymy widget i ustawiamy layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Tworzymy widget dla QStackedWidget
        self.stacked_widget = QStackedWidget()
        

        # Dodajemy poszczególne strony do QStackedWidget
        self.page1 = Page1()
        self.stacked_widget.addWidget(self.page1)
        

        self.page2 = Page2()
        self.stacked_widget.addWidget(self.page2)

        self.page3 = Page3()
        self.stacked_widget.addWidget(self.page3)

        # Domyślnie pokazujemy pierwszą stronę
        self.stacked_widget.setCurrentWidget(self.page1)

        layout.addWidget(self.stacked_widget)
        self.stacked_widget.hide()  # Ustawienie przycisku jako niewidocznego

 # Tworzymy przyciski dla stron po zalogowaniu
        self.button_page1 = QPushButton("Moje pliki")
        self.button_page1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page1))
        layout.addWidget(self.button_page1)
        self.button_page1.hide()  # Ukrywamy przycisk

        self.button_page2 = QPushButton("Dodaj plik")
        self.button_page2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page2))
        layout.addWidget(self.button_page2)
        self.button_page2.hide()  # Ukrywamy przycisk

        self.button_page3 = QPushButton("Page 3")
        self.button_page3.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page3))
        layout.addWidget(self.button_page3)
        self.button_page3.hide()  # Ukrywamy przycisk
        

        self.login_button = QPushButton("Zaloguj się")  # Przypisanie do atrybutu
        self.register_button = QPushButton("Zarejestruj się")  # Przypisanie do atrybutu
        self.login_button.clicked.connect(self.openLogin)
        self.register_button.clicked.connect(self.openRegister)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)


    def openLogin(self):
        # self.close()  # Zamknij obecne okno
        login_window = imports.SignInWindow()  # Utwórz nowe okno logowania
        login_window.userAuth.connect(self.onUserLogged)
        login_window.exec_()  # Pokaż nowe okno

    def onUserLogged(self, user):
        QMessageBox.warning(self, 'Zalogowano', 'zalogowano ' + user.getName())
        self.login_button.hide()  # Ukrycie przycisku logowania
        self.register_button.hide()  # Ukrycie przycisku rejestracji
        self.stacked_widget.show()  # Ustawienie przycisku jako niewidocznego
        self.button_page1.show()
        self.button_page2.show()
        self.button_page3.show()

    def openRegister(self):
        register_window = imports.SignUpWindow()
        register_window.exec_()

