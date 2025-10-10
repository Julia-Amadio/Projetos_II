'''
TESTE DE EXECUÇÃO:
    ESTE CÓDIGO USA UM AMBIENTE PYTHON 3.11!!!!!!!!! ISSO DEVE SER ALTERADO NAS CONFIGS DA IDE!!!!!!!!!
    Se já tiver uma versão superior, fazer download do Python 3.11 e criar o ambiente.
    NO PYCHARM --> File > Settings > Python > Interpreter > Add interpreter > Local interpreter > Escolher o ambiente 3.11 criado
    Depois disso, ir no menu de Run na parte superior da tela > Edit configurations > Selecionar o ambiente 3.11
    1 - Manter requirements.txt no mesmo diretório deste script.
    2 - Manter a pasta das imagens que serão segmentadas no mesmo diretório deste script.
        A pasta mencionada acima deve possuir subpastas para separação das classes.
    3 - AJUSTAR OS DIRETÓRIOS DENTRO DA MAIN
    4 - RODAR NO TERMINAL ANTES DO RUN: pip install -r requirements.txt

WARNINGS A SEREM CORRIGIDOS:
    ---- UserWarning: ShiftScaleRotate is a special case of Affine transform. Please use Affine transform instead.
    original_init(self, **validated_kwargs)                             -----> LINHA 48
    Versões mais recentes do Albumentations unificaram tudo em Affine
    ShiftScaleRotate ainda funciona, mas é mantido apenas por compatibilidade (pode ser removido no futuro).
    ---- UserWarning: Argument(s) 'var_limit' are not valid for transform GaussNoise
    A.GaussNoise(var_limit=(0.01, 0.1))                                 -----> LINHA 50
    Antes, o GaussNoise aceitava o argumento var_limit=(min, max) para definir a variação do ruído.
    Agora ele mudou para std_range=(min, max) (standard deviation range)

ANOTAÇÕES:
    Mais pra frente, se quiser distribuir: pip install setuptools
    Adicionar um setup.py ou pyproject.toml para empacotar OU criar um executável .exe com pyinstaller.
'''

import os
import time
import cv2
import numpy as np
from PIL import Image
from rembg import remove
import albumentations as A


#1 ---------- Função: pipeline de augmentation
def build_augmentation_pipeline():
    #Cria e retorna o pipeline de augmentations
    return A.Compose([
        #ALTERADO: A.RandomResizedCrop(height=224, width=224, scale=(0.6, 1.0), p=1.0)
        #Não aceita mais os argumentos height e width. Espera um argumento chamado size=(H, W)
        #Versões mais novas do Albumentations (1.4+) unificaram os parâmetros de recorte aleatório
        #Confirmar a versão instalada: pip show albumentations
        A.RandomResizedCrop(size=(224, 224), scale=(0.6, 1.0), p=1.0),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.3),
        A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=25, p=0.6), #<----------------------- AQUI
        A.OneOf([
            A.GaussNoise(var_limit=(0.01, 0.1)), #<----------------------- AQUI
            A.GaussianBlur(blur_limit=(1, 3)),
        ], p=0.4),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.7),
        A.HueSaturationValue(hue_shift_limit=5, sat_shift_limit=12, val_shift_limit=10, p=0.4),
    ], p=1.0)

#2 ---------- Funções auxiliares
def segment_leaf_rembg(image_path):
    #Remove o fundo da folha usando rembg e retorna uma imagem PIL
    input_img = Image.open(image_path).convert("RGB")
    output = remove(input_img)
    return output

def prepare_image_for_augmentation(pil_image):
    #Converte PIL --> numpy e garante formato RGB (3 canais)
    img_np = np.array(pil_image)

    if len(img_np.shape) == 3 and img_np.shape[-1] == 4:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    elif len(img_np.shape) == 2 or (len(img_np.shape) == 3 and img_np.shape[-1] == 1):
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    return img_np


def augment_save_image(img_np, out_path, transform):
    #Aplica o pipeline de augmentation em uma imagem (numpy) e salva o resultado
    augmented = transform(image=img_np)
    out = augmented["image"]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cv2.imwrite(out_path, out)
    print(f"Imagem aumentada salva em: {out_path}")

#3 ---------- Função principal de processamento por pasta
def process_dataset_with_augmentation(root_dir, output_root, transform=None):
    #Percorre subpastas de 'root_dir', aplica segmentação (rembg) e data augmentation
    #Salva resultados organizados por classe
    if transform is None:
        transform = build_augmentation_pipeline()

    print("Iniciando augmentation...\n")

    for label in os.listdir(root_dir):
        class_path = os.path.join(root_dir, label)
        if not os.path.isdir(class_path):
            print(f"Pulado (não é diretório): {class_path}")
            continue

        out_class_dir = os.path.join(output_root, label + "_aug")
        os.makedirs(out_class_dir, exist_ok=True)

        print(f"Processando classe: {label}")
        for img_name in os.listdir(class_path):
            if img_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                img_path = os.path.join(class_path, img_name)
                out_path = os.path.join(out_class_dir, img_name)

                try:
                    print(f"  Aplicando augmentation em: {img_name}")
                    start_rembg = time.time()
                    result_rembg = segment_leaf_rembg(img_path)
                    end_rembg = time.time()
                    print(f"    Fundo removido em {end_rembg - start_rembg:.2f}s")

                    #Converte e garante formato RGB
                    result_rembg_np = prepare_image_for_augmentation(result_rembg)

                    #Aplica augmentation e salva
                    augment_save_image(result_rembg_np, out_path, transform)

                except Exception as e:
                    print(f"ERRO ao processar {img_path}: {e}")
    print("\nAugmentation concluída!")

#4 ----------  Ponto de entrada
if __name__ == "__main__":
    root_dir = r"/Users/Julia/Desktop/projsoja/fundoruim_teste"
    output_root = r"/Users/Julia/Desktop/projsoja/output"
    process_dataset_with_augmentation(root_dir, output_root)