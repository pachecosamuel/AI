from utils.security import hash_password, verify_password, create_access_token
from models.user import User
from datetime import timedelta

# Simulação de um "banco de dados" temporário
FAKE_DB = {}

def register_user(request):
    """Registra novo usuário"""
    if request.username in FAKE_DB:
        return {"error": "Usuário já existe!"}

    FAKE_DB[request.username] = {
        "username": request.username,
        "email": request.email,
        "password": hash_password(request.password)
    }
    return {"message": "Usuário registrado com sucesso!"}

def authenticate_user(username: str, password: str):
    """Valida credenciais do usuário e retorna os dados do usuário autenticado."""
    user = FAKE_DB.get(username)
    if not user or not verify_password(password, user["password"]):
        return None

    return user  # <-- Agora retorna o usuário inteiro (um dicionário).
