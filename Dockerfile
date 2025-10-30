#imagem base
FROM python:3.10

#define diretório de trabalho
WORKDIR /python_scripts

#copia scripts e requirements
COPY python_scripts/ /python_scripts/
COPY requirements.txt ./

#instala dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential && \
    rm -rf /var/lib/apt/lists/*

#instala dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#expõe a porta padrão
EXPOSE 8000

#inicia a API (usa $PORT se existir)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]