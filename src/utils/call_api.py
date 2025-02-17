import requests

url = "https://ai-production-9568.up.railway.app/chat-body"
headers = {"Content-Type": "application/json"}
data = {"prompt": "Explique o conceito de juros compostos"}

response = requests.post(url, json=data, headers=headers)

print(response.json())  # Exibe a resposta da IA
