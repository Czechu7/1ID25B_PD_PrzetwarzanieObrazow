#Do externalModules wszystkie importy z pipa

#Ponizej import modulow
import helloworld

from services import authService

from mainpage import MainMenu
from views.signInWindow import SignInWindow
from views.signUpWindow import SignUpWindow
from views.addPhotoByIdWindow import AddPhotoByIdWindow
from views.page1 import Page1
from views.page2 import Page2
from views.page3 import Page3
from views.userDashboard import UserDashboard
from main import main
from services.imagesService import choose_and_send_photo
from services import imagesService
from services.classifiedImagesService import sendClassifiedPhoto
from services import classifiedImagesService
