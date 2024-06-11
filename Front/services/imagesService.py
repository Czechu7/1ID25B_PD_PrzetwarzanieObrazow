import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout,
                             QWidget, QStackedWidget, QFileDialog, QFrame, QApplication)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import requests
from services.authService import getLoggedUserInfo
import os

active_uploaders = []

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

def choose_and_send_photo():
    file_path, _ = QFileDialog.getOpenFileName(None, "Wybierz zdjęcie", "", "Pliki zdjęć (*.png *.jpg *.jpeg *.bmp)")
    if file_path:
        user_info = getLoggedUserInfo()
        token = user_info['token']
        uploader = FileUploader("http://localhost:8080/images/upload", file_path, token)
        uploader.finished.connect(lambda status_code, response_text: on_upload_finished( status_code, response_text))
        uploader.start()
        active_uploaders.append(uploader)
    else:
        QMessageBox.warning(None, "Anulowano", "Nie wybrano żadnego zdjęcia.")

def on_upload_finished(status_code, response_text):
    if status_code == 201:  # Zmieniono na 201, ponieważ stworzenie zasobu zwraca 201
        QMessageBox.information(None, "Sukces", "Zdjęcie zostało pomyślnie wysłane.\n" + response_text)
    else:
        QMessageBox.warning(None, "Błąd", f"Nie udało się wysłać zdjęcia. Status: {status_code}\n{response_text}")

def get_user_image(user_id, image_name):
    user_info = getLoggedUserInfo()
    token = user_info['token']
    url = f"http://localhost:8080/images/user/{user_id}/image/{image_name}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content  # Zwróć zawartość binarną
    else:
        return None

def get_all_images_for_user(user_id):
    user_info = getLoggedUserInfo()
    token = user_info['token']
    url = f"http://localhost:8080/images/user/{user_id}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Zwróć listę nazw obrazów
    else:
        return None
    
def save_all_images_locally(user_id):
    # Get a list of all image names for the user
    image_names = get_all_images_for_user(user_id)
    if image_names is not None:
        for image_name in image_names:
            image_content = get_user_image(user_id, image_name)
            if image_content is not None:
                user_folder = os.path.join("images", "user", str(user_id))
                os.makedirs(user_folder, exist_ok=True)  

                file_path = os.path.join(user_folder, image_name)
                
                with open(file_path, "wb") as file:
                    file.write(image_content)