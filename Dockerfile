FROM python:3.10-slim

#Define diretório de trabalho dentro do container
WORKDIR /python_scripts

#Copia os arquivos do projeto para dentro da imagem
COPY . /python_scripts

#Atualiza o pip e instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

#Instalação das dependências Python
RUN pip install --no-cache-dir -r requirements_notFinished.txt

#Configuração da aplicação
EXPOSE 8000

#Comando de inicialização da API FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]