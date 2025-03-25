from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from datetime import timedelta
from models.token import Token
from models.user import UserInDB

from utils.rate_limiter import rate_limiter, failed_attempts, reset_attempts  
from utils.firebase import create_user
from utils.security import get_password_hash
from utils.auth import authenticate_user, create_access_token
from utils.config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.auth import create_access_token, get_current_active_user, authenticate_user

router = APIRouter(tags=["Register, login and authentication"])
security = HTTPBearer()


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    _=Depends(rate_limiter)
) -> Token:
    """
    Realiza login do usuário e retorna um token de acesso.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", dependencies=[Depends(get_current_active_user)])
async def register_user(user: UserInDB):
    """
    Registra um novo usuário no Firestore.
    """
    try:
        hashed_password = get_password_hash(user.password)
        new_user = create_user(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,  # Senha já hashada
            full_name=user.full_name
        )
        return {"message": "Usuário criado com sucesso!", "user_id": new_user["id"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))