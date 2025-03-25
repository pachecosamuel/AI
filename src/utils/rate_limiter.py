from fastapi import Request, HTTPException, status, Depends
from datetime import datetime, timedelta
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Dicionário para armazenar tentativas
failed_attempts = {}

# Configurações do limitador
MAX_ATTEMPTS = 5  # Máximo de tentativas antes do bloqueio
BLOCK_TIME = timedelta(minutes=5)  # Tempo de bloqueio

async def rate_limiter(request: Request):
    client_ip = request.client.host  # Captura o IP do usuário
    now = datetime.now()

    # Recupera dados do usuário/IP
    attempts = failed_attempts.get(client_ip, {"count": 0, "last_attempt": None, "blocked_until": None})

    logger.info(f"Tentativa de acesso do IP: {client_ip}. Tentativas anteriores: {attempts['count']}")

    # Se estiver bloqueado, verifica se o tempo expirou
    if attempts["blocked_until"] and now < attempts["blocked_until"]:
        logger.warning(f"IP {client_ip} bloqueado até {attempts['blocked_until']}. Bloqueando requisição.")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Excesso de tentativas. Tente novamente após {attempts['blocked_until']}."
        )

    # Atualiza contagem e horário da tentativa
    attempts["count"] += 1
    attempts["last_attempt"] = now

    # Bloqueia se exceder o limite
    if attempts["count"] > MAX_ATTEMPTS:
        attempts["blocked_until"] = now + BLOCK_TIME
        failed_attempts[client_ip] = attempts
        logger.error(f"IP {client_ip} excedeu o limite ({MAX_ATTEMPTS} tentativas). Bloqueado até {attempts['blocked_until']}.")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Aguarde 5 minutos."
        )

    failed_attempts[client_ip] = attempts  # Atualiza registro

    logger.info(f"Tentativa permitida para o IP {client_ip}. Total de tentativas: {attempts['count']}")



def reset_attempts(client_ip: str):
    """Remove o IP do dicionário de tentativas após login bem-sucedido."""
    if client_ip in failed_attempts:
        del failed_attempts[client_ip]


