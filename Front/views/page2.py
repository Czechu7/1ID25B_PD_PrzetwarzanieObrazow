from PyQt5.QtWidgets import QWidget, QLabel

class Page2(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("This is Page 1")