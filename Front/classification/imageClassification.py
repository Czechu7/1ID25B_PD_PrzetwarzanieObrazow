import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog

def open_image(self):
    # Use QFileDialog to get the image file path
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png)")
    if file_path:
        # Display the selected image
        self.display_image(file_path)

def display_image(self, file_path):
    pixmap = QPixmap(file_path)
    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True)  # Scale the image to fit the label

def perform_classification(self):
    # Obsługa wyjątków w przypadku braku załadowanych obrazów
    if not self.image_paths:
        QMessageBox.warning(self, "Brak obrazów", "Proszę dodać obrazy przed wykonaniem klasyfikacji.", QMessageBox.Ok)
        return
        

        # Rozpoczęcie klasyfikacji załadowadowanych obrazów
        for index, image_path in enumerate(self.image_paths):
            image_tensor = self.load_img(image_path)

            # Wybór modelu
            if self.model_list_button.currentText() == "EfficientNetV2":
                detector_output = self.detector_EfficientNetV2(image_tensor)
            elif self.model_list_button.currentText() == "CenternetHourglass104_512x512":
                detector_output = self.detector_CenternetHourglass104_512x512(image_tensor)

            image_with_boxes = self.draw_boxes(image_tensor[0].numpy(), detector_output, threshold)
            pixmap = self.convert_np_image_to_pixmap(image_with_boxes)
            pixmap = pixmap.scaledToWidth(self.thumbnail_width, Qt.SmoothTransformation)

            # Automatyczny zapis obrazu z oznaczeniami do pliku (i ewentualna konwersja do) .jpg
            file_path_img, _ = image_path.rsplit('.', 1)
            file_path_img = os.path.join(self.output_dir, 
            os.path.basename(file_path_img) + f"_{self.model_list_button.currentText()}.jpg")
            cv2.imwrite(file_path_img, cv2.cvtColor(image_with_boxes, cv2.COLOR_RGB2BGR))

            # Automatyczny zapis wyników klasyfikacji do pliku .txt
            file_path_txt, _ = image_path.rsplit('.', 1)
            file_path_txt = os.path.join(self.output_dir,
            os.path.basename(file_path_txt) + f"_{self.model_list_button.currentText()}.txt")
            with open(file_path_txt, 'w') as f:
                f.write("Wyniki klasyfikacji:\n")
                boxes = detector_output["detection_boxes"][0].numpy()
                classes = detector_output["detection_classes"][0].numpy().astype(int)
                scores = detector_output["detection_scores"][0].numpy()
                # Obliczenie powierzchni obrazu (szerokość * wysokość)
                total_image_area = image_with_boxes.shape[0] * image_with_boxes.shape[1]

                for i in range(len(scores)):
                    class_name = self.labels_map.get(classes[i], 'unknown')
                    score = scores[i]
                    box = boxes[i]

                    # Określenie koloru prostokąta w zależności od oceny prawdopodobieństwa
                    color = self.get_color_based_on_percentage(score)

                    image_with_boxes = cv2.rectangle(image_with_boxes, 
                    (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), color, 2) 
                    image_with_boxes = cv2.putText(image_with_boxes, 
                    f"{class_name}: Score={score:.2f}", (int(box[1]), int(box[0]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    # Box ma format: y_min, x_min, y_max, x_max, i wartości x, y w zakresie od 0 do 1
                    # Przeskalowanie krawędzi do wartości w pikselach
                    y_min = int(box[0] * image_with_boxes.shape[0])
                    x_min = int(box[1] * image_with_boxes.shape[1])
                    y_max = int(box[2] * image_with_boxes.shape[0])
                    x_max = int(box[3] * image_with_boxes.shape[1])

                    # Obliczenie obszaru wykrytego obiektu
                    detection_box_area = (y_max - y_min) * (x_max - x_min)

                    # Obliczenie proporcji procentowej obszaru obiektu wobec całkowitej powierzchni obrazu
                    percentage_of_total_image = (detection_box_area / total_image_area) * 100.0

                    f.write(f"{class_name}, ocena prawdopodobieństwa = {score * 100:.2f}%, zajmowany obszar obrazu = {percentage_of_total_image:.2f}%\n")