# =====================================
# Imagem base
# =====================================
FROM python:3.10

# Define diretório de trabalho
WORKDIR /python_scripts

# Copia scripts e requirements
COPY python_scripts/ /python_scripts/
COPY requirements.txt ./

# Instala dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da API
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]