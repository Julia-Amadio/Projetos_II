#imagem base
FROM python:3.10
WORKDIR /app
COPY requirements.txt ./
COPY python_scripts/ .

#instala dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

#instala dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#expõe a porta que o Render definirá via variável $PORT
EXPOSE 10000

#inicia o servidor FastAPI (sem o prefixo python_scripts)
CMD uvicorn main:app --host 0.0.0.0 --port $PORT