import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout,
                             QWidget, QStackedWidget, QFileDialog, QFrame, QApplication)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import os
import requests
import imports
from services.authService import getLoggedUserInfo

UPLOAD_URL = "http://localhost:8080/classifiedImages/upload"


activeUploaders = []
def sendPhoto(self, fileName):
                
        # Pobranie listy wszystkich plików i katalogów w podanym folderze
        folder_path = os.path.join("classified", "user", str(6))
        # all_files = os.listdir(folder_path)

        # # Filtrowanie tylko plików
        # only_files = [f for f in all_files if os.path.isfile(os.path.join(folder_path, f))]

        # # Wyświetlenie listy plików
        # print("Pliki w folderze:")
        # for file in only_files:
        #     print(file)

        print(folder_path)

        userInfo = getLoggedUserInfo()
        token = userInfo['token']
        userId = userInfo['id']
        filePath = os.path.join("classified", "user", str(userId))
        photoPath = os.path.join(filePath, fileName)
        classifiedText = None
        userText = None
        with open(filePath + '/classifiedtext.txt', 'r') as file:
            classifiedText = file.read()
        with open(filePath + '/usertext.txt', 'r') as file:
            userText = file.read()
        print(filePath)
        print(photoPath)
        print(classifiedText)
        print(userText)
        if filePath:
            uploader = FileUploader(UPLOAD_URL, photoPath, classifiedText, userText, token)
            uploader.finished.connect(lambda: activeUploaders.remove(uploader)) 
            uploader.start()
            activeUploaders.append(uploader) 

        else:
            QMessageBox.warning(self, "Canceled", "This photo not exist!.")


# def onUploadFinished(self, status_code, response_text):
#         if status_code == 200:
#             QMessageBox.information(self, "Success", "The photo has been successfully sent.\n" + response_text)
#         else:
#             QMessageBox.warning(self, "Error", f"Failed to send the photo. Status: {status_code}\n{response_text}")


class FileUploader(QThread):
    finished = pyqtSignal(int, str)

    def __init__(self, url, file_path, classifiedText, userText, token):
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
