# Usa uma imagem base do Python
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala o Poetry manualmente
RUN pip install poetry

# Instala as dependências do projeto
RUN poetry install --no-dev --no-interaction --no-ansi

# Expõe a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para rodar a API
CMD ["poetry", "run", "uvicorn", "request_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
