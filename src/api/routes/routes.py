from fastapi import APIRouter
from models.request import PromptRequest
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from utils.security import decode_access_token

from services.cohere_service import generate_response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
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



