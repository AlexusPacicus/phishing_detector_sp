# recolector_phishing.py
# Autor: Alexis Zapico Fernández
# Objetivo: Descargar automáticamente URLs de phishing desde OpenPhish y guardarlas en data/raw/phishing

import requests
import pandas as pd
from datetime import datetime
import os
import logging

 # Usar __file__ para rutas absolutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOGS_DIR, 'recolector_phishing.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

FEED_URL = "https://openphish.com/feed.txt"

def obtener_datos_openphish(url=FEED_URL):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        urls = response.text.strip().split('\n')
        logging.info(f"Descargadas {len(urls)} URLs de OpenPhish.")
        return urls
    except Exception as e:
        logging.error(f'Error descargando datos de OpenPhish: {e}')
        return []

def procesar_datos(urls):
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    datos = []
    for url in urls:
        datos.append({
            'url': url,
            'fecha_hora_recoleccion': fecha_hora,
            'fuente': 'OpenPhish',
            'observaciones': ''
        })
    return pd.DataFrame(datos)

def guardar_datos(df):
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'openphish_{fecha_hora}.csv'
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)
    df.to_csv(ruta_archivo, index=False)
    logging.info(f"Guardados {len(df)} registros en {ruta_archivo}.")

if __name__ == "__main__":
    urls = obtener_datos_openphish()
    if urls:
        df = procesar_datos(urls)
        guardar_datos(df)
        print(f"[INFO] Guardadas {len(df)} URLs en {DATA_DIR}")
    else:
        print("[WARNING] No se han descargado datos de OpenPhish. Ver logs para más información.")
