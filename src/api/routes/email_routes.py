from fastapi import APIRouter, HTTPException
from utils.email_service import send_email

router = APIRouter()

@router.post("/send-email/")
def send_email_route(to_email: str, subject: str, body: str):
    result = send_email(to_email, subject, body)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
