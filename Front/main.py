import imports
from PyQt5.QtWidgets import QApplication
import sys
import time

def main():
    print("Sprawdzanie czy użytkownik jest zalogowany.")
    logged_user_info = imports.authService.getLoggedUserInfo()
    if logged_user_info:
        print("Zalogowany użytkownik:")
        print(f"Rola: {logged_user_info['role']}")
        print(f"Nazwa użytkownika: {logged_user_info['user_name']}")
        print("Token:", logged_user_info['token'])
        print("Czas wygaśnięcia tokena:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(logged_user_info['expiration_time'])))
    else:
        print("Brak zalogowanego użytkownika.")


    print("Uruchomiono główny moduł.")
    app = QApplication(sys.argv)
    window = imports.MainMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
