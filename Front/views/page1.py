from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        self.welcome_label = QLabel("This is Page 1")
        
        # Tworzymy przycisk do zmiany tekstu etykiety
        self.change_text_button = QPushButton("Change Text")
        self.change_text_button.clicked.connect(self.changeText)
        
        # Tworzymy układ dla strony 1
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.change_text_button)
        
        self.setLayout(layout)
    
    def changeText(self):
        # Zmieniamy tekst etykiety
        self.welcome_label.setText("Text changed!")