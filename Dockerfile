#Use Python 3.11 (compatível com PyTorch CPU e rembg-lite)
FROM python:3.11-slim

#Define diretório de trabalho
WORKDIR /python_scripts

#Copia código da pasta local
COPY python_scripts/ /python_scripts/

#Copia requirements
COPY requirements.txt ./

#Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

#Instala pip atualizado
RUN pip install --no-cache-dir --upgrade pip

#Instala todas as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

#Expõe porta para FastAPI
EXPOSE 8000

#Comando para iniciar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]