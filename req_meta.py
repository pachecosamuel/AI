import requests
import json

# 🔥 CONFIGURAÇÕES — ALTERE AQUI
ACCESS_TOKEN = "EAAbnbzHJLmcBQAgtqeH9ICfNMjlJt4LvldZB46qk1sPyruKnYl8WxqrHGIk2oZBF8wDdBRmlNROfVXMzLpQ6JtRoLHoeqKCxGRECrlEi1MhgIIZCq6O1b7ATCQVwX4J8xdrmk0R5PJtnZBzWTOPce1helo4UPvxWWouGcDl32lTbRXSZCGDEF5YabwAyoLZBYacgtf2OKKi4df"
PHONE_NUMBER_ID = "838537506017077"  # Ex: "838537506017077"
RECIPIENT = "5524992156965"  # Seu número real com DDI
API_VERSION = "v22.0"

# META_TOKEN = "EAAbnbzHJLmcBQAgtqeH9ICfNMjlJt4LvldZB46qk1sPyruKnYl8WxqrHGIk2oZBF8wDdBRmlNROfVXMzLpQ6JtRoLHoeqKCxGRECrlEi1MhgIIZCq6O1b7ATCQVwX4J8xdrmk0R5PJtnZBzWTOPce1helo4UPvxWWouGcDl32lTbRXSZCGDEF5YabwAyoLZBYacgtf2OKKi4df"
# PHONE_NUMBER_ID = 838537506017077
# VERIFY_TOKEN = "meu_token_secreto_123"
# WPP_API_VERSION = "v22.0"

# 🔥 URL
url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

# 🔥 PAYLOAD (igual ao do Postman)
payload = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": RECIPIENT,
    "type": "text",
    "text": {
        "preview_url": False,
        "body": "Mensagem enviada via script Python 🚀"
    }
}

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

print("\n📤 Enviando mensagem...")
response = requests.post(url, headers=headers, json=payload)

print("\n📥 RESPOSTA:")
print("Status Code:", response.status_code)
try:
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except:
    print(response.text)
