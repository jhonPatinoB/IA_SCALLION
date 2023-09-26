from modelo_difusion import cargar_reglas, generar_imagen
from api_clima import obtener_temperatura

REGLAS_JSON_PATH = "data_parametros/reglas.json"

def definir_parametros(clima, terreno, meses):
    # Cargar las reglas desde el archivo JSON
    reglas = cargar_reglas(REGLAS_JSON_PATH)

    # Prompt basado en las reglas y el clima
    prompt = f"A scallion with leaves colored{reglas[clima][terreno]['Color_hojas']}, size:{reglas[clima][terreno]['Tamaño']}, stak color:{reglas[clima][terreno]['Color_tallo']}, month of cultivation: {reglas[clima][terreno]['Mes'][meses]}"

    # Generar la imagen
    imagen_resultante = generar_imagen(prompt)

    # Mostrar la imagen usando Matplotlib
    return imagen_resultante

def tipo(temperatura):
    if 0 <= temperatura <= 12:
        clima_resultante = "frío"
    elif 13 <= temperatura <= 16:
        clima_resultante = "templado"
    else:
        clima_resultante = "cálido"
    
    return clima_resultante

def main_generar(terreno, meses):
    clima = tipo(obtener_temperatura())
    return definir_parametros(clima, terreno, meses)