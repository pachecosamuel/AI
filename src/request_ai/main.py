from fastapi import FastAPI
from pydantic import BaseModel
import cohere
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("COHERE_KEY")

# Inicializar o cliente Cohere
co = cohere.Client(api_key=API_KEY)

# Criar a aplicação FastAPI
app = FastAPI()

# Criar um modelo Pydantic para a requisição
class PromptRequest(BaseModel):
    prompt: str
    
    
@app.post("/chat-body")
async def chat(request: PromptRequest):
    """Recebe um prompt e retorna a resposta da IA."""
    resposta = co.generate(prompt=request.prompt, max_tokens=100)
    return {"resposta": resposta.generations[0].text.strip()}
    
@app.post("/chat-parameter")
async def chat(prompt: str):
    """Recebe um prompt e retorna a resposta da IA."""
    resposta = co.generate(prompt=prompt, max_tokens=100)
    return {"resposta": resposta.generations[0].text.strip()}

# Roda a API com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
