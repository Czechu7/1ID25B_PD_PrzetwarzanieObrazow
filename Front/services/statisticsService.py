import requests
import os
import time
import requests

API_URL = 'http://127.0.0.1:8080/classifiedImages/statistics'
TOKEN_FILE = 'token.txt'

# POBRANIE STATYSTYK
def getStatistics():
    print('Pobieranie statystyk..')
    token = loadFileToken()
    
    headers = {'Authorization': 'Bearer ' + token}
    res = requests.get(API_URL, headers=headers)
    if(res.status_code == 200): # 200 Successful
        return res.json()
    else:
        raise Exception('Błąd pobrania statystyk!')
    

# WCZYTANIE TOKENU Z PLIKU
def loadFileToken():
    tokenPath = os.path.join(os.getcwd(), TOKEN_FILE)
    if os.path.exists(tokenPath):
        with open(tokenPath, 'r') as plik:
            token = plik.read().strip()
        return token
    else:
        return None
