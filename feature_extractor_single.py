import os
import torch
import numpy as np
from PIL import Image
from rembg import remove
from torchvision import transforms
from transformers import ConvNextImageProcessor, ConvNextForImageClassification


#Função de segmentação + fundo branco
def segment_and_whitebg(image_path: str, save_dir: str = "processed") -> str:
    """
    Remove o fundo de uma folha e substitui por branco
    Retorna o caminho da imagem salva
    """
    os.makedirs(save_dir, exist_ok=True)

    #Remove fundo
    input_img = Image.open(image_path).convert("RGB")
    output = remove(input_img)  #RGBA (com transparência)

    #Adiciona fundo branco
    bg = Image.new("RGBA", output.size, (255, 255, 255, 255))
    whitebg = Image.alpha_composite(bg, output).convert("RGB")

    #Caminho da imagem processada
    base_name = os.path.basename(image_path)
    name, _ = os.path.splitext(base_name)
    save_path = os.path.join(save_dir, f"{name}_whitebg.jpg")

    #Salva
    whitebg.save(save_path, "JPEG", quality=95)
    print(f"Imagem segmentada e salva em: {save_path}")

    return save_path


#Classe para extração de features (ConvNeXt)
class FeatureExtractor:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Usando dispositivo: {self.device}")

        #Modelo e pré-processador
        self.processor = ConvNextImageProcessor.from_pretrained(
            "facebook/convnext-large-224-22k-1k"
        )
        self.model = ConvNextForImageClassification.from_pretrained(
            "facebook/convnext-large-224-22k-1k"
        ).to(self.device)

        #Remove camada de classificação (ficam só as features)
        self.model.classifier = torch.nn.Identity()
        self.model.eval()

    def extract_convnext(self, image_path: str) -> np.ndarray:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            features = self.model(**inputs).logits
        features_np = features.cpu().numpy().flatten()
        print(f"Vetor de características extraído com shape: {features_np.shape}")
        return features_np


#Função principal
def process_single_image(image_path: str, output_dir: str = "processed"):
    """
    Faz todo o pipeline em uma única imagem:
    - Segmentação e substituição do fundo
    - Extração de features ConvNeXt
    """
    #1) Segmentação e fundo branco
    processed_path = segment_and_whitebg(image_path, save_dir=output_dir)

    #2) Extração de features
    extractor = FeatureExtractor()
    features = extractor.extract_convnext(processed_path)

    #3) Salvar o vetor de características
    feat_path = os.path.join(output_dir, "features_single.npy")
    np.save(feat_path, features)
    print(f"Vetor de características salvo em: {feat_path}")

    return feat_path


#Execução direta
if __name__ == "__main__":
    #Caminho da imagem
    image_path = r"C:\Users\Julia\Downloads\clb2_600px.jpg"

    #Executa pipeline completo
    process_single_image(image_path)