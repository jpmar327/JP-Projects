import requests

URL = "https://your-api.com/graphql"
TOKEN = "your_token_here"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

query = """
query {
    yourQuery {
        field1
        field2
    }
}
"""

variables = {
    "exampleVar": "value"
}

payload = {
    "query": query,
    "variables": variables,
}

response = requests.post(URL, json=payload, headers=headers)

print(f"Status: {response.status_code}")
print(f"Body:   {response.json()}")
