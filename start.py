from data.cities import *
from data.routes import *
from data.graph import *

### Ejecutar esto para cargar los datos de las ciudades y las rutas
def main():
    mercator()
    no_mercator()
    createRoutes()
    getGraph()

main()