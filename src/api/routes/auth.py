from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from services.auth_service import authenticate_user, register_user, create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(request: RegisterRequest):
    """Endpoint para registrar um novo usuário."""
    result = register_user(request)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Autenticação e geração de token JWT"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas!")

    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/token")
async def fake_token():
    """Endpoint fake para que o Swagger permita inserir o Bearer Token manualmente"""
    return {"access_token": "fake_token", "token_type": "bearer"}
