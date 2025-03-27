from fastapi import Request, HTTPException, status, Depends
from datetime import datetime, timedelta, timezone
from utils.firebase import db
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Dicionário para armazenar tentativas
failed_attempts = {}
collection_ref = db.collection("failed_attempts") 

# Configurações do limitador
MAX_ATTEMPTS = 3
BLOCK_TIME = timedelta(minutes=5)  



def get_attempts(client_ip: str) -> dict:
    """Recupera as tentativas de login do Firestore ou cache local."""
    if client_ip in failed_attempts:
        return failed_attempts[client_ip]  
    
    doc_ref = collection_ref.document(client_ip)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    
    return {"count": 0, "last_attempt": None, "blocked_until": None}


def is_blocked(attempts: dict, now: datetime, client_ip: str):
    """Verifica se o IP está bloqueado e lança exceção se necessário."""
    blocked_until = attempts["blocked_until"]

    if blocked_until:
        if isinstance(blocked_until, str):  # Se Firestore salvou como string, converte
            blocked_until = datetime.fromisoformat(blocked_until).replace(tzinfo=timezone.utc)

        if now < blocked_until:
            logger.warning(f"IP {client_ip} bloqueado até {blocked_until}. Bloqueando requisição.")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Excesso de tentativas. Tente novamente após {blocked_until}."
            )

def update_attempts(client_ip: str, attempts: dict, now: datetime):
    """Atualiza as tentativas de login e salva no Firestore."""
    attempts["count"] += 1
    attempts["last_attempt"] = now

    if attempts["count"] > MAX_ATTEMPTS:
        attempts["blocked_until"] = now + BLOCK_TIME
        logger.error(f"IP {client_ip} excedeu o limite ({MAX_ATTEMPTS} tentativas). Bloqueado até {attempts['blocked_until']}.")
    else:
        attempts["blocked_until"] = None  # Garante que não bloqueia indevidamente

    failed_attempts[client_ip] = attempts
    collection_ref.document(client_ip).set(attempts)  # Salva no Firestore


async def rate_limiter(request: Request):
    """Middleware de limitação de requisições baseado no IP."""
    client_ip = request.client.host
    now = datetime.now(timezone.utc)

    attempts = get_attempts(client_ip)

    # Se o tempo de bloqueio expirou, resetamos o contador
    if attempts["blocked_until"] and now >= attempts["blocked_until"]:
        logger.info(f"IP {client_ip} foi desbloqueado automaticamente após expiração do tempo limite.")
        collection_ref.document(client_ip).delete()  # Remove do Firestore
        failed_attempts.pop(client_ip, None)  # Remove do cache local
        attempts = {"count": 0, "last_attempt": None, "blocked_until": None}

    is_blocked(attempts, now, client_ip)
    update_attempts(client_ip, attempts, now)

    logger.info(f"Tentativa permitida para o IP {client_ip}. Total de tentativas: {attempts['count']}")


def reset_attempts(client_ip: str):
    """Reseta as tentativas de login após um login bem-sucedido."""
    if client_ip in failed_attempts:
        del failed_attempts[client_ip]
    
    collection_ref.document(client_ip).delete()
    logger.info(f"Tentativas do IP {client_ip} resetadas após login bem-sucedido.")