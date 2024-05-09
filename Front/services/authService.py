import requests
from models.User import User
import jwt
import os
import time

API_URL = 'http://localhost:8080/api/v1'

# Rejestracja nowego konta
def signUp(name, password):
    body = {'name': name, 'password': password}
    res = requests.post(API_URL + '/sign-up', json=body)
    if(res.status_code == 201): # 201 Created
        resJson = res.json()
        tokenDecrypt = jwt.decode(resJson['token'], algorithms="HS256", options={"verify_signature": False})
        user = User(resJson['user']['id'], resJson['user']['name'], resJson['user']['role'], resJson['token'], tokenDecrypt['iat'], tokenDecrypt['exp'])
        with open('token.txt', 'w') as plik:
            plik.write(user.token)
        return user; #Obiekt użytkownika User
    else:
        raise Exception('Błąd rejestracji!')


# Logowanie
def signIn(name, password):
    body = {'name': name, 'password': password}
    res = requests.post(API_URL + '/sign-in', json=body)
    if(res.status_code == 200): # 200 Successful
        resJson = res.json()
        tokenDecrypt = jwt.decode(resJson['token'], algorithms="HS256", options={"verify_signature": False})
        user = User(resJson['user']['id'], resJson['user']['name'], resJson['user']['role'], resJson['token'], tokenDecrypt['iat'], tokenDecrypt['exp'])     
        with open('token.txt', 'w') as plik:
            plik.write(user.token)
        return user; #Obiekt użytkownika User
    else:
        raise Exception('Błąd logowania!')

def isUserLogged():
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as plik:
            token = plik.read().strip()
        try:
            tokenDecrypt = jwt.decode(token, algorithms="HS256", options={"verify_signature": False})
            if tokenDecrypt['exp'] > time.time():
                return True
            else:
                print('Token wygasł.')
                return False
        except jwt.InvalidTokenError:
            print('Nieprawidłowy token.')
            return False
    else:
        print('Token nie istnieje.')
        return False
    
def logout():
    if os.path.exists('token.txt'):
        os.remove('token.txt')
        print('Wylogowano pomyślnie.')
    else:
        print('Brak zalogowanego użytkownika.')

def getLoggedUserInfo():
    if os.path.exists('token.txt'):
        with open('token.txt', 'r') as plik:
            token = plik.read().strip()
        try:
            tokenDecrypt = jwt.decode(token, algorithms="HS256", options={"verify_signature": False})
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
    else:
        print('Token nie istnieje.')
        return None



