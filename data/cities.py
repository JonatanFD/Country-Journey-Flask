import pandas as pd
import numpy as np
import math
from constantes import *

# Función para convertir latitud y longitud a coordenadas Mercator
def mercator_projection(lat, lon):
    width = 1920
    height = 1080
    scaleFactor = 20

    x = (lon + 180) * (width / 360) * scaleFactor - (width * scaleFactor) / 3
    y = height / 2 - math.log(math.tan(math.pi / 4 + (lat * math.pi) / 180 / 2)) * (width / (2 * math.pi)) * scaleFactor - height

    return x, y

def mercator():
    # Cargar los datos desde un archivo Excel
    df = pd.read_excel(CITIES_JSON_EXCEL)

    # Lista de países sudamericanos (ISO 2)
    south_american_countries = ['AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'GY', 'PY', 'PE', 'SR', 'UY', 'VE']

    # Filtrar las ciudades cuyos países estén en Sudamérica
    filtered_df = df[df['iso2'].isin(south_american_countries)]

    # Seleccionar solo las columnas que te interesan: ciudad, país, latitud y longitud
    filtered_df = filtered_df[['city', 'lat', 'lng', 'country']]

    # Eliminar duplicados basados en el nombre de la ciudad y el país
    filtered_df = filtered_df.drop_duplicates(subset=['city', 'country'])

    # Limitar a 200 ciudades por país
    filtered_df = filtered_df.groupby('country').head(500)

    # Aplicar la proyección de Mercator a las columnas de latitud y longitud
    filtered_df['longitude'], filtered_df['latitude'] = zip(*filtered_df.apply(lambda row: mercator_projection(row['lat'], row['lng']), axis=1))

    # Convertir el DataFrame filtrado a formato JSON con coordenadas Mercator
    json_data = filtered_df[['city', 'country', 'longitude', 'latitude']].to_json(orient="records", indent=4)

    # Guardar en un archivo JSON
    with open(CITIES_JSON_FILE, "w") as json_file:
        print(f"Cantidad de ciudades: {len(json_data)}")
        json_file.write(json_data)


def no_mercator():
    # Cargar los datos desde un archivo Excel
    df = pd.read_excel(CITIES_JSON_EXCEL)

    # Lista de países sudamericanos (ISO 2)
    south_american_countries = ['AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'GY', 'PY', 'PE', 'SR', 'UY', 'VE']

    # Filtrar las ciudades cuyos países estén en Sudamérica
    filtered_df = df[df['iso2'].isin(south_american_countries)]

    # Seleccionar solo las columnas que te interesan: ciudad, país, latitud y longitud
    filtered_df = filtered_df[['city', 'lat', 'lng', 'country']]

    # Eliminar duplicados basados en el nombre de la ciudad y el país
    filtered_df = filtered_df.drop_duplicates(subset=['city', 'country'])

    # Limitar a 200 ciudades por país
    filtered_df = filtered_df.groupby('country').head(500)

    # Aplicar la proyección de Mercator a las columnas de latitud y longitud
    filtered_df['longitude'], filtered_df['latitude'] = zip(*filtered_df.apply(lambda row: (row['lat'], row['lng']), axis=1))

    # Convertir el DataFrame filtrado a formato JSON con coordenadas Mercator
    json_data = filtered_df[['city', 'country', 'longitude', 'latitude']].to_json(orient="records", indent=4)

    # Guardar en un archivo JSON
    with open(CITIES_JSON_NO_MERCATOR, "w") as json_file:
        print(f"Cantidad de ciudades: {len(json_data)}")
        json_file.write(json_data)

no_mercator()