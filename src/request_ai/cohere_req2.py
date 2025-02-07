import cohere
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_KEY")

co = cohere.ClientV2(API_KEY)
response = co.chat(
    model="command-r-plus", 
    messages=[{"role": "user", "content": "hello world!"}]
)

print(response)
