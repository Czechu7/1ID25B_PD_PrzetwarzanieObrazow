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
        self.setGeometry(100, 100, 800, 600)

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
        login_window.exec_()

    def openRegister(self):
        register_window = imports.SignUpWindow()  
        register_window.exec_()

    def onUserLogged(self, user):
        QMessageBox.warning(self, 'Zalogowano', 'zalogowano ' + user.getName())
        window = imports.UserDashboard() # Jeśli użytkownik jest zalogowany, wyświetl okno nawigacji użytkownika
        window.show()
        self.close()
        
    def openRegister(self):
        register_window = imports.SignUpWindow()
        register_window.userAuth.connect(self.onUserLogged)  # Połącz z sygnałem userAuth z okna rejestracji
        register_window.exec_()

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
