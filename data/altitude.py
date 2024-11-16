import requests
import json
import random
import pandas as pd
from constantes import *

def getRandomBetween(min, max):
    return random.randint(min, max)

def obtener_altitud(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        altitud = data['results'][0]['elevation']
        return altitud
    else:
        return None  # En caso de error

def extraer_altitud(punto):
    with open(CITIES_JSON_NO_MERCATOR, "r") as archivo:
        puntos = json.load(archivo)

    for punto in puntos:
        lat = punto["latitude"]
        lon = punto["longitude"]
        altitud = obtener_altitud(lon, lat)
        if altitud is not None:
            print(f"Altitud para lat: {lat}, lon: {lon} es: {altitud} metros")
            punto["altitude"] = altitud
        else:
            print(f"Error al obtener altitud para lat: {lat}, lon: {lon}")
            punto["altitude"] = getRandomBetween(0, 6000)

    with open(CITIES_JSON_NO_MERCATOR, "w") as archivo:
        json.dump(puntos, archivo, indent=4)

with open(CITIES_JSON_NO_MERCATOR, "r") as archivo:
    puntos = json.load(archivo)
    df = pd.DataFrame(puntos)
    df.to_excel('ciudades_sudamericanas.xlsx', index=False)

### Ejecutar solamente si no se tiene la informacion de la altitud