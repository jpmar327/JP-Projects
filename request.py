import requests

URL = "https://jsonplaceholder.typicode.com/posts/1"
TOKEN = "your_token_here"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

response = requests.get(URL, headers=headers)

print(f"Status: {response.status_code}")
print(f"Body:   {response.json()}")
