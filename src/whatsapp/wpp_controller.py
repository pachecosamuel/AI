@router.post("/webhook")
async def whatsapp_webhook(request: dict):
    entry = await parse_incoming_payload(request)
    resposta = await ai_service(entry)
    await send_text_message(entry.from_number, resposta)
