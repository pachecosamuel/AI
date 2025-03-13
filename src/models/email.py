# Modelo de entrada
from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    recipients: list[EmailStr]  # Lista de e-mails válidos
    subject: str
    body: str