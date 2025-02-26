import bcrypt
from google.cloud import firestore
from google.cloud.firestore import Client
from passlib.context import CryptContext
from utils.config import FIREBASE_CREDENTIALS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Inicializando Firestore
db: Client = firestore.Client.from_service_account_json(FIREBASE_CREDENTIALS)

def hash_password(password: str) -> str:
    """Gera um hash seguro para a senha."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_user(username: str, email: str, password: str, full_name: str = "") -> dict:
    """Cria um novo usuário no Firestore, armazenando a senha hashada."""
    users_ref = db.collection("users")
    
    # Verifica se o usuário já existe
    if users_ref.where("email", "==", email).get():
        raise ValueError("Email já cadastrado")
    
    if users_ref.where("username", "==", username).get():
        raise ValueError("Username já cadastrado")

    hashed_password = hash_password(password)

    user_data = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "full_name": full_name,
        "disabled": False
    }

    # Adiciona o usuário ao Firestore
    new_user_ref = users_ref.add(user_data)
    
    return {"id": new_user_ref[1].id, **user_data}


def get_user_by_email_or_username(identifier: str) -> dict | None:
    """Busca um usuário pelo e-mail ou username."""
    users_ref = db.collection("users")

    # Busca pelo email
    query_email = users_ref.where("email", "==", identifier).limit(1).get()
    if query_email:
        return query_email[0].to_dict()

    # Busca pelo username
    query_username = users_ref.where("username", "==", identifier).limit(1).get()
    if query_username:
        return query_username[0].to_dict()

    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha informada corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(identifier: str, password: str) -> dict | None:
    """Autentica um usuário verificando a senha."""
    user = get_user_by_email_or_username(identifier)
    
    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    return user