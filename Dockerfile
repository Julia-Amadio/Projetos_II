FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c " \
    from huggingface_hub import snapshot_download; \
    print('Downloading ConvNext models (snapshot)...'); \
    snapshot_download(repo_id='facebook/convnext-large-224-22k-1k'); \
    print('ConvNext models downloaded.'); \
    "

RUN python -c " \
    from rembg import new_session; \
    print('Downloading rembg models (u2net)...'); \
    new_session('u2net'); \
    print('rembg models downloaded.'); \
    "

COPY python_scripts/ ./python_scripts/

EXPOSE 10000

CMD uvicorn python_scripts.main:app --host 0.0.0.0 --port $PORT