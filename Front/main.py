import imports
from PyQt5.QtWidgets import QApplication
import sys

def main():
    print("Uruchomiono główny moduł.")
    #Poniżej nalezy inicjowac moduly
    app = QApplication(sys.argv)
    window = imports.MainMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()