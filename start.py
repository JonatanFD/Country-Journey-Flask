from data.cities import *
from data.routes import *
from data.graph import *

### Ejecutar esto para cargar los datos de las ciudades y las rutas
def start():
    mercator()
    no_mercator()
    createRoutes()
    getGraph()

start()