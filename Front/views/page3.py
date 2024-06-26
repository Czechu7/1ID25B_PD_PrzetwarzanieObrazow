import sys
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMessageBox, QVBoxLayout, QWidget, QPushButton, QFrame, QListWidget, QListView, QListWidgetItem, QSlider
import imports

class Page3(QWidget):
    def __init__(self):
        super().__init__()

        # Create frame
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)  # Set frame shape
        frame.setLineWidth(2)  # Set frame width

# Create list widget
        self.list_widget = QListWidget(self)
        self.list_widget.setViewMode(QListView.ListMode)  # Set view mode to ListMode
        self.list_widget.setFlow(QListView.TopToBottom)  # Set flow to top-to-bottom

        # Load and display statistics
        self.load_statistics()

        # Create layout for the page
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)  # Add list widget to layout
        
        # Set layout to frame
        frame.setLayout(layout)

        # Main layout for the page
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)  # Add frame to main layout
        self.setLayout(main_layout)


    def load_statistics(self):
        statistics = imports.getStatistics()
        for key, value in statistics.items():
            item = QListWidgetItem(f"{key}: {value}")
            self.list_widget.addItem(item)

