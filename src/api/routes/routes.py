from fastapi import APIRouter
from models.request import PromptRequest
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from utils.security import decode_access_token

from services.cohere_service import generate_response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/chat-body")
async def chat_body(request: PromptRequest):
    """Recebe um prompt e retorna a resposta da IA."""
    return {"resposta": generate_response(request.prompt, max_tokens=1000)}


@router.post("/chat-parameter")
async def chat_parameter(prompt: str):
    """Recebe um prompt como parâmetro e retorna a resposta da IA."""
    return {"resposta": generate_response(prompt, max_tokens=100)}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verifica o token JWT e retorna o usuário"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido!")
    return payload.get("sub")


@router.get("/secure")
async def secure_endpoint(user: str = Depends(get_current_user)):
    """Endpoint protegido - só funciona com JWT válido"""
    return {"message": f"Bem-vindo, {user}! Este endpoint é protegido."}

