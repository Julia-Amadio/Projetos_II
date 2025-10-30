from fastapi import FastAPI, File, UploadFile
from python_scripts.feature_extractor_single import process_single_image
import shutil
import os

app = FastAPI(title="SojaFeatExtractorAPI")

@app.post("/extract_features/")
async def extract_features(file: UploadFile = File(...)):
    """
    Endpoint que recebe uma imagem e retorna o caminho
    do vetor de características extraído.
    """
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #Processa a imagem (segmentação + extração)
    features_path = process_single_image(temp_path)

    #Remove imagem temporária
    os.remove(temp_path)

    return {"features_saved_at": features_path}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    import uvicorn
    uvicorn.run("python_scripts.main:app", host="0.0.0.0", port=port)
