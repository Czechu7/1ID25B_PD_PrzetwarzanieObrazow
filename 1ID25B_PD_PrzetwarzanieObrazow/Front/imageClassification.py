# imageClassification.py
import cv2
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

class CenterNetHourglass:
    def __init__(self):
        # Initialize CenterNet Hourglass model
        pass

    def predict(self, image):
        # Perform inference and return bounding boxes
        boxes = [(100, 100, 200, 200)]  # Dummy boxes for demonstration
        return boxes

class EfficientDet:
    def __init__(self):
        # Initialize EfficientDet model
        pass

    def predict(self, image):
        # Perform inference and return bounding boxes
        boxes = [(300, 300, 400, 400)]  # Dummy boxes for demonstration
        return boxes

class ImageClassifier:
    def __init__(self, parent_window):
        self.centernet = CenterNetHourglass()
        self.efficientdet = EfficientDet()
        self.parent_window = parent_window

        self.app = QApplication([])

    def open_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self.parent_window, "Open Image", "", "Image Files (*.jpg *.jpeg *.png)")
        if file_path:
            self.classify_image(file_path)

    def classify_image(self, image_path):
        image = cv2.imread(image_path)

        centernet_boxes = self.centernet.predict(image)
        efficientdet_boxes = self.efficientdet.predict(image)

        image_with_boxes1 = image.copy()
        self.draw_boxes(image_with_boxes1, centernet_boxes)

        image_with_boxes2 = image.copy()
        self.draw_boxes(image_with_boxes2, efficientdet_boxes)

        result1 = self.convert_cv_image_to_qpixmap(image_with_boxes1)
        result2 = self.convert_cv_image_to_qpixmap(image_with_boxes2)

        self.parent_window.show_result_images(result1, result2)

        self.app.exec_()

    def draw_boxes(self, image, boxes):
        for box in boxes:
            x1, y1, x2, y2 = box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"({x1}, {y1}) - ({x2}, {y2})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def convert_cv_image_to_qpixmap(self, cv_image):
        height, width, channel = cv_image.shape
        bytesPerLine = 3 * width
        q_img = QImage(cv_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        return pixmap
