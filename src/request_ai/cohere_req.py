import cohere
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_KEY")

# co = cohere.Client(COHERE_API = os.getenv("COHERE_KEY"))
co = cohere.Client(api_key = API_KEY)
resposta = co.generate(prompt="Explique o que é inteligência artificial.", max_tokens=50)
print("\n🤖 Resposta da IA:", resposta.generations[0].text)
