import requests
from dotenv import load_dotenv
import os
import random

# Set a seed for reproducibility
random.seed(42)

# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face token from the environment variables
HF_TOKEN = os.getenv('HGFACE')

# Configuração da API da Hugging Face
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}