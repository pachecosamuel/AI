# src/api/routes/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models.token import Token
from models.user import User
from models.request import PromptRequest
from services.cohere_service import generate_response
from utils.config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.security import authenticate_user, create_access_token, get_current_active_user, fake_users_db

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.post("/chat-body")
async def chat_body(request: PromptRequest):
    """Recebe um prompt e retorna a resposta da IA."""
    return {"resposta": generate_response(request.prompt, max_tokens=1000)}

@router.post("/chat-parameter")
async def chat_parameter(prompt: str):
    """Recebe um prompt como parâmetro e retorna a resposta da IA."""
    return {"resposta": generate_response(prompt, max_tokens=100)}
