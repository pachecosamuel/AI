# Usa uma imagem base do Python
FROM python:3.11

# Define o diretório de trabalho
WORKDIR /src 

# Copia apenas os arquivos necessários para instalar as dependências
COPY pyproject.toml poetry.lock /src/

# Instala o Poetry manualmente
RUN pip install poetry

# Configura o Poetry para criar o ambiente virtual dentro do container
RUN poetry config virtualenvs.create false

# Instala as dependências do projeto antes de copiar o restante
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Agora copia o restante dos arquivos
COPY . /src

# **DEBUG: Verifica se os arquivos estão no lugar correto**
RUN ls -R /src
RUN if [ -f "/src/main.py" ]; then echo "main.py encontrado!"; else echo "main.py NÃO ENCONTRADO!"; fi
RUN if [ -f "/src/request_ai/main.py" ]; then echo "request_ai/main.py encontrado!"; else echo "request_ai/main.py NÃO ENCONTRADO!"; fi

# Expõe a porta 8000 para a API
EXPOSE 8000

# **Correção do CMD: Chama o caminho correto do main.py**
CMD ["poetry", "run", "python", "request_ai/main.py"]
