from fastapi import FastAPI
import uvicorn
from api.routes import auth_routes, service_routes
from whatsapp.wpp_controller import router as wpp_router

app = FastAPI()

# Registrar rotas
app.include_router(auth_routes.router)
app.include_router(service_routes.router)
app.include_router(wpp_router)
# app.include_router(wpp_router, prefix="/whatsapp")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

