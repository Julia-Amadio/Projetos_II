#Imagem base
FROM python:3.10

WORKDIR /app

#Instala dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

#Copia o requirements.txt primeiro para cachear a camada de dependências
COPY requirements.txt .

#Instala dependências python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#PRÉ-DOWNLOAD DOS MODELOS
#Força o download dos modelos do Transformers e do rembg durante o build,
#para que eles já existam quando o servidor iniciar.
RUN python -c " \
    from transformers import ConvNextImageProcessor, ConvNextForImageClassification; \
    print('Downloading ConvNext models...'); \
    ConvNextImageProcessor.from_pretrained('facebook/convnext-large-224-22k-1k'); \
    ConvNextForImageClassification.from_pretrained('facebook/convnext-large-224-22k-1k'); \
    print('ConvNext models downloaded.'); \
    \
    from rembg import new_session; \
    print('Downloading rembg models (u2net)...'); \
    new_session('u2net'); \
    print('rembg models downloaded.'); \
    "

#Copia o código da aplicação
#vem DEPOIS do pip install e do download
COPY python_scripts/ ./python_scripts/

#Expõe a porta (apenas para documentação, Render usará $PORT)
EXPOSE 10000

#Inicia o servidor FastAPI usando a variável $PORT fornecida pelo Render
#forma "shell" simples que interpreta a variável de ambiente
CMD uvicorn python_scripts.main:app --host 0.0.0.0 --port $PORT