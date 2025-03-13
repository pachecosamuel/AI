# src/api/routes/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, APIRouter, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from models.token import Token
from models.request import PromptRequest
from models.user import User, UserInDB
from models.email import EmailRequest

from utils.config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.auth import create_access_token, get_current_active_user, authenticate_user
from utils.firebase import create_user
from utils.security import get_password_hash

from services.cohere_service import generate_response
from services.file_service import save_file
from services.pdf_service import extract_text_from_pdf
from services.email_service import send_email


router = APIRouter()

@router.post("/send-email")
def send_email_endpoint(request: EmailRequest):
    try:
        response = send_email(request.subject, request.body, request.recipients)
        return {"success": True, "message": response["message"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/extract-text/")
async def extract_text(file_path: str):
    """Recebe um caminho de arquivo e retorna o texto extraído (somente PDFs)."""
    text = extract_text_from_pdf(file_path)
    return {"message": "Texto extraído com sucesso!", "text": text}


@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """Recebe um arquivo PDF e o salva no servidor."""
    file_path = save_file(file)
    return {"message": "Arquivo recebido com sucesso!", "file_path": file_path}


@router.post("/register")
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


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
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


@router.post("/chat-body")
async def chat_body(request: PromptRequest):
    """
    Recebe um prompt e retorna a resposta da IA.
    """
    return {"resposta": generate_response(request.prompt, max_tokens=1000)}


@router.post("/chat-parameter")
async def chat_parameter(prompt: str):
    """
    Recebe um prompt como parâmetro e retorna a resposta da IA.
    """
    return {"resposta": generate_response(prompt, max_tokens=100)}
