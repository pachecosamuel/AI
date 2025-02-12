from fastapi import FastAPI
import uvicorn
from api.routes import router
from src.utils.config import PORT

app = FastAPI()

# Registrar rotas
app.include_router(router)

if __name__ == "__main__":
    print(f"Rodando na porta: {PORT}")  # Debug
    uvicorn.run(app, host="0.0.0.0", port=PORT)
