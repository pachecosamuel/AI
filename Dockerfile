# Usa uma imagem base do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /src

# Copia apenas os arquivos necessários para instalar as dependências
COPY pyproject.toml poetry.lock /src/

# Instala o Poetry manualmente
RUN pip install poetry

# Instala as dependências do projeto antes de copiar o restante
RUN poetry install --no-dev --no-interaction --no-ansi

# Agora copia o restante dos arquivos
COPY . /src

# Expõe a porta 8000 para a API
EXPOSE 8000

# Comando para rodar a API
CMD ["poetry", "run", "uvicorn", "request_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
