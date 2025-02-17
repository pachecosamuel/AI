# src\utils\config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COHERE_KEY")
PORT = int(os.getenv("PORT", 8080))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

