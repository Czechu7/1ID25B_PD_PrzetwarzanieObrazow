import requests
import os
import time
import requests

API_URL = 'http://127.0.0.1:8080/classifiedImages/statistics'
TOKEN_FILE = 'token.txt'

def get_statistics(user_id):
    print('Pobieranie statystyk dla użytkownika o ID:', user_id)
    token = load_token_from_file()
    
    if token:    
        headers = {'Authorization': 'Bearer ' + token}
        # Update the URL to include the userId in the path
        user_statistics_url = f"{API_URL.rsplit('/', 1)[0]}/user/{user_id}/statistics"
        response = requests.get(user_statistics_url, headers=headers)
        
        if response.status_code == 200:  # 200 Successful
            return response.json()
        else:
            raise Exception('Błąd pobrania statystyk!')
    else:
        return {}
def load_token_from_file():
    token_path = os.path.join(os.getcwd(), TOKEN_FILE)
    
    if os.path.exists(token_path):
        with open(token_path, 'r') as file:
            token = file.read().strip()
        return token
    else:
        return None