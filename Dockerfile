FROM python:3.10

WORKDIR /python_scripts

COPY python_scripts/ /python_scripts/

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git wget ca-certificates libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]