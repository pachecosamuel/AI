from fastapi import FastAPI
import uvicorn
from utils.config import PORT, SECRET_KEY
from api.routes.routes import router as api_router

app = FastAPI()

# Registrar rotas
app.include_router(api_router)

if __name__ == "__main__":
    print(f"SECRET_KEY usada: {SECRET_KEY}")
    print(f"Rodando na porta: {PORT}")  # Debug
    uvicorn.run(app, host="0.0.0.0", port=PORT)

