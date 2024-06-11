import os
import json
import imports
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QDialog, QLineEdit, QTextEdit, QApplication, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap, QResizeEvent
from PyQt5.QtCore import Qt, QSize
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

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

        # Create classified images button
        self.classified_images_button = QPushButton("Moje klasyfikacje", self)
        self.classified_images_button.clicked.connect(self.load_classified_images)
        buttons_layout.addWidget(self.classified_images_button)  # Add classified images button to buttons layout

        # Create classification button
        self.classification_button = QPushButton("Klasyfikacja", self)
        self.classification_button.clicked.connect(self.classify_selected_image)  # Connect button to classify_selected_image method
        buttons_layout.addWidget(self.classification_button)  # Add classification button to buttons layout

        # Add buttons layout to the main layout
        layout.addLayout(buttons_layout)

        # Create progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # Create progress label
        self.progress_label = QLabel("", self)
        self.progress_label.setAlignment(Qt.AlignCenter)  # Center align text

        # Add progress bar and progress label to the main layout
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)

        # Set layout to frame
        frame.setLayout(layout)

        # Create main layout for page 1
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

        # Load model for classification
        self.detector = hub.load("https://www.kaggle.com/models/tensorflow/efficientdet/TensorFlow2/d0/1")
        self.labels_map = self.load_label_map()

        # Double click event for list widget
        self.list_widget.itemDoubleClicked.connect(self.show_classification_dialog)

    def load_images(self):
        # Clear current items in the list widget
        self.list_widget.clear()

        # Get user ID
        user_id = self.get_user_id()
        imports.imagesService.save_all_images_locally(user_id)
        # Get path to user's images folder
        if user_id:
            images_folder = os.path.join("images", "user", str(user_id))
            
            # Load images from the folder
            if os.path.exists(images_folder):
                for image_name in os.listdir(images_folder):
                    if image_name.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp')):
                        image_path = os.path.join(images_folder, image_name)
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            image_item = QListWidgetItem(QIcon(pixmap), image_name)
                            self.list_widget.addItem(image_item)
        else:
            print("Brak zalogowanego użytkownika.")

    def show_classification_dialog(self, item):
        image_name = item.text()
        user_id = self.get_user_id()
        if user_id:
            images_folder = os.path.join("images", "user", str(user_id))
            image_path = os.path.join(images_folder, image_name)
            classified_folder = os.path.join("classified", "user", str(user_id))  # Path to classified images folder
            dialog = ClassificationDialog(image_name, image_path, [], classified_folder, self.get_user_id)
            dialog.load_classification_files()  # No argument needed here
            dialog.exec_()
        else:
            print("Brak zalogowanego użytkownika.")


    def load_classified_images(self):
        # Clear current items in the list widget
        self.list_widget.clear()

        # Get user ID
        user_id = self.get_user_id()

        # Get path to user's classified images folder
        if user_id:
            classified_folder = os.path.join("classified", "user", str(user_id))
            
            # Load images from the folder
            if os.path.exists(classified_folder):
                for image_name in os.listdir(classified_folder):
                    if image_name.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp')):
                        image_path = os.path.join(classified_folder, image_name)
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            image_item = QListWidgetItem(QIcon(pixmap), image_name)
                            self.list_widget.addItem(image_item)
        else:
            print("Brak zalogowanego użytkownika.")

    def classify_selected_image(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an image to classify.")
            return

        selected_item = selected_items[0]
        image_name = selected_item.text()

        # Get user ID
        user_id = self.get_user_id()

        if user_id:
            images_folder = os.path.join("images", "user", str(user_id))
            classified_folder = os.path.join("classified", "user", str(user_id))

            # Create classified folder if it doesn't exist
            os.makedirs(classified_folder, exist_ok=True)

            image_path = os.path.join(images_folder, image_name)
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.progress_label.setText("Classification in progress...")
            self.progress_bar.setValue(0)
            QApplication.processEvents()
            
            classified_image, detection_data = self.perform_classification(img)
            
            if classified_image is not None:
                base_name, ext = os.path.splitext(image_name)
                if not base_name.endswith("_classifiedimage"):
                    base_name += "_classifiedimage"
                classified_image_path = os.path.join(classified_folder, f"{base_name}{ext}")
                cv2.imwrite(classified_image_path, classified_image)
                self.progress_label.setText("Classification completed")
                self.progress_bar.setValue(100)
                self.show_classification_results(base_name, classified_image_path, detection_data, classified_folder)
            else:
                self.progress_label.setText("Classification failed")
                self.progress_bar.setValue(0)
        else:
            print("Brak zalogowanego użytkownika.")

    def perform_classification(self, img):
        try:
            image_tensor = tf.convert_to_tensor(img, dtype=tf.uint8)
            image_tensor = tf.expand_dims(image_tensor, 0)

            detector_output = self.detector(image_tensor)

            image_with_boxes = self.draw_boxes(img, detector_output)
            detection_data = self.extract_detection_data(detector_output)
            
            # Simulate progress update
            self.progress_bar.setValue(50)
            QApplication.processEvents()
            
            return cv2.cvtColor(image_with_boxes, cv2.COLOR_RGB2BGR), detection_data  # Convert back to BGR before returning

        except Exception as e:
            print(f"An error occurred during classification: {str(e)}")
            return None, []

    def draw_boxes(self, image_np, detector_output):
        image_with_boxes = image_np.copy()
        boxes = detector_output["detection_boxes"].numpy()[0]
        class_indices = detector_output["detection_classes"].numpy()[0].astype(int)
        scores = detector_output["detection_scores"].numpy()[0]

        threshold = 0.5  # Threshold value

        for i in range(len(boxes)):
            ymin, xmin, ymax, xmax = boxes[i]
            class_index = class_indices[i]
            score = scores[i]

            if score >= threshold:
                left, right, top, bottom = int(xmin * image_with_boxes.shape[1]), int(xmax * image_with_boxes.shape[1]), int(ymin * image_with_boxes.shape[0]), int(ymax * image_with_boxes.shape[0])

                color = self.get_color_based_on_percentage(score)  # Get color based on score
                cv2.rectangle(image_with_boxes, (left, top), (right, bottom), color, 2)

                label = f"{self.labels_map[class_index]}: {score * 100:.2f}%"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                label_ymin = max(top, label_size[1] + 10)
                cv2.rectangle(image_with_boxes, (left, label_ymin - label_size[1] - 10), (left + label_size[0], label_ymin + 5), (255, 255, 255), cv2.FILLED)
                cv2.putText(image_with_boxes, label, (left, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        return image_with_boxes

    def extract_detection_data(self, detector_output):
        detection_data = []
        boxes = detector_output["detection_boxes"].numpy()[0]
        class_indices = detector_output["detection_classes"].numpy()[0].astype(int)
        scores = detector_output["detection_scores"].numpy()[0]

        threshold = 0.5  # Threshold value

        for i in range(len(boxes)):
            score = scores[i]
            if score >= threshold:
                detection_data.append({
                    "class": self.labels_map[class_indices[i]],
                    "score": score * 100
                })

        return detection_data

    def get_color_based_on_percentage(self, percentage):
        if percentage < 0.45:
            return (0, 0, 255)  # Red for low percentages
        elif percentage < 0.55:
            return (0, 165, 255)  # Orange for medium percentages
        elif percentage < 0.65:
            return (0, 255, 255)  # Yellow for high percentages
        else:
            return (0, 255, 0)  # Green for very high percentages

    def get_user_id(self):
        # Check if user is logged in
        isUserLogged = imports.authService.isUserLogged()
    
        if isUserLogged:
            # Get logged user info
            logged_user_info = imports.authService.getLoggedUserInfo()
            return logged_user_info['id']  # Extract user ID
        else:
            # If user is not logged in, return None or any default value as needed
            return None

    def load_label_map(self):
        label_map_url = "https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt"
        label_map_path = tf.keras.utils.get_file("coco_classes.txt", label_map_url)

        labels_map = {}
        with open(label_map_path, 'r') as f:
            label_id = None
            for line in f:
                if "id:" in line:
                    label_id = int(line.split(":")[1])
                if "display_name:" in line and label_id is not None:
                    display_name = line.split(":")[1].strip().strip("'\"")
                    labels_map[label_id] = display_name
                    label_id = None

        return labels_map

    def show_classification_results(self, image_name, image_path, detection_data, classified_folder):
        dialog = ClassificationDialog(image_name, image_path, detection_data, classified_folder, self)
        dialog.exec_()

    def save_classification_data(self, classified_folder, classification_text, user_text):
        user_id = self.get_user_id()
        
        if user_id:
            classified_text_path = os.path.join(classified_folder, f"{image_name}_classifiedtext.txt")
            user_text_path = os.path.join(classified_folder, f"{image_name}_usertext.txt")

            with open(classified_text_path, 'w') as txt_file:
                txt_file.write(classification_text)

            with open(user_text_path, 'w') as txt_file:
                txt_file.write(user_text)

            QMessageBox.information(self, "Success", "Classification data saved successfully.")
        else:
            print("Brak zalogowanego użytkownika.")

class ClassificationDialog(QDialog):
    def __init__(self, image_name, image_path, detection_data, classified_folder, get_user_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Classification Results")
        self.setFixedSize(1100, 800)

        self.image_name = image_name
        self.image_path = image_path
        self.classified_folder = classified_folder

        self.layout = QHBoxLayout()

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        right_layout = QVBoxLayout()

        json_data_label = QLabel("Classification Data:", self)
        right_layout.addWidget(json_data_label)

        self.json_text = QTextEdit(self)
        classification_text = f""
        for detection in detection_data:
            classification_text += f"{detection['class']}: {detection['score']:.2f}%\n"
        self.json_text.setPlainText(classification_text)
        self.json_text.setReadOnly(True)
        right_layout.addWidget(self.json_text)

        notes_label = QLabel("User Text:", self)
        right_layout.addWidget(notes_label)

        self.notes_field = QTextEdit(self)
        self.notes_field.setFixedHeight(int(0.5 * self.height()))
        right_layout.addWidget(self.notes_field)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(lambda: self.save_data(classified_folder))
        right_layout.addWidget(save_button)

        self.layout.addLayout(right_layout)
        self.setLayout(self.layout)
        self.load_image()
        self.edit_mode_enabled = False
        self.get_user_id = get_user_id

    def load_image(self):
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def load_classification_files(self):
        user_id = self.get_user_id()  # Call get_user_id method
        if user_id:
            classified_folder = os.path.join("classified", "user", str(user_id))

            base_name, ext = os.path.splitext(self.image_name)

            # Load usertext.txt
            user_text_path = os.path.join(classified_folder, f"{base_name}_usertext.txt")
            if os.path.exists(user_text_path):
                with open(user_text_path, 'r') as user_text_file:
                    user_text = user_text_file.read()
                self.notes_field.setPlainText(user_text)

            # Load classifiedtext.txt
            classified_text_path = os.path.join(classified_folder, f"{base_name}_classifiedtext.txt")
            if os.path.exists(classified_text_path):
                with open(classified_text_path, 'r') as classified_text_file:
                    classified_text = classified_text_file.read()
                classification_text = f"{classified_text}"
                self.json_text.setPlainText(classification_text)

            # Load classifiedimage.jpeg
            classified_image_path = os.path.join(classified_folder, f"{base_name}_classifiedimage.jpeg")
            if os.path.exists(classified_image_path):
                pixmap = QPixmap(classified_image_path)
                if not pixmap.isNull():
                    self.image_label.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def save_data(self, classified_folder):
        classification_text = self.json_text.toPlainText()
        user_text = self.notes_field.toPlainText()
        
        base_name, ext = os.path.splitext(self.image_name)

        classified_text_path = os.path.join(classified_folder, f"{base_name}_classifiedtext.txt")
        user_text_path = os.path.join(classified_folder, f"{base_name}_usertext.txt")

        with open(classified_text_path, 'w') as txt_file:
            txt_file.write(classification_text)

        with open(user_text_path, 'w') as txt_file:
            txt_file.write(user_text)

        QMessageBox.information(self, "Success", "Classification data saved successfully.")