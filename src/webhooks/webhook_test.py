from fastapi import FastAPI, Request, Query
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

VERIFY_TOKEN = "meu_token_secreto_123"

@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
    ):
    
    print("📩 GET recebido:", {
    "hub.mode": hub_mode,
    "hub.challenge": hub_challenge,
    "hub.verify_token": hub_verify_token
    })
        
    if hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)

    return PlainTextResponse(content="Invalid verify token", status_code=403)


@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("📩 Webhook recebido:", data)
    return {"status": "received"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
