# src\utils\config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_KEY")
PORT = int(os.getenv("PORT", 8080))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Credenciais do usuário administrador
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_FULL_NAME = os.getenv("ADMIN_FULL_NAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_DISABLED = os.getenv("ADMIN_DISABLED") == "true"  # Converte para booleano

