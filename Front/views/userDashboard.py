from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtCore import Qt
import imports as imports
import time
from views.page1 import Page1
from views.page2 import Page2
from views.page3 import Page3

class UserDashboard(QMainWindow):
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
        Wylogowanie.hide()  # Ukrywamy element menu "Wyloguj"
        file_menu.addAction(action_exit)

        # Dodajemy akcję do elementu menu "Wyloguj"
        action_logout = QAction("Wyloguj", self)
        action_logout.triggered.connect(self.onLogout)
        Wylogowanie.addAction(action_logout)

        # Tworzymy label na powitanie użytkownika
        self.welcome_label = QLabel(self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        
        isUserLogged = imports.authService.isUserLogged()
        if isUserLogged:
            logged_user_info = imports.authService.getLoggedUserInfo()
            role = logged_user_info['role']
            user_name = logged_user_info['user_name']
            token = logged_user_info['token']
            expiration_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(logged_user_info['expiration_time']))
            user_info_text = f"Zalogowany użytkownik:\nRola: {role}\nNazwa użytkownika: {user_name}\nToken: {token}\nCzas wygaśnięcia tokena: {expiration_time}"
            self.welcome_label.setText(user_info_text)
        else:
            self.welcome_label.setText("Brak zalogowanego użytkownika.")

        # Ustawiamy layout dla okna
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)

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

        # Tworzymy przyciski dla stron po zalogowaniu
        self.button_page1 = QPushButton("Zdjecia")
        self.button_page1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page1))
        layout.addWidget(self.button_page1)

        self.button_page2 = QPushButton("Dodaj zdjecie")
        self.button_page2.clicked.connect(imports.imagesService.choose_and_send_photo)
        layout.addWidget(self.button_page2)

        self.button_page3 = QPushButton("Strona 3")
        self.button_page3.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page3))
        layout.addWidget(self.button_page3)
        
    def onLogout(self):
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany.")
        imports.authService.logout()
        self.close()
        # Pokazanie okna imports.mainMenu
        # Uruchomienie pliku main.py
        import subprocess
        subprocess.Popen(["python", "main.py"])
