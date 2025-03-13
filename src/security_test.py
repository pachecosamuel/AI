import requests

BASE_URL = "http://127.0.0.1:8080"

# Usuário de teste
credentials = {
    "username": "pacheco",
    "password": "pacheco"
}

# 1. Login para obter o token
response = requests.post(f"{BASE_URL}/login", data=credentials)

if response.status_code == 200:
    token = response.json().get("access_token")
    print("Token obtido:", token)

    # 2. Chamar endpoint protegido
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/hello", headers=headers)

    print("Resposta do /hello:", response.json())
else:
    print("Falha no login:", response.json())
