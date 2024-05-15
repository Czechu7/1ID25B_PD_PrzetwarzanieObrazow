import sys
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMessageBox, QVBoxLayout, QWidget, QPushButton, QFrame, QListWidget, QListView, QListWidgetItem, QSlider

class Page3(QWidget):
    def __init__(self):
        super().__init__()

        # Create frame
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)  # Set frame shape
        frame.setLineWidth(2)  # Set frame width

        # Create list widget
        self.list_widget = QListWidget(self)
        self.list_widget.setViewMode(QListView.IconMode)  # Set view mode to IconMode
        self.list_widget.setFlow(QListView.LeftToRight)  # Set flow to left-to-right

        # Create progress label
        self.progress_label = QLabel("", self)
        self.progress_label.setAlignment(Qt.AlignCenter)  # Center align text

        # "Klasyfikacja" button
        self.classify_button = QPushButton("Klasyfikacja", self)
        self.classify_button.clicked.connect(self.open_image)

        # Threshold slider
        self.threshold_slider = QSlider()
        self.threshold_slider.setOrientation(Qt.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(50)  # Set base value to 50
        self.threshold_slider.valueChanged.connect(self.update_threshold)


        # Create layout for the page
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)  # Add list widget to layout
        layout.addWidget(self.classify_button)
        layout.addWidget(self.threshold_slider)
        layout.addWidget(self.progress_label)
        
        # Set layout to frame
        frame.setLayout(layout)

        # Main layout for the page
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)  # Add frame to main layout
        self.setLayout(main_layout)

        # Load model
        self.detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/d2/1")
        
        # Load label map
        label_map_url = "https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt"
        label_map_path = tf.keras.utils.get_file("coco_classes.txt", label_map_url)

        self.labels_map = {}
        with open(label_map_path, 'r') as f:
            label_id = None
            for line in f:
                if "id:" in line:
                    label_id = int(line.split(":")[1])
                if "display_name:" in line and label_id is not None:
                    display_name = line.split(":")[1].strip().strip("'\"")
                    self.labels_map[label_id] = display_name
                    label_id = None

    def open_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")

        if file_dialog.exec_():
            image_path = file_dialog.selectedFiles()[0]
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.perform_classification(img)

    def perform_classification(self, img):
        self.progress_label.setText("Classification in progress...")
        QApplication.processEvents()

        try:
            image_tensor = tf.convert_to_tensor(img, dtype=tf.uint8)
            image_tensor = tf.expand_dims(image_tensor, 0)

            detector_output = self.detector(image_tensor)

            image_with_boxes = self.draw_boxes(img, detector_output)
            # Resize image to half
            resized_image = cv2.resize(image_with_boxes, (0, 0), fx=0.5, fy=0.5)
            pixmap = self.convert_np_image_to_pixmap(resized_image)
            self.list_widget.clear()
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            item = QListWidgetItem()
            item.setSizeHint(pixmap.size())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, image_label)

        except Exception as e:
            QMessageBox.critical(self, "Classification Error", f"An error occurred during classification: {str(e)}", QMessageBox.Ok)
        finally:
            self.progress_label.setText("Classification completed")

    def draw_boxes(self, image_np, detector_output):
        image_with_boxes = image_np.copy()
        boxes = detector_output["detection_boxes"].numpy()[0]  # Get the first batch element
        class_indices = detector_output["detection_classes"].numpy()[0].astype(int)  # Get the first batch element
        scores = detector_output["detection_scores"].numpy()[0]  # Get the first batch element

        threshold = self.threshold_slider.value() / 100.0

        for i in range(len(boxes)):
            ymin, xmin, ymax, xmax = boxes[i]
            class_index = class_indices[i]
            score = scores[i]

            if score >= threshold:
                left, right, top, bottom = int(xmin * image_with_boxes.shape[1]), int(xmax * image_with_boxes.shape[1]), int(ymin * image_with_boxes.shape[0]), int(ymax * image_with_boxes.shape[0])

                color = self.get_color_based_on_percentage(score)
                cv2.rectangle(image_with_boxes, (left, top), (right, bottom), color, 2)

                label = f"{self.labels_map[class_index]}: {score * 100:.2f}%"
                label_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                label_ymin = max(top, label_size[1] + 10)
                cv2.rectangle(image_with_boxes, (left, label_ymin - label_size[1] - 10), (left + label_size[0], label_ymin + baseline - 10), (255, 255, 255), cv2.FILLED)
                cv2.putText(image_with_boxes, label, (left, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return image_with_boxes

    def get_color_based_on_percentage(self, percentage):
        if percentage < 0.45:
            return (255, 0, 0)  # Red
        elif percentage < 0.55:
            return (255, 165, 0)  # Orange
        elif percentage < 0.65:
            return (255, 255, 0)  # Yellow
        else:
            return (0, 255, 0)  # Green

    def convert_np_image_to_pixmap(self, np_image):
        height, width, channel = np_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(np_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)

    def update_threshold(self):
        if self.list_widget.count() > 0:
            pixmap = self.list_widget.itemWidget(self.list_widget.item(0))
            if pixmap is not None:
                self.perform_classification(self.convert_pixmap_to_np_image(pixmap.pixmap()))

        threshold_value = self.threshold_slider.value()
        self.threshold_label.setText(f"Probability Threshold: {threshold_value}%")


    def convert_pixmap_to_np_image(self, pixmap):
        image = pixmap.toImage()
        width, height = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(height * width * 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
        return arr[:, :, :3]  # Remove the alpha channel if present