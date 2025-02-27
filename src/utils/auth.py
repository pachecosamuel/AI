# src/utils/auth.py
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from google.cloud import firestore
from passlib.context import CryptContext
from models.token import TokenData
from models.user import UserInDB
from utils.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, FIREBASE_CREDENTIALS

# Inicializa Firestore
db = firestore.Client.from_service_account_json(FIREBASE_CREDENTIALS)

# Configuração de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(identifier: str) -> UserInDB | None:
    """Busca um usuário no Firestore pelo e-mail ou username."""
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", identifier).limit(1).get()
    if not query:
        query = users_ref.where("username", "==", identifier).limit(1).get()
    
    if query:
        user_data = query[0].to_dict()
        return UserInDB(**user_data)
    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha informada corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(identifier: str, password: str) -> UserInDB | None:
    """Autentica um usuário verificando a senha."""
    user = get_user(identifier)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Gera um token JWT para autenticação."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Obtém o usuário a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """Garante que o usuário não está desativado."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
