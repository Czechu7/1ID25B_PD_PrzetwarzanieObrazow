import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout,
                             QWidget, QStackedWidget, QFileDialog)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import requests
import imports
from services.authService import getLoggedUserInfo  

class FileUploader(QThread):
    finished = pyqtSignal(int, str)

    def __init__(self, url, file_path, token):
        super(FileUploader, self).__init__()

        self.url = url
        self.file_path = file_path
        self.token = token

    def run(self):
        try:
            headers = {'Authorization': f'Bearer {self.token}'}
            with open(self.file_path, 'rb') as file:
                files = {'image': (self.file_path, file)}
                response = requests.post(self.url, files=files, headers=headers)
                self.finished.emit(response.status_code, response.text)
        except Exception as e:
            self.finished.emit(0, str(e))

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Główne")
        self.setGeometry(100, 100, 900, 900)

        self.initUI()
        self.active_uploaders = []  


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

        # Tworzymy powitanie
        self.welcome_label = QLabel("Witaj! Zanim zaczniemy, zaloguj się!.", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Ustawiamy layout dla okna
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)

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
        self.button_page1 = QPushButton("Moje zdjęcia")
        self.button_page1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page1))
        layout.addWidget(self.button_page1)
        self.button_page1.hide()

        self.button_page2 = QPushButton("Dodaj zdjęcie")
        self.button_page2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page2))
        self.button_page2.clicked.connect(self.choose_and_send_photo)
        layout.addWidget(self.button_page2)
        self.button_page2.hide()

        self.button_page3 = QPushButton("Opcja 3")
        self.button_page3.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page3))
        layout.addWidget(self.button_page3)
        self.button_page3.hide()

        # Przyciski logowania i rejestracji
        self.login_button = QPushButton("Zaloguj się")
        self.register_button = QPushButton("Zarejestruj się")
        self.login_button.clicked.connect(self.openLogin)
        self.register_button.clicked.connect(self.openRegister)
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
        self.button_page1.show()
        self.button_page2.show()
        self.button_page3.show()
        self.welcome_label.hide()

    def onLogout(self):
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany.")
        imports.authService.logout() 
        self.login_button.show()  # Ukrycie przycisku logowania
        self.register_button.show()  # Ukrycie przycisku rejestracji
        self.stacked_widget.hide()  # Ustawienie przycisku jako niewidocznego
        self.button_page1.hide()
        self.button_page2.hide()
        self.button_page3.hide()
        self.welcome_label.show()

    def choose_and_send_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz zdjęcie", "", "Pliki zdjęć (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            user_info = getLoggedUserInfo()
            token = user_info['token']
            uploader = FileUploader("http://localhost:8080/images/upload", file_path, token)
            uploader.finished.connect(lambda: self.active_uploaders.remove(uploader)) 
            uploader.start()
            self.active_uploaders.append(uploader) 

        else:
            QMessageBox.warning(self, "Anulowano", "Nie wybrano żadnego zdjęcia.")

    def on_upload_finished(self, status_code, response_text):
        if status_code == 200:
            QMessageBox.information(self, "Sukces", "Zdjęcie zostało pomyślnie wysłane.\n" + response_text)
        else:
            QMessageBox.warning(self, "Błąd", f"Nie udało się wysłać zdjęcia. Status: {status_code}\n{response_text}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())
