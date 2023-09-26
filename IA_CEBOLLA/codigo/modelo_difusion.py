import json
import torch
import matplotlib.pyplot as plt
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image

model_id = "stabilityai/stable-diffusion-2-1"

# Cargar las reglas desde el archivo JSON
def cargar_reglas(rutas_reglas):
    with open(rutas_reglas, 'r') as archivo:
        reglas = json.load(archivo)
    return reglas

# Función para generar una imagen basada en un prompt
def generar_imagen(prompt):
    model_id = "stabilityai/stable-diffusion-2-1"

    # Usar el DPMSolverMultistepScheduler
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_attention_slicing()

    # Generar la imagen
    image = pipe(prompt, height=512, width=768, num_inference_steps=10).images[0]

    return image
