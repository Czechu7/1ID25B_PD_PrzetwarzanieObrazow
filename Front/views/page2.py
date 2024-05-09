from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QListWidget, QListView
from PyQt5.QtCore import Qt
import imports 
from . import choose_and_send_photo


class Page2(QWidget):
    def __init__(self):
        super().__init__()
        
        self.active_uploaders = []  
        # Tworzymy ramkę
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)  # Ustawiamy kształt ramki
        frame.setLineWidth(2)  # Ustawiamy szerokość ramki

        # Tworzymy listę
        self.list_widget = QListWidget(self)
        self.list_widget.setViewMode(QListView.IconMode)  # Ustawiamy tryb widoku na IconMode
        self.list_widget.setFlow(QListView.LeftToRight)  # Ustawiamy przepływ od lewej do prawej

        # Dodajemy elementy do listy
        self.list_widget.addItem("Item 1")
        self.list_widget.addItem("Item 2")
        self.list_widget.addItem("Item 3")
        

        # Tworzymy etykietę
        self.welcome_label = QLabel("This is Page 1")
        self.welcome_label.setAlignment(Qt.AlignCenter)  # Wycentrowanie tekstu

        # Tworzymy przycisk do zmiany tekstu etykiety
        self.change_text_button = QPushButton("Add Photo")
        self.change_text_button.clicked.connect(choose_and_send_photo)
        

        # Tworzymy układ dla strony 1
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)  # Dodajemy listę do layoutu
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.change_text_button)
        
        # Dodajemy układ do ramki
        frame.setLayout(layout)

        # Tworzymy układ główny strony 1
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)  # Dodajemy ramkę do układu głównego
        self.setLayout(main_layout)
    
    def changeText(self):
        # Zmieniamy tekst etykiety
        self.welcome_label.setText("Text changed!")