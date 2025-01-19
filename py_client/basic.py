import requests

endpoint = "http://localhost:8000/api/"
#get_response = requests.get(endpoint, params={"abc":123}, json={"query": "Hello world"})
#get_response = requests.get(endpoint, json={"product_id": 123})
get_response = requests.post(endpoint, json={"title": "title", "content": "Hello world"})
print(get_response.json())
#print(get_response.status_code)
