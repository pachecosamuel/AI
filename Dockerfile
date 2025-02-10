# Usa uma imagem base do Python
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /src

# Copia os arquivos necessários para instalar as dependências
COPY pyproject.toml poetry.lock /src/

# Instala o Poetry manualmente
RUN pip install poetry

# Configura o Poetry para não criar ambientes virtuais dentro do container
RUN poetry config virtualenvs.create false

# Agora copia o restante dos arquivos (incluindo `main.py`)
COPY . /src

# Instala as dependências do projeto após copiar todos os arquivos
RUN poetry install --only main --no-root --no-interaction --no-ansi

# **DEBUG: Lista os arquivos do diretório para verificar a estrutura**
RUN ls -R /src | grep -E "main.py|request_ai"

# Expõe a porta 8000 para a API
EXPOSE 8000

# Executa a aplicação apontando para o local correto de `main.py`
CMD ["poetry", "run", "python", "src/request_ai/main.py"]
