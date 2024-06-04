import os
import json
import imports
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QDialog, QLineEdit, QTextEdit
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

        # # Connect double-click event for showing clasificated window
        # self.list_widget.itemDoubleClicked.connect(self.open_classification_window)

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

        # cREATE BUTTON MOJE KLASYFIKACJE
        self.load_clasyfication_button = QPushButton("Moje klasyfikacje", self)
        self.load_clasyfication_button.clicked.connect(self.load_clasyfication_images)
        buttons_layout.addWidget(self.load_clasyfication_button)  # Add MY clasyfication button to buttons layout

        # Create classification button
        self.classification_button = QPushButton("Klasyfikacja", self)
        self.classification_button.clicked.connect(self.classify_selected_image)  # Connect button to classify_selected_image method
        buttons_layout.addWidget(self.classification_button)  # Add classification button to buttons layout

        # Add buttons layout to the main layout
        layout.addLayout(buttons_layout)

        # Set layout to frame
        frame.setLayout(layout)

        # Create main layout for page 1
        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

        # Load model for classification
        self.detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/d2/1")
        self.labels_map = self.load_label_map()

    def load_clasyfication_images(self):
         # Clear current items in the list widget
        self.list_widget.clear()

        # Get user ID
        user_id = self.get_user_id()
        imports.imagesService.save_all_images_locally(user_id)
        if user_id:
            images_folder = os.path.join("classified", "user", str(user_id))

            # Define supported image extensions
            supported_extensions = ['.jpeg', '.jpg', '.png']

            # Load images from the folder
            if os.path.exists(images_folder):
                print(f"Images folder found: {images_folder}")

                # List all items in the folder for debugging
                folder_contents = os.listdir(images_folder)
                print(f"Contents of the folder: {folder_contents}")

                for image_name in folder_contents:
                    if any(image_name.lower().endswith(ext) for ext in supported_extensions):
                        image_path = os.path.join(images_folder, image_name)
                        print(f"Loading image: {image_path}")
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            image_item = QListWidgetItem(QIcon(pixmap), image_name)
                            self.list_widget.addItem(image_item)
                            print(f"Added image: {image_name}")
                        else:
                            print(f"Failed to load image: {image_path}")
                    else:
                        print(f"Skipped non-image file: {image_name}")
            else:
                print(f"Images folder does not exist: {images_folder}")
        else:
            print("Brak zalogowanego użytkownika.")

    def load_images(self):
        # Clear current items in the list widget
        self.list_widget.clear()

        # Get user ID
        user_id = self.get_user_id()
        imports.imagesService.save_all_images_locally(user_id)
        if user_id:
            images_folder = os.path.join("images", "user", str(user_id))

            # Define supported image extensions
            supported_extensions = ['.jpeg', '.jpg', '.png']

            # Load images from the folder
            if os.path.exists(images_folder):
                print(f"Images folder found: {images_folder}")

                # List all items in the folder for debugging
                folder_contents = os.listdir(images_folder)
                print(f"Contents of the folder: {folder_contents}")

                for image_name in folder_contents:
                    if any(image_name.lower().endswith(ext) for ext in supported_extensions):
                        image_path = os.path.join(images_folder, image_name)
                        print(f"Loading image: {image_path}")
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            image_item = QListWidgetItem(QIcon(pixmap), image_name)
                            self.list_widget.addItem(image_item)
                            print(f"Added image: {image_name}")
                        else:
                            print(f"Failed to load image: {image_path}")
                    else:
                        print(f"Skipped non-image file: {image_name}")
            else:
                print(f"Images folder does not exist: {images_folder}")
        else:
            print("Brak zalogowanego użytkownika.")

# def open_classification_window(self):
#     selected_items = self.list_widget.selectedItems()
#     if not selected_items:
#         QMessageBox.warning(self, "No Selection", "Please select an image to classify.")
#         return

#     user_id = self.get_user_id()
#     if not user_id:
#         print("Brak zalogowanego użytkownika.")
#         return

#     images_folder = os.path.join("classified", "user", str(user_id))
#     image_path = os.path.join(images_folder, 'zdjęcie.jpg')
#     description_path = os.path.join(images_folder, 'opis_zdjecia.txt')
#     comment_path = os.path.join(images_folder, 'komentarz.txt')

#     if os.path.exists(image_path) and os.path.exists(description_path) and os.path.exists(comment_path):
#         dialog = ClassificationDetailsDialog(image_path, description_path, comment_path, self)
#         dialog.exec_()
#     else:
#         QMessageBox.warning(self, "Missing Files", "One or more required files are missing.")


        

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
            images_folder = fr"images\user\{user_id}"
            classified_folder = fr"classified\user\{user_id}"  # Path to classified images folder

            # Create classified folder if it doesn't exist
            os.makedirs(classified_folder, exist_ok=True)

            image_path = os.path.join(images_folder, image_name)
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            classified_image, detection_data = self.perform_classification(img)
            if classified_image is not None:
                classified_image_path = os.path.join(classified_folder, "classifiedimage.jpeg")
                cv2.imwrite(classified_image_path, classified_image)
                
                self.show_classification_results(image_name, classified_image_path, detection_data, classified_folder)
        else:
            print("Brak zalogowanego użytkownika.")

    def perform_classification(self, img):
        try:
            image_tensor = tf.convert_to_tensor(img, dtype=tf.uint8)
            image_tensor = tf.expand_dims(image_tensor, 0)

            detector_output = self.detector(image_tensor)

            image_with_boxes = self.draw_boxes(img, detector_output)
            detection_data = self.extract_detection_data(detector_output)
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
            classified_text_path = os.path.join(classified_folder, "classifiedtext.txt")
            user_text_path = os.path.join(classified_folder, "usertext.txt")

            with open(classified_text_path, 'w') as txt_file:
                txt_file.write(classification_text)

            with open(user_text_path, 'w') as txt_file:
                txt_file.write(user_text)

            QMessageBox.information(self, "Success", "Classification data saved successfully.")
        else:
            print("Brak zalogowanego użytkownika.")

# class ClassificationDetailsDialog(QDialog):
#     def __init__(self, image_path, description_path, comment_path, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Classification Details")
#         self.setFixedSize(1100, 800)  # Set fixed size for the dialog

#         self.layout = QHBoxLayout()

#         self.image_label = QLabel(self)
#         self.layout.addWidget(self.image_label)

#         right_layout = QVBoxLayout()

#         description_label = QLabel("Opis zdjęcia:", self)
#         right_layout.addWidget(description_label)

#         self.description_text = QTextEdit(self)
#         self.description_text.setReadOnly(True)
#         right_layout.addWidget(self.description_text)

#         comment_label = QLabel("Komentarz:", self)
#         right_layout.addWidget(comment_label)

#         self.comment_text = QTextEdit(self)
#         self.comment_text.setReadOnly(True)
#         right_layout.addWidget(self.comment_text)

#         self.layout.addLayout(right_layout)
#         self.setLayout(self.layout)

#         # Load image and text files
#         self.load_image(image_path)
#         self.load_text(description_path, self.description_text)
#         self.load_text(comment_path, self.comment_text)

#     def load_image(self, image_path):
#         pixmap = QPixmap(image_path)
#         if not pixmap.isNull():
#             self.image_label.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))

#     def load_text(self, file_path, text_widget):
#         if os.path.exists(file_path):
#             with open(file_path, 'r') as file:
#                 text = file.read()
#                 text_widget.setPlainText(text)
#         else:
#             text_widget.setPlainText("File not found: " + file_path)

class ClassificationDialog(QDialog):
    def __init__(self, image_name, image_path, detection_data, classified_folder, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Classification Results")
        self.setFixedSize(1100, 800)  # Set fixed size for the dialog

        self.image_path = image_path
        self.classified_folder = classified_folder
        self.image_name = image_name

        self.layout = QHBoxLayout()

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        right_layout = QVBoxLayout()

        json_data_label = QLabel("Classification Data:", self)
        right_layout.addWidget(json_data_label)

        self.json_text = QTextEdit(self)
        classification_text = f"Image Name: {image_name}\n"
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
        save_button.clicked.connect(self.save_data)
        right_layout.addWidget(save_button)

        self.layout.addLayout(right_layout)
        self.setLayout(self.layout)

        # Load image and set maximum size
        self.load_image()

    def load_image(self):
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def save_data(self):
        classification_text = self.json_text.toPlainText()
        user_text = self.notes_field.toPlainText()
        classified_text_path = os.path.join(self.classified_folder, "classifiedtext.txt")
        user_text_path = os.path.join(self.classified_folder, "usertext.txt")

        with open(classified_text_path, 'w') as txt_file:
            txt_file.write(classification_text)

        with open(user_text_path, 'w') as txt_file:
            txt_file.write(user_text)

        QMessageBox.information(self, "Success", "Classification data saved successfully.")
