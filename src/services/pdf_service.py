import logging
from PyPDF2 import PdfReader
import os


# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """Extrai o texto de um arquivo PDF e retorna como string."""
    try:
        # Limpa o caminho do arquivo (remove aspas, normaliza barras)
        file_path = file_path.strip("\"'")  # Remove aspas duplas ou simples
        file_path = os.path.normpath(file_path)  # Normaliza barras
        
        with open(file_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        
        logger.info(f"Texto extraído com sucesso do arquivo: {file_path}")
        return text
    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {e}")
        raise



# def extract_text_from_pdf(file_path: str) -> str:
#     """Extrai o texto de um arquivo PDF e retorna como string."""
#     try:
#         with open(file_path, "rb") as pdf_file:
#             reader = PdfReader(pdf_file)
#             text = "\n".join([page.extract_text() or "" for page in reader.pages])
        
#         logger.info(f"Texto extraído com sucesso do arquivo: {file_path}")
#         return text
#     except Exception as e:
#         logger.error(f"Erro ao extrair texto do PDF: {e}")
#         raise
