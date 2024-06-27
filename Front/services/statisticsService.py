import requests
from services.authService import getLoggedUserInfo

API_URL = 'http://127.0.0.1:8080/classifiedImages/statistics'

# POBRANIE STATYSTYK
def getStatistics():
    print('Pobieranie statystyk..')
    if(getLoggedUserInfo() == None):
        return {}
    
    userInfo = getLoggedUserInfo()

    if(userInfo):    
        token = userInfo['token']
        headers = {'Authorization': 'Bearer ' + token}
        res = requests.get(API_URL, headers=headers)
        if(res.status_code == 200):
            if(res.json() == []):
                print('Brak statystyk')
                return {}
            else:
                print(res.json())
                return res.json()
        else:
            raise Exception('Błąd pobrania statystyk!')
    else:
        return {}
    
