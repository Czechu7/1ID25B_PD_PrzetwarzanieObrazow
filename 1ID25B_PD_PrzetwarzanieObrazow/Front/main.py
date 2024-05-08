import imports
from PyQt5.QtWidgets import QApplication
import sys
from imageClassification import ImageClassifier

def main():
    print("Uruchomiono główny moduł.")
    #Poniżej nalezy inicjowac moduly
    app = QApplication(sys.argv)
    window = imports.MainMenu()

    image_classifier = ImageClassifier()
    window.layout.addWidget(image_classifier.main_window)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
