import requests

product_id = 9

endpoint = f"http://localhost:8000/api/products/{product_id}/delete/"
get_response = requests.delete(endpoint)
print(get_response.status_code)

