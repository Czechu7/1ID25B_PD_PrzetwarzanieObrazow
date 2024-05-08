import os
import sys
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QFileDialog, QHBoxLayout, QLabel, QMainWindow, \
                            QMessageBox, QProgressBar, QPushButton, QScrollArea, QSlider, QVBoxLayout, QWidget

class Page3(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("This is Page 1")

        # Set up layout
        layout = QVBoxLayout()

        # Open Image button
        self.open_image_button = QPushButton("Open Image", self)
        self.open_image_button.clicked.connect(self.open_image)
        layout.addWidget(self.open_image_button)

        # Classify Image button
        self.classify_button = QPushButton("Klasyfikacja", self)
        self.classify_button.clicked.connect(self.perform_classification)
        layout.addWidget(self.classify_button)

        # Label to display the image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 300)  # Set fixed size for the label
        layout.addWidget(self.image_label)

        self.setLayout(layout)

        self.detector_EfficientNetV2 = hub.load("https://tfhub.dev/tensorflow/efficientdet/d2/1")

        # Load label map
        label_map_url = "https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt"
        self.labels_map = {}
        with open(tf.keras.utils.get_file("coco_classes.txt", label_map_url), 'r') as f:
            for line in f:
                if "name:" in line:
                    label_id = int(next(f).split(":")[1])
                    display_name = next(f).split(":")[1].strip().strip("'\"")
                    self.labels_map[label_id] = display_name

        self.image_path = []

    def open_image(self):
        # Use QFileDialog to get the image file path
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png)")
        if file_path:
            # Display the selected image
            self.image_path = file_path
            self.display_image(file_path)

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Scale the image to fit the label

    def perform_classification(self):
        if self.image_path:
            # Load and preprocess image
            image = cv2.imread(self.image_path)
            image_tensor = tf.convert_to_tensor(image)
            image_tensor = tf.image.resize_with_pad(image_tensor, 640, 640)
            image_tensor = tf.cast(image_tensor, tf.uint8)  # Cast to uint8
            image_tensor = tf.expand_dims(image_tensor, axis=0)  # Add batch dimension

            # Perform inference
            detector_output = self.detector_EfficientNetV2(image_tensor)

            # Process detection results
            image_with_boxes = image.copy()
            boxes = detector_output["detection_boxes"][0].numpy()
            classes = detector_output["detection_classes"][0].numpy().astype(int)
            scores = detector_output["detection_scores"][0].numpy()
            total_image_area = image_with_boxes.shape[0] * image_with_boxes.shape[1]

            for i in range(len(scores)):
                class_name = self.labels_map.get(classes[i], 'unknown')
                score = scores[i]
                box = boxes[i]

                # Draw bounding box and label
                y_min = int(box[0] * image_with_boxes.shape[0])
                x_min = int(box[1] * image_with_boxes.shape[1])
                y_max = int(box[2] * image_with_boxes.shape[0])
                x_max = int(box[3] * image_with_boxes.shape[1])

                # Draw bounding box
                cv2.rectangle(image_with_boxes, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # Write label
                cv2.putText(image_with_boxes, f"{class_name}: {score:.2f}", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)