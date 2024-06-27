from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QLineEdit, QPushButton
import imports
from models.User import User
import time
import os
from . import  get_all_images_for_user, get_user_image 

class SignInWindow(QDialog):
    userAuth = pyqtSignal(User)
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logowanie")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Zaloguj się")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):
        name = self.username_input.text()
        password = self.password_input.text()
        try:
            res = imports.authService.signIn(name, password)
            print(vars(res))
            print(time.time())
            self.userAuth.emit(res)
            self.close();
            # Download user images after successful login
            image_names = get_all_images_for_user(res.user_id)
            if image_names is not None:
                for image_name in image_names:
                    image_content = get_user_image(res.user_id, image_name)
                    if image_content is not None:
                        with open(os.path.join('/images', image_name), 'wb') as f:
                            f.write(image_content)
        except Exception as e:
            print('Wystąpił błąd: ' + str(e))

