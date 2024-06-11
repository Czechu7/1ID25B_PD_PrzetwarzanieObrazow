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

class FileUploader(QThread):
    finished = pyqtSignal(int, str)

    def __init__(self, url, file_path, classifiedText, userText, token):
        super(FileUploader, self).__init__()

        self.url = url
        self.file_path = os.path.join(os.getcwd(), file_path)
        self.classifiedText = classifiedText
        self.userText = userText
        self.token = token

    def run(self):
        try:
            headers = {'Authorization': f'Bearer {self.token}'}
            data = {
                'classifiedText': self.classifiedText, 'userText': self.userText
                }
            print(self.file_path)
            with open(self.file_path, 'rb') as file:
                files = {'image': (self.file_path, file)}
                response = requests.post(self.url, files=files, data=data, headers=headers)
                print('Photo sent successfully!')
                self.finished.emit(response.status_code, response.text)
        except Exception as e:
            self.finished.emit(0, str(e))


def sendClassifiedPhoto(fileName, classifiedText, userText):
        userInfo = getLoggedUserInfo()
        token = userInfo['token']
        userId = userInfo['id']
        photoPath = os.path.join("classified", "user", str(userId), fileName)
        
        # DEBUG SECTION-------
        # print(token)
        # print(photoPath)
        # print(classifiedText)
        # print(userText)
        # --------------------

        if photoPath:
            uploader = FileUploader(UPLOAD_URL, photoPath, classifiedText, userText, token)
            uploader.finished.connect(lambda: activeUploaders.remove(uploader)) 
            uploader.start()
            activeUploaders.append(uploader) 

        else:
            QMessageBox.warning(self, "Canceled", "This photo not exist!.")

