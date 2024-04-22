import requests
from models.User import User

API_URL = 'http://localhost:8080/api/v1'

# Rejestracja nowego konta
def signUp(name, password):
    body = {'name': name, 'password': password}
    res = requests.post(API_URL + '/sign-up', json=body)

    if(res.status_code == 201): # 201 Created
        resJson = res.json()
        user = User(resJson['user']['id'], resJson['user']['name'], resJson['user']['role'], resJson['token'])
        return user; #Obiekt użytkownika User
    else:
        raise Exception('Błąd rejestracji!')

# Logowanie
def signIn(name, password):
    body = {'name': name, 'password': password}
    res = requests.post(API_URL + '/sign-in', json=body)
    
    if(res.status_code == 200):
        resJson = res.json()
        user = User(resJson['user']['id'], resJson['user']['name'], resJson['user']['role'], resJson['token'])
        return user; #Obiekt użytkownika User
    else:
        raise Exception('Błąd logowania!')

