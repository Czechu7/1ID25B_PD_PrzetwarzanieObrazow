from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFrame, QListWidget, QListView, QListWidgetItem
from PyQt5.QtCore import Qt, QSize

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
        self.list_widget.addItem("Powodzenia wam z tym kodem")
        self.list_widget.addItem("jak by ktos o cos pytal dlaczego ")
        self.list_widget.addItem("to tak dziala to nie wiem")

        # Tworzymy etykietę
        self.welcome_label = QLabel("This is Page 1")
        self.welcome_label.setAlignment(Qt.AlignCenter)  # Wycentrowanie tekstu

        # Tworzymy przycisk do dodawania zdjęcia
        self.add_photo_button = QPushButton("Add Photo")
        self.add_photo_button.clicked.connect(self.addPhoto)

        # Tworzymy układ dla strony 1
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)  # Dodajemy listę do layoutu
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.add_photo_button)  # Dodajemy przycisk do layoutu
        
        # Dodajemy układ do ramki
        frame.setLayout(layout)

        # Tworzymy układ główny strony 1
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)  # Dodajemy ramkę do układu głównego
        self.setLayout(main_layout)
    
    def addPhoto(self):
        # Zmiana koloru elementu "Item 1"
        item = self.list_widget.item(0)  # Pobieramy wskaźnik do pierwszego elementu (indeks 0)
        if item is not None:
            item.setBackground(Qt.red)  # Ustawiamy tło na czerwone dla pierwszego elementu
