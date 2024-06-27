from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QMessageBox, QLineEdit, QPushButton
import imports

class AddPhotoByIdWindow(QDialog):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dodaj zdjęcie użytkownika")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")
        layout.addWidget(self.username_input)

        self.photoId = QLineEdit()
        self.photoId.setPlaceholderText("Identyfikator zdjęcia")
        layout.addWidget(self.photoId)

        addPhotoByIdBtn = QPushButton("Dodaj zdjęcie")
        addPhotoByIdBtn.clicked.connect(self.addPhotoById)
        layout.addWidget(addPhotoByIdBtn)

        self.setLayout(layout)

    def addPhotoById(self):
        username = self.username_input.text()
        photoId = self.idPhoto.text()
        try:
            res = imports.classifiedImagesService.addPhotoById(username, photoId)
            self.close();
        except Exception as e:
            print('Wystąpił błąd: ' + str(e))
            QMessageBox.warning(self, "Błąd", "Wystąpił błąd podczas dodawnai zdjęcia.")

