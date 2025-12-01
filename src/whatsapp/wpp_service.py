from src.utils.config import META_TOKEN, PHONE_NUMBER_ID, VERIFY_TOKEN, WPP_API_VERSION
from src.whatsapp.wpp_models import NormalizedMessage
from typing import Dict, Any
import logging
import httpx

logger = logging.getLogger(__name__)

def parse_webhook_payload(payload: Dict[str, Any]) -> NormalizedMessage:
    """
    Extrai e normaliza o payload recebido do Webhook do WhatsApp para o modelo
    NormalizedMessage.

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
            raise ValueError("Payload inválido: missing entry")

        change = entry[0].get("changes", [])
        if not change:
            raise ValueError("Payload inválido: missing changes")

        value = change[0].get("value", {})
        messages = value.get("messages", [])
        if not messages:
            raise ValueError("Nenhuma mensagem encontrada no payload")

        msg = messages[0]  # foco na primeira mensagem do batch

        # Campos principais da mensagem
        sender_number = msg.get("from")
        sender_name = (
            value.get("contacts", [{}])[0].get("profile", {}).get("name")
            if value.get("contacts")
            else None
        )

        # texto pode não existir (imagem, etc.) → usar empty string como fallback
        message_text = ""
        if msg.get("type") == "text":
            message_text = msg.get("text", {}).get("body", "") or ""
        else:
            # placeholder para outros tipos (p.ex. "image" -> caption)
            # você pode estender aqui para image/video/location etc.
            message_text = msg.get("text", {}).get("body", "") or ""

        message_id = msg.get("id") or ""
        timestamp = msg.get("timestamp") or ""

        normalized = NormalizedMessage(
            sender_number=str(sender_number),
            sender_name=sender_name,
            message_text=str(message_text),
            message_id=str(message_id),
            timestamp=str(timestamp),
        )

        logger.debug("NormalizedMessage criado: %s", normalized.model_dump_json())

        return normalized

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
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    response.raise_for_status()
    return response.json()
