from google.cloud import firestore
from google.cloud.firestore import Client
from utils.config import FIREBASE_CREDENTIALS

# Inicializando Firestore
db: Client = firestore.Client.from_service_account_info(FIREBASE_CREDENTIALS)

def get_user(identifier: str) -> dict | None:
    """Busca um usuário pelo e-mail ou username no Firestore."""
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

def create_user(username: str, email: str, hashed_password: str, full_name: str = "") -> dict:
    """Cria um novo usuário no Firestore."""
    users_ref = db.collection("users")

    # Verifica se já existe um usuário com esse e-mail ou username
    if get_user(email) or get_user(username):
        raise ValueError("Usuário já cadastrado")

    user_data = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "full_name": full_name,
        "disabled": False
    }

    new_user_ref = users_ref.add(user_data)
    
    return {"id": new_user_ref[1].id, **user_data}
