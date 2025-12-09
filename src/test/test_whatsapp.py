# src/tests/test_wpp_service.py

import pytest
import httpx
import respx
from fastapi import FastAPI
from unittest.mock import patch, AsyncMock
from fastapi.responses import PlainTextResponse
from src.whatsapp.wpp_models import NormalizedMessage

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from unittest.mock import patch, AsyncMock

from src.utils.config import META_TOKEN, PHONE_NUMBER_ID, WPP_API_VERSION, VERIFY_TOKEN

from src.whatsapp.wpp_service import (
    parse_webhook_payload, 
    generate_basic_response,
    send_whatsapp_message,
    log_incoming_message
)

# Importa o router real
from src.whatsapp.wpp_controller import router
from src.utils.config import VERIFY_TOKEN

# Cria app temporário só para testes
app = FastAPI()
app.include_router(router)


@pytest.mark.asyncio
async def test_verify_webhook_valid_token():
    """Deve retornar o challenge quando o token está correto."""
    
    challenge_value = "123456"

    url = (
        f"/webhook?"
        f"hub.mode=subscribe&"
        f"hub.challenge={challenge_value}&"
        f"hub.verify_token={VERIFY_TOKEN}"
    )

    transport = httpx.ASGITransport(app=app)  # ✅ Novo jeito
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(url)

    assert response.status_code == 200
    assert response.text == challenge_value


@pytest.mark.asyncio
async def test_verify_webhook_invalid_token():
    """Deve retornar o challenge quando o token está correto."""
    
    url = (
        f"/webhook?"
        f"hub.mode=subscribe&"
        f"hub.challenge=abc&"
        f"hub.verify_token=WRONG"
    )

    transport = httpx.ASGITransport(app=app)  # ✅ Novo jeito
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(url)

    assert response.status_code == 403
    assert response.text == "Invalid verify token"


# ------------------------------
# TESTES POST /webhook
# ------------------------------

@pytest.mark.asyncio
async def test_receive_webhook_empty_payload():
    """Se o payload é vazio ou inválido, deve retornar ignored."""

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://test"
    ) as ac:
        response = await ac.post("/webhook", json={})

    assert response.status_code == 200
    assert response.json() == {"status": "ignored"}


@pytest.mark.asyncio
async def test_receive_webhook_no_sender():
    """Se não houver sender_name, deve retornar ignored e NÃO enviar mensagem."""

    sample_payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "text": {"body": "mensagem sem sender"}
                    }]
                }
            }]
        }]
    }

    with (
        patch("src.whatsapp.wpp_service.parse_webhook_payload") as mock_parse,
        patch("src.whatsapp.wpp_controller.send_whatsapp_message", new_callable=AsyncMock) as mock_send
    ):

        class FakeMsg:
            sender_name = None
            text = "mensagem sem sender"

        mock_parse.return_value = FakeMsg()

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.post("/webhook", json=sample_payload)

        assert response.status_code == 200
        assert response.json() == {"status": "ignored"}

        mock_send.assert_not_called()
        
        

# SAMPLE_PAYLOAD = {
#     "object": "whatsapp_business_account",
#     "entry": [
#         {
#             "id": "1370937",
#             "changes": [
#                 {
#                     "value": {
#                         "messaging_product": "whatsapp",
#                         "metadata": {
#                             "display_phone_number": "5524992356939",
#                             "phone_number_id": "83857077"
#                         },
#                         "contacts": [
#                             {
#                                 "profile": {"name": "Samuel Pacheco"},
#                                 "wa_id": "5524992156969"
#                             }
#                         ],
#                         "messages": [
#                             {
#                                 "from": "5524992156969",
#                                 "id": "wamid.HBgNNTUyNDk5MEQ2NjAxAA==",
#                                 "timestamp": "17642587",
#                                 "text": {"body": "Oba"},
#                                 "type": "text"
#                             }
#                         ]
#                     },
#                     "field": "messages"
#                 }
#             ]
#         }
#     ]
# }

# def test_parse_webhook_payload():
#     normalized = parse_webhook_payload(SAMPLE_PAYLOAD)
#     assert normalized.sender_number == "5524992156969"
#     assert normalized.sender_name == "Samuel Pacheco"
#     assert normalized.message_text == "Oba"
#     assert normalized.message_id.startswith("wamid.")
#     assert normalized.timestamp == "17642587"


# def test_log_incoming_message(caplog):
#     """Teste se a função registra corretamente o log da mensagem recebida."""

#     message = NormalizedMessage(
#         message_id="5511999999999",
#         message_text="Olá!",
#         sender_name="João",
#         sender_number="123456789",
#         timestamp="176422587"
#     )


#     with caplog.at_level("INFO"):
#         log_incoming_message(message)

#     assert "📩 Mensagem recebida de João: Olá!" in caplog.text
    
# def test_generate_basic_response():
#     """Teste simples para validar o eco da mensagem."""

#     message = NormalizedMessage(
#         message_id="5511999999999",
#         message_text="Olá!",
#         sender_name="João",
#         sender_number="123456789",
#         timestamp="176422587"
#     )

#     response = generate_basic_response(message)

#     assert response == "Recebido: Olá!"
    

# @pytest.mark.asyncio
# async def test_send_whatsapp_message_success():
#     """Mock simples usando respx, sem monkeypatch extra."""

#     # Caminho esperado da API
#     url = f"https://graph.facebook.com/{WPP_API_VERSION}/{PHONE_NUMBER_ID}/messages"


#     expected_json = {"messages": [{"id": "wamid.TEST123"}]}

#     async with respx.mock:
#         route = respx.post(url).mock(
#             return_value=httpx.Response(200, json=expected_json)
#         )

#         result = await send_whatsapp_message("5511999999999", "Olá!")

#         assert route.called
#         assert result == expected_json