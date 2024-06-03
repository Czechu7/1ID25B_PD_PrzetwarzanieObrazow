import os
import imports
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class Page1(QWidget):
    def __init__(self):
        super().__init__()

        # Create frame
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(2)

        # Create list widget
        self.list_widget = QListWidget(self)
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(200, 200))  # Set icon size to 200x200 pixels
        self.list_widget.setFlow(QListWidget.LeftToRight)

        # Create layout for page 1
        layout = QVBoxLayout()

        # Add list widget to the main layout
        layout.addWidget(self.list_widget)

        # Create buttons layout
        buttons_layout = QHBoxLayout()

        # Create load images button
        self.load_images_button = QPushButton("Moje zdjęcia", self)
        self.load_images_button.clicked.connect(self.load_images)
        buttons_layout.addWidget(self.load_images_button)  # Add load images button to buttons layout

        # Create classification button
        self.classification_button = QPushButton("Klasyfikacja", self)
        buttons_layout.addWidget(self.classification_button)  # Add classification button to buttons layout

        # Add buttons layout to the main layout
        layout.addLayout(buttons_layout)

        # Set layout to frame
        frame.setLayout(layout)

        # Create main layout for page 1
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def load_images(self):
        # Check if user is logged in
        isUserLogged = imports.authService.isUserLogged()
    
        if isUserLogged:
            # Get logged user info
            logged_user_info = imports.authService.getLoggedUserInfo()
            user_id = logged_user_info['id']  # Extract user ID
        else:
            # If user is not logged in, set user_id to None or any default value as needed
            user_id = None
    
        # Get path to user's images folder
        if user_id:
            images_folder = f"images/user/{user_id}/"
            
            # Clear current items in the list widget
            self.list_widget.clear()

            # Load images from the folder
            if os.path.exists(images_folder):
                for image_name in os.listdir(images_folder):
                    if image_name.endswith('.jpeg'):
                        image_path = os.path.join(images_folder, image_name)
                        image_item = QListWidgetItem(QIcon(QPixmap(image_path)), image_name)
                        image_item.setSizeHint(QSize(300, 300))  # Set size hint for the image item
                        self.list_widget.addItem(image_item)
        else:
            print("Brak zalogowanego użytkownika.")