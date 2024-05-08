from PyQt5.QtCore import QThread, pyqtSignal
import requests

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
