import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Caminho para o JSON da chave do Firebase
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

if not os.path.exists(FIREBASE_CREDENTIALS):
    raise FileNotFoundError(f"Arquivo {FIREBASE_CREDENTIALS} não encontrado. Verifique o caminho.")

# Inicializar Firebase
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)

# Conectar ao Firestore
db = firestore.client()
