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

#expõe explicitamente a porta usada pelo Render
EXPOSE 10000

#inicia o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]