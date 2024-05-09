import requests
from models.User import User
import jwt
import os
import time

API_URL = 'http://localhost:8080/api/v1'
TOKEN_FILE = 'token.txt'

# REJESTRACJA NOWEGO KONTA
def signUp(name, password):
    body = {'name': name, 'password': password}
    res = requests.post(API_URL + '/sign-up', json=body)
    if(res.status_code == 201): # 201 Created
        resJson = res.json()
        tokenDecrypt = jwt.decode(resJson['token'], algorithms="HS256", options={"verify_signature": False})
        user = User(resJson['user']['id'], resJson['user']['name'], resJson['user']['role'], resJson['token'], tokenDecrypt['iat'], tokenDecrypt['exp'])
        with open(TOKEN_FILE, 'w') as plik:
            plik.write(user.token)
        return user; #Obiekt użytkownika User
    else:
        raise Exception('Błąd rejestracji!')


# LOGOWANIE
def signIn(name, password):
    body = {'name': name, 'password': password}
    res = requests.post(API_URL + '/sign-in', json=body)
    if(res.status_code == 200): # 200 Successful
        resJson = res.json()
        token = resJson['token']
        tokenDecrypt = decodeToken(token)
        user = User(resJson['user']['id'], resJson['user']['name'], resJson['user']['role'], resJson['token'], tokenDecrypt['iat'], tokenDecrypt['exp'])     
        with open(TOKEN_FILE, 'w') as plik:
            plik.write(user.token)
        return user; #Obiekt użytkownika User
    else:
        raise Exception('Błąd logowania!')
    
# WERYFIKACJA CZY UZYTKOWNIK JEST ZALOGOWANY
def isUserLogged():
    token = loadFileToken()
    if(token == None): 
        print('Token nie istnieje.')
        return None
    try:
        tokenDecrypt = decodeToken(token)
        if tokenDecrypt['exp'] > time.time():
            return True
        else:
            print('Token wygasł.')
            return False
    except jwt.InvalidTokenError:
        print('Nieprawidłowy token.')
        return False
    
# WYLOGOWANIE
def logout():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print('Wylogowano pomyślnie.')
    else:
        print('Brak zalogowanego użytkownika.')

# POBRANIE INFORMACJI O UŻYTKOWNIKU
def getLoggedUserInfo():
    token = loadFileToken()
    if(token == None): 
        print('Token nie istnieje.')
        return None
    try:
        tokenDecrypt = decodeToken(token)
        user_info = {
            'role': tokenDecrypt.get('scopes'),
            'user_name': tokenDecrypt.get('sub'),
            'iat': tokenDecrypt.get('iat'),
            'token': token,
            'expiration_time': tokenDecrypt.get('exp')
        }
        return user_info
    except jwt.InvalidTokenError:
        print('Nieprawidłowy token.')
        return None
        

# FUNKCJE POMOCNICZE
# WCZYTANIE TOKENU Z PLIKU
def loadFileToken():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as plik:
            token = plik.read().strip()
        return token
    else:
        return None

# DEKODOWANIE TOKENU
def decodeToken(token):
    return jwt.decode(token, algorithms="HS256", options={"verify_signature": False})
