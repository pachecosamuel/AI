import os
import jwt
import datetime
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

# Chave secreta para assinar os tokens (use uma mais segura no ambiente de produção)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

# Segurança HTTP para o FastAPI
security = HTTPBearer()

# Simulação de banco de dados (usuários hardcoded para MVP)
FAKE_USERS_DB = {
    "admin": {"username": "admin", "password": "1234"},  
    "user": {"username": "user", "password": "pass"}
}

def generate_jwt(username: str):
    """Gera um token JWT válido por 1 hora"""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"sub": username, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verifica se o token JWT é válido"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
