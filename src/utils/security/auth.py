#src\utils\auth.py
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from models.token import TokenData
from models.user import UserInDB
from utils.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.firebase.firebase import get_user
from utils.security.security import verify_password

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()

def authenticate_user(identifier: str, password: str) -> UserInDB | None:
    """Autentica um usuário verificando a senha."""
    user_data = get_user(identifier)
    
    if not user_data or not verify_password(password, user_data["hashed_password"]):
        return None
    
    # Adiciona o campo 'password' ao instanciar o modelo UserInDB, mas usando hashed_password
    user_data['password'] = user_data.get("hashed_password")  # Adiciona a senha ao campo password
    
    return UserInDB(**user_data)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Gera um token JWT para autenticação."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInDB:
    """Obtém o usuário a partir do token JWT."""

    token = credentials.credentials

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
    
    # 🔥 Adiciona 'password' ao user antes de criar UserInDB
    user['password'] = user.get("hashed_password", "")
    
    return UserInDB(**user)

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    """Garante que o usuário não está desativado."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
