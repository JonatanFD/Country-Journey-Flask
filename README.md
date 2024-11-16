
# Manual de Instalación y Configuración

## Requisitos del Proyecto
Este proyecto está desarrollado con:
- Flask (Framework web)
- Anaconda (Entorno de desarrollo)

## Instalación de Anaconda

1. Descarga Anaconda:
   - Visita [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)
   - Selecciona la versión correspondiente a tu sistema operativo (Windows/MacOS/Linux)

2. Instala Anaconda:
   - **Windows**: Ejecuta el instalador descargado y sigue las instrucciones
   - **MacOS**: Abre el archivo .pkg descargado y sigue el asistente
   - **Linux**: Desde terminal:
     ```bash
     bash ~/Downloads/Anaconda3-20XX.XX-Linux-x86_64.sh
     ```

3. Verifica la instalación:
   ```bash
   conda --version
   ```

## Configuración del Proyecto

1. Crea un nuevo entorno:
   ```bash
   conda create --name env python=3.9
   ```

2. Activa el entorno:
   ```bash
   conda activate env
   ```

3. Instala las dependencias:
   ```bash
   pip install flask
   ```

## Carga de Datos
Es importante ejecutar este script primero para cargar los datos de las ciudades y las rutas.

Ejecutar:
   ```bash
   python start.py
   ```


## Iniciar el Servidor Flask

1. Activa el entorno si no está activo:
   ```bash
   conda activate env
   ```

2. Inicia el servidor:
   ```bash
   flask --app main run --debug
   ```

3. Accede a la aplicación en tu navegador:
   - [http://localhost:5000](http://localhost:5000)