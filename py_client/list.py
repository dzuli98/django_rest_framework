import requests
from getpass import getpass

auth_endpoint = "http://localhost:8000/api/auth/"
password = getpass()
auth_response = requests.post(auth_endpoint, json={'username': 'cfe', 
                                              'password': password })
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    # headers = {
    #     "Authorization": f"Token {token}"
    # }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    endpoint = "http://localhost:8000/api/products/"
    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())
    # data = get_response.json() #after including pagination
    # next_url = data['next']
    # if next_url is not None:
    #     get_response = requests.get(next_url, headers=headers)

