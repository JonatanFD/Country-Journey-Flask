import json
import numpy as np
from scipy.spatial import Delaunay
from data.constantes import *

def cargar_ciudades(archivo):
    with open(archivo, 'r') as f:
        return json.load(f)

def calcular_distancia(ciudad1, ciudad2):
    return np.sqrt((ciudad1['longitude'] - ciudad2['longitude'])**2 +
                   (ciudad1['latitude'] - ciudad2['latitude'])**2)

def calcular_rutas_delaunay(ciudades, distancia_maxima):
    coordenadas = np.array(
        [[ciudad['longitude'], ciudad['latitude']] for ciudad in ciudades])
    tri = Delaunay(coordenadas)

    rutas = []
    for simplex in tri.simplices:
        for i in range(3):
            for j in range(i+1, 3):
                ciudad1 = ciudades[simplex[i]]
                ciudad2 = ciudades[simplex[j]]
                distancia = calcular_distancia(ciudad1, ciudad2)

                if distancia <= distancia_maxima:
                    ruta = {
                        "from": f"{ciudad1['city']},{ciudad1['country']}",
                        "to": f"{ciudad2['city']},{ciudad2['country']}",
                        "distance": distancia
                    }
                    rutas.append(ruta)

    return rutas

def eliminar_rutas_duplicadas(rutas):
    rutas_unicas = {}
    for ruta in rutas:
        ciudades = tuple(sorted([ruta['from'], ruta['to']]))
        if ciudades not in rutas_unicas or ruta['distance'] < rutas_unicas[ciudades]['distance']:
            rutas_unicas[ciudades] = ruta

    return list(rutas_unicas.values())

def calcular_y_guardar_rutas(ciudades, archivo_salida, distancia_maxima):
    rutas = calcular_rutas_delaunay(ciudades, distancia_maxima)
    rutas_unicas = eliminar_rutas_duplicadas(rutas)

    with open(archivo_salida, 'w') as f:
        json.dump(rutas_unicas, f, indent=4)
    
    print(f"Se han guardado {len(rutas_unicas)} rutas únicas en {archivo_salida}")


def createRoutes():
    ciudades = cargar_ciudades(CITIES_JSON_FILE)
    distancia_maxima = 1200
    calcular_y_guardar_rutas(ciudades, ROUTES_JSON_FILE, distancia_maxima)

createRoutes()