import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QLabel, QPushButton, QMessageBox, QVBoxLayout,
                             QWidget, QStackedWidget, QFileDialog, QFrame, QApplication)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import requests
import imports
from services.authService import getLoggedUserInfo

UPLOAD_URL = "http://localhost:8080/classifiedImages/upload"
PHOTOS_LOCATION = "/classified/user/"

activeUploaders = []
def sendPhoto(self, fileName):
        userInfo = getLoggedUserInfo()
        token = userInfo['token']
        userId = userInfo['id']
        filePath = PHOTOS_LOCATION + userId + '/' + fileName
        
        if filePath:
            uploader = FileUploader(UPLOAD_URL, filePath, token)
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