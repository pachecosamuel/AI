from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class WppText(BaseModel):
    body: str

class WppMessage(BaseModel):
    from_: str = Field(alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[WppText] = None

    # O WhatsApp usa a chave "from", mas Python não permite atributo "from"
    # Por isso, usamos alias="from"
        # Nova configuração para o Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True,   # permite usar from_ ao construir o model
        extra="ignore"           # evita erro caso o WhatsApp envie campos a mais
    )


class WppContactProfile(BaseModel):
    name: str


class WppContact(BaseModel):
    profile: WppContactProfile
    wa_id: str


class WppValue(BaseModel):
    contacts: List[WppContact]
    messages: List[WppMessage]


class WppChange(BaseModel):
    field: str
    value: WppValue


class WppEntry(BaseModel):
    id: str
    changes: List[WppChange]


class WhatsAppWebhook(BaseModel):
    object: str
    entry: List[WppEntry]
    
    
# ---------------------------
#  Modelo interno normalizado
# ---------------------------

class NormalizedMessage(BaseModel):
    sender_number: str
    sender_name: Optional[str]
    message_text: str
    message_id: str
    timestamp: str