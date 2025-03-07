import os
import shutil
import logging
from fastapi import UploadFile

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"

def save_file(file: UploadFile) -> str:
    """Salva o arquivo enviado no diretório local e retorna o caminho."""
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Arquivo salvo com sucesso: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Erro ao salvar o arquivo: {e}")
        raise
