from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QLineEdit, QPushButton
import imports
from models.User import User

class SignUpWindow(QDialog):
    userAuth = pyqtSignal(User)
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rejestracja")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        register_btn = QPushButton("Zarejestruj się")
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def register(self):
        name = self.username_input.text()
        password = self.password_input.text()
        try:
            res = imports.authService.signUp(name, password)
            print(vars(res))
            self.userAuth.emit(res)
            self.close();
        except Exception as e:
            print('Wystąpił błąd: ' + str(e))
            QMessageBox.warning(self, "Błąd", "Wystąpił błąd podczas logowania.")

