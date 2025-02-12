import cohere
from src.utils.config import API_KEY

co = cohere.Client(api_key=API_KEY)

def generate_response(prompt: str, max_tokens: int = 100) -> str:
    """Gera resposta da IA a partir do prompt."""
    response = co.generate(prompt=prompt, max_tokens=max_tokens)
    return response.generations[0].text.strip()
