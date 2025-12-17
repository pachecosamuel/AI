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
from pathlib import Path


from automation.engine import FlowEngine
from automation.state import InMemoryStateManager
from automation.manager import FlowManager
from automation.config import FLOWS_DIR

BASE_DIR = Path(__file__).resolve().parents[1]
FLOWS_DIR = BASE_DIR / "automation" / "flows"

flow_manager = FlowManager(str(FLOWS_DIR))
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
    

    # ─────────────────────────────────────────
    # ZONA 1 — FILTRO DE EVENTOS
    # ─────────────────────────────────────────
    try:
        message = parse_webhook_payload(payload)
    except IgnoredEvent:
        logger.debug("🔕 Evento ignorado (não é mensagem)")
        return {"status": "ignored"}

    # validações simples (ainda zona 1)
    if not message.sender_name:
        return {"status": "ignored"}

    if not message.sender_number:
        logger.warning("⚠ Ignorado: sender_number vazio")
        return {"status": "ignored"}

    # ─────────────────────────────────────────
    # ZONA 2 — PROCESSAMENTO
    # ─────────────────────────────────────────
    logger.info("=== DEBUG ENGINE START ===")
    logger.info(f"Flows encontrados: {flow_manager.list_flows()}")
    logger.info(f"Texto recebido: {message.message_text}")
    logger.info(f"Engine default_flow: {engine.default_flow}")
    logger.info("=== DEBUG ENGINE END ===")

    log_incoming_message(message)
    
    try:
        engine_response = engine.handle_message(
            user_id=message.sender_number,
            text=message.message_text
        )
        reply_text = engine_response["reply"]

    except Exception as e:
        logger.exception("❌ Erro na engine, usando fallback")
        reply_text = generate_basic_response(message)

    await send_whatsapp_message(
        to=message.sender_number,
        text=reply_text
    )

    return {"status": "success"}