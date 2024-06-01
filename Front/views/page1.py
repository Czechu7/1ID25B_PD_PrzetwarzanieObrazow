from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QListWidget, QListView, QListWidgetItem
from PyQt5.QtCore import Qt, QSize
from . import getLoggedUserInfo, get_all_images_for_user,  get_user_image
import imports

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        # Tworzymy ramkę
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)  # Ustawiamy kształt ramki
        frame.setLineWidth(2)  # Ustawiamy szerokość ramki

        # Tworzymy listę
        self.list_widget = QListWidget(self)
        self.list_widget.setViewMode(QListView.IconMode)  # Ustawiamy tryb widoku na IconMode
        self.list_widget.setFlow(QListView.LeftToRight)  # Ustawiamy przepływ od lewej do prawej

        # Ustawiamy szerokość elementów listy na 200x200 pikseli (odwołanie sie do css'a)
        self.list_widget.setStyleSheet("QListWidget::item { width: 200px; height: 200px; }")

        # Dodajemy elementy do listy
        self.list_widget.addItem("zdjecie1")
        self.list_widget.addItem("zdjecie2 ")
        self.list_widget.addItem("zdjecie3")

        # Tworzymy etykietę
        self.welcome_label = QLabel("Moje zdjecia")
        self.welcome_label.setAlignment(Qt.AlignCenter)  # Wycentrowanie tekstu


        # Tworzymy układ dla strony 1
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)  # Dodajemy listę do layoutu
        layout.addWidget(self.welcome_label)
        
        # Dodajemy układ do ramki
        frame.setLayout(layout)

        # Tworzymy układ główny strony 1
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)  # Dodajemy ramkę do układu głównego
        self.setLayout(main_layout)

