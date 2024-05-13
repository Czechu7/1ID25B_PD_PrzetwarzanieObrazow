import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout,
                             QWidget, QStackedWidget, QFileDialog, QFrame, QApplication)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import requests
import imports
from services.authService import getLoggedUserInfo


active_uploaders = []  
def choose_and_send_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Wybierz zdjęcie", "", "Pliki zdjęć (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            user_info = getLoggedUserInfo()
            token = user_info['token']
            uploader = FileUploader("http://localhost:8080/images/upload", file_path, token)
            uploader.finished.connect(lambda: active_uploaders.remove(uploader)) 
            uploader.start()
            active_uploaders.append(uploader) 

        else:
            QMessageBox.warning(self, "Anulowano", "Nie wybrano żadnego zdjęcia.")

def on_upload_finished(self, status_code, response_text):
        if status_code == 200:
            QMessageBox.information(self, "Sukces", "Zdjęcie zostało pomyślnie wysłane.\n" + response_text)
        else:
            QMessageBox.warning(self, "Błąd", f"Nie udało się wysłać zdjęcia. Status: {status_code}\n{response_text}")

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

class imagesService(QThread):
    finished = pyqtSignal(int, str) 
    def __init__(self, url, file_path):
        super().__init__()
        self.url = url
        self.file_path = file_path

    def run(self):
        try:
            with open(self.file_path, 'rb') as file:
                files = {'image': file}
                response = requests.post(self.url, files=files)
                self.finished.emit(response.status_code, response.text)
        except Exception as e:
            self.finished.emit(0, str(e))  


def get_user_images(self):
    user_info = getLoggedUserInfo()
    token = user_info['token']
    user_id = user_info['id']  # assuming 'id' is a key in the user_info dictionary
    url = f"http://localhost:8080/images/{user_id}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content  # return binary content
    else:
        return None