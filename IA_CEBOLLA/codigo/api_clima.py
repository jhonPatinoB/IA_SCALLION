import requests
import json

start_time = '2023-09-26T04:00:00Z'
api_key = 'xRct8cslHTNgI7mXmSwHe0sLDv202AJ4'
location = 'aquitania'
url = f"https://api.tomorrow.io/v4/weather/history/recent?location={location}&start_time={start_time}&apikey={api_key}"
headers = {"accept": "application/json"}

def obtener_temperatura():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        forecast = json.loads(response.text)

        # Fecha deseada que quieres buscar
        target_date = start_time

        # Busca la posición de la fecha deseada dentro de los datos
        position = None
        for index, hourly_data in enumerate(forecast["timelines"]["hourly"]):
            if hourly_data["time"] == target_date:
                position = index
                break

        if position is not None:
            temperature = forecast["timelines"]["hourly"][position]["values"]["temperature"]
            print(f"La temperatura para la fecha {target_date} en Aquitania es de {temperature}°C.")
            return temperature
        else:
            print("no se encontro nada")
    else:
        print("Error:", response.status_code)
