#Etapa base — ambiente Python leve
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
#Exibe o progresso de instalação de cada biblioteca
RUN echo "📦 Instalando dependências Python..." && \
    while read requirement; do \
        echo "➡️ Instalando: $requirement"; \
        pip install --no-cache-dir $requirement; \
    done < requirements.txt && \
    echo "✅ Todas as dependências foram instaladas com sucesso."

#Configuração da aplicação
EXPOSE 8000

#Comando de inicialização da API FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]