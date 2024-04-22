from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import imports

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Główne")
        self.setGeometry(100, 100, 400, 200)

        self.initUI()

    def initUI(self):
        # Tworzymy akcję dla menu
        action_exit = QAction("Wyjdź", self)
        action_exit.triggered.connect(self.close)

        # Tworzymy pasek menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Plik")
        file_menu.addAction(action_exit)
        imports.helloworld.hello_world()
        # Tworzymy powitanie
        welcome_label = QLabel("Witaj! To jest menu główne.", self)
        welcome_label.setAlignment(Qt.AlignCenter)

        # Ustawiamy layout dla okna
        layout = QVBoxLayout()
        layout.addWidget(welcome_label)

        # Tworzymy widget i ustawiamy layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
