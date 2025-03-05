import os
import json
from dotenv import load_dotenv

load_dotenv(verbose=True)

print("PRIVATE KEY (direto do os.getenv):", repr(os.getenv("FIREBASE_PRIVATE_KEY")))

# Teste para ver se a variável foi carregada
print(repr(os.getenv("FIREBASE_PRIVATE_KEY")))

API_KEY = os.getenv("COHERE_KEY")
PORT = int(os.getenv("PORT", 8080))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Credenciais do usuário administrador
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_FULL_NAME = os.getenv("ADMIN_FULL_NAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_DISABLED = os.getenv("ADMIN_DISABLED", "false").lower() == "true"


# Reconstruindo as credenciais do Firebase a partir das variáveis de ambiente
FIREBASE_CREDENTIALS = {
    "type": os.getenv("FIREBASE_TYPE", ""),
    "project_id": os.getenv("FIREBASE_PROJECT_ID", ""),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID", ""),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", ""),  # Corrige quebras de linha
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL", ""),
    "client_id": os.getenv("FIREBASE_CLIENT_ID", ""),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI", ""),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI", ""),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL", ""),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL", ""),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN", "")
}

print("PRIVATE KEY:", repr(os.getenv("FIREBASE_PRIVATE_KEY")))
print("PROJECT ID:", repr(os.getenv("FIREBASE_PROJECT_ID")))


print("FIREBASE_CREDENTIALS carregadas:")
for key, value in FIREBASE_CREDENTIALS.items():
    print(f"{key}: {'OK' if value else 'MISSING'}")

# Verificando se os dados essenciais foram carregados corretamente
if not FIREBASE_CREDENTIALS["private_key"] or not FIREBASE_CREDENTIALS["client_email"]:
    raise ValueError("Credenciais do Firebase estão incompletas. Verifique suas variáveis de ambiente.")

# Certificando que as credenciais foram carregadas corretamente
# if not FIREBASE_CREDENTIALS.get("private_key") or not FIREBASE_CREDENTIALS.get("client_email"):
#     raise ValueError("Credenciais do Firebase estão incompletas. Verifique suas variáveis de ambiente.")

print("Firebase Credentials carregadas com sucesso!")  # Debug opcional

# if FIREBASE_CREDENTIALS:
#     try:
#         FIREBASE_CREDENTIALS = json.loads(FIREBASE_CREDENTIALS)
#     except json.JSONDecodeError:
#         raise ValueError("Erro ao carregar as credenciais do Firebase. Verifique o formato JSON.")
# else:
#     raise ValueError("FIREBASE_CREDENTIALS não está definida. Configure corretamente no ambiente.")



