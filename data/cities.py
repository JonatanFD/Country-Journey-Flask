import pandas as pd
import numpy as np
import math
from data.constantes import *
import json

def mercator_projection(lat, lon):
    width = 1920
    height = 1080
    scaleFactor = 20

    x = (lon + 180) * (width / 360) * scaleFactor - (width * scaleFactor) / 3
    y = height / 2 - math.log(math.tan(math.pi / 4 + (lat * math.pi) / 180 / 2)) * (width / (2 * math.pi)) * scaleFactor - height

    return x, y

def mercator():
    df = pd.read_excel(CITIES_JSON_EXCEL)

    south_american_countries = ['AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'GY', 'PY', 'PE', 'SR', 'UY', 'VE']
    filtered_df = df[df['iso2'].isin(south_american_countries)]
    filtered_df = filtered_df[['city', 'lat', 'lng', 'country']]
    filtered_df = filtered_df.drop_duplicates(subset=['city', 'country'])
    filtered_df = filtered_df.groupby('country').head(500)
    filtered_df['longitude'], filtered_df['latitude'] = zip(*filtered_df.apply(lambda row: mercator_projection(row['lat'], row['lng']), axis=1))
    json_data = filtered_df[['city', 'country', 'longitude', 'latitude']].to_json(orient="records", indent=4)

    with open(CITIES_JSON_FILE, "w") as json_file:
        print(f"Cantidad de ciudades: {len(json_data)}")
        json_file.write(json_data)


def no_mercator():
    df = pd.read_excel(CITIES_JSON_NO_MERCATOR_EXCEL)

    json_data = df.to_dict(orient='records')

    with open(CITIES_JSON_NO_MERCATOR, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

mercator()
no_mercator()