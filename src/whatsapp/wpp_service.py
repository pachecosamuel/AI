from utils.config import META_TOKEN, PHONE_NUMBER_ID, VERIFY_TOKEN, WPP_API_VERSION
from whatsapp.wpp_models import NormalizedMessage
from typing import Dict, Any
import logging
import httpx

logger = logging.getLogger(__name__)

class IgnoredEvent(Exception):
    """Usado para indicar que o evento recebido não é uma mensagem de usuário."""
    pass


def parse_webhook_payload(payload: Dict[str, Any]) -> NormalizedMessage:
    """
    Extrai e normaliza o payload recebido do Webhook do WhatsApp para o modelo
    NormalizedMessage.
    Parseia eventos que contenham mídias e textos.
    Ignora eventos de status

    Exemplo de mapeamento:
      - sender_number <- messages[0]["from"]
      - sender_name   <- contacts[0]["profile"]["name"] (se existir)
      - message_text  <- messages[0]["text"]["body"] (se for text)
      - message_id    <- messages[0]["id"]
      - timestamp     <- messages[0]["timestamp"]
    """
    try:
        entry = payload.get("entry", [])
        if not entry:
            raise IgnoredEvent("Payload sem entry message.")

        change = entry[0].get("changes", [])
        if not change:
            raise IgnoredEvent("Payload sem entry message.")

        value = change[0].get("value", {})
        
        # 🟦 Caso 1 — Evento de STATUS → ignorar
        if "statuses" in value and "messages" not in value:
            status = value["statuses"][0].get("status")
            msg_id = value["statuses"][0].get("id")
            logger.info("🔵 Status %s para mensagem %s", status, msg_id)
            raise IgnoredEvent("Evento de status")
        
        # 🟩 Caso 2 — Evento de mensagem recebida
        messages = value.get("messages", [])
        if not messages:
            logger.info("🔵 Evento de status recebido → pass")
            raise IgnoredEvent("Evento de status (sent/delivered/read)")

        msg = messages[0]  

        # Campos principais da mensagem
        sender_number = msg.get("from")
        sender_name = (
            value.get("contacts", [{}])[0]
            .get("profile", {})
            .get("name")
        )


        # Suporte básico: textos e fallback para mídia
        msg_type = msg.get("type")
        
        if msg_type == "text":
            message_text = msg.get("text", {}).get("body", "")
        else:
            caption = msg.get(msg_type, {}).get("caption") or ""
            message_text = caption or f"[{msg_type.upper()} recebida]"


        normalized = NormalizedMessage(
            sender_number=str(sender_number),
            sender_name=sender_name,
            message_text=str(message_text),
            message_id=str(msg.get("id") or ""),
            timestamp=str(msg.get("timestamp") or "")
        )

        logger.info(
            "💬 Mensagem recebida de %s: %s",
            normalized.sender_name or normalized.sender_number,
            normalized.message_text
        )

        return normalized

    except IgnoredEvent as ige:
        raise
    
    except Exception as e:
        logger.exception("Erro ao normalizar payload do WhatsApp: %s", e)
        raise


def log_incoming_message(message: NormalizedMessage) -> None:
    """ Registra uma mensagem recebida no log. """
    sender = message.sender_name or message.sender_number
    logger.info(f"📩 Mensagem recebida de {sender}: {message.message_text}")



def generate_basic_response(message: NormalizedMessage) -> str:
    # Por enquanto só ecoa
    return f"Recebido: {message.message_text}"


async def send_whatsapp_message(to: str, text: str) -> dict:
    """Envia mensagem via WhatsApp Cloud API."""
    url = (
        f"https://graph.facebook.com/{WPP_API_VERSION}/"
        f"{PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {META_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    response.raise_for_status()
    return response.json()
