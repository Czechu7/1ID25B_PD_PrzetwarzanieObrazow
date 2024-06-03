import imports
from PyQt5.QtWidgets import QApplication
import sys
import time

def main():
    print("Sprawdzanie czy użytkownik jest zalogowany.")
    isUserLogged = imports.authService.isUserLogged()
    
    if isUserLogged:
        logged_user_info = imports.authService.getLoggedUserInfo()
        user_id = logged_user_info['id']  # Extracting user ID
        print("Zalogowany użytkownik:")
        print(f"Rola: {logged_user_info['role']}")
        print(f"id_uzytkownika: {user_id}")  # Printing user ID
        print(f"Nazwa użytkownika: {logged_user_info['user_name']}")
        print("Token:", logged_user_info['token'])
        print("Czas wygaśnięcia tokena:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(logged_user_info['expiration_time'])))
        imports.imagesService.get_all_images_for_user(user_id)
        print(imports.imagesService.get_all_images_for_user(user_id))
        imports.imagesService.save_all_images_locally(user_id)
        print(imports.imagesService.save_all_images_locally)
    else:
        print("Brak zalogowanego użytkownika.")

    print("Uruchomiono główny moduł.")
    app = QApplication(sys.argv)
    if isUserLogged:
        window = imports.UserDashboard()  # Przekazanie informacji o użytkowniku do MainMenu
    else:
        window = imports.MainMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
