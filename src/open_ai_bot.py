import os
import openai
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("🚨 A chave da OpenAI não foi encontrada. Verifique seu .env!")

# Criar cliente OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def perguntar_ia(pergunta):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": pergunta}]
    )
    return resposta.choices[0].message.content

if __name__ == "__main__":
    pergunta = input("Pergunte algo para a IA: ")
    resposta = perguntar_ia(pergunta)
    print("\n🤖 Resposta da IA:", resposta)
