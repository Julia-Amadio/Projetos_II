#imagem base
FROM python:3.10

#define diretório de trabalho
WORKDIR /python_scripts

# copia scripts e requirements
COPY python_scripts/ /python_scripts/
COPY requirements.txt ./

#instala dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential && \
    rm -rf /var/lib/apt/lists/*

#instala dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#expõe a porta que o Render definirá via variável $PORT
EXPOSE 10000

#inicia o servidor FastAPI — lê a porta dinamicamente
CMD ["sh", "-c", "echo 'Starting API on port ${PORT:-10000}'; ls -R; uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]