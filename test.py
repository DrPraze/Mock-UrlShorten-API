import requests

BASE = "http://127.0.0.1:5000/"
response = requests.get(BASE+"shortenlink/7/https://google.com")
print(response.json())
