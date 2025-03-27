from fastapi import APIRouter, Depends, HTTPException, status, APIRouter, UploadFile, File
from fastapi.security import HTTPBearer

from models.request import PromptRequest
from models.email import EmailRequest

from utils.auth import get_current_active_user
from services.cohere_service import generate_response
from services.file_service import save_file
from services.pdf_service import extract_text_from_pdf
from services.email_service import send_email


router = APIRouter(tags=["Services"])
security = HTTPBearer()

@router.get("/hello_world", dependencies=[Depends(get_current_active_user)], tags=["Test"])
def say_hello():
    try:
        print("Oi, mundo!")
        return {"success": True, "message": "sucess"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/extract-text/", dependencies=[Depends(get_current_active_user)])
async def extract_text(file_path: str):
    """Recebe um caminho de arquivo e retorna o texto extraído (somente PDFs)."""
    text = extract_text_from_pdf(file_path)
    return {"message": "Texto extraído com sucesso!", "text": text}


@router.post("/upload-file/", dependencies=[Depends(get_current_active_user)])
async def upload_file(file: UploadFile = File(...)):
    """Recebe um arquivo PDF e o salva no servidor."""
    file_path = save_file(file)
    return {"message": "Arquivo recebido com sucesso!", "file_path": file_path}


@router.post("/send-email", dependencies=[Depends(get_current_active_user)])
def send_email_endpoint(request: EmailRequest):
    try:
        response = send_email(request.subject, request.body, request.recipients)
        return {"success": True, "message": response["message"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat-body", dependencies=[Depends(get_current_active_user)])
async def chat_body(request: PromptRequest):
    """
    Recebe um prompt e retorna a resposta da IA.
    """
    return {"resposta": generate_response(request.prompt, max_tokens=1000)}


@router.post("/chat-parameter", dependencies=[Depends(get_current_active_user)])
async def chat_parameter(prompt: str):
    """
    Recebe um prompt como parâmetro e retorna a resposta da IA.
    """
    return {"resposta": generate_response(prompt, max_tokens=100)}