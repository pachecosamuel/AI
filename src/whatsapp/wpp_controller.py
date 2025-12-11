from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from utils.config import VERIFY_TOKEN
from whatsapp.wpp_service import(
    parse_webhook_payload,
    log_incoming_message,
    generate_basic_response,
    send_whatsapp_message,
    IgnoredEvent
)
import logging
import json

from automation.engine import FlowEngine
from automation.state import InMemoryStateManager
from automation.manager import FlowManager

flow_manager = FlowManager("src/automation/flows")
state_manager = InMemoryStateManager()
engine = FlowEngine(flow_manager, state_manager, default_flow="welcome_flow")

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Whatsapp"])

@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    
    print("📩 GET recebido:", {
    "hub.mode": hub_mode,
    "hub.challenge": hub_challenge,
    "hub.verify_token": hub_verify_token
    })
    
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)
    
    return PlainTextResponse(content="Invalid verify token", status_code=403)


@router.post("/webhook")
async def receive_webhook(request: Request):
    """Recebe eventos reais enviados pelo WhatsApp Cloud API."""
    
    payload = await request.json()

    logger.debug("📥 Payload recebido (resumido): object=%s ", payload.get("object"))

    try:
        
        message = parse_webhook_payload(payload)
        logger.info(f"✔ Parsed message: {message}")

        if not message.sender_name:
            return {"status": "ignored"}

        if not message.sender_number:
            logger.warning("⚠ Ignorado: sender_number vazio")
            return {"status": "ignored"}

        log_incoming_message(message)

        try:
            # tenta pegar estado e responder via engine
            engine_response = engine.handle_message(user_id=message.sender_number, text=message.message_text)
            reply_text = engine_response["reply"]

            await send_whatsapp_message(to=message.sender_number, text=reply_text)

        except Exception as e:
            # fallback atual
            reply_text = generate_basic_response(message)
            await send_whatsapp_message(to=message.sender_number, text=reply_text)



        return {"status": "success"}

    except Exception as e:
        return JSONResponse(status_code=200, content={"status": "ignored"})
    

# @router.post("/webhook")
# async def receive_webhook(request: Request):
#     """Recebe eventos reais enviados pelo WhatsApp Cloud API."""
    
#     payload = await request.json()

#     logger.debug("📥 Payload recebido (resumido): object=%s ", payload.get("object"))

#     try:
        
#         message = parse_webhook_payload(payload)
#         logger.info(f"✔ Parsed message: {message}")

#         if not message.sender_name:
#             return {"status": "ignored"}

#         if not message.sender_number:
#             logger.warning("⚠ Ignorado: sender_number vazio")
#             return {"status": "ignored"}

#         log_incoming_message(message)

#         ai_response = generate_basic_response(message)
#         logger.info(f"💬 Resposta IA: {ai_response}")

#         send_status = await send_whatsapp_message(
#             to=message.sender_number,
#             text=ai_response
#         )

#         logger.info(f"📤 Resultado envio Meta: {send_status}")

#         return {"status": "success"}

#     except Exception as e:
#         return JSONResponse(status_code=200, content={"status": "ignored"})
    

