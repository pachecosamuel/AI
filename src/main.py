from fastapi import FastAPI
import uvicorn
from api.routes import auth_routes, service_routes

app = FastAPI()

# Registrar rotas
app.include_router(auth_routes.router)
app.include_router(service_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

