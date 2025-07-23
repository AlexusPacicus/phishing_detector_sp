# recolector_phishing.py
# Autor: Alexis Zapico Fernández
# Objetivo: Descargar automáticamente URLs de phishing desde OpenPhish y guardarlas en data/raw/phishing

import requests
import pandas as pd
from datetime import datetime
import os
import logging
import time
from logging.handlers import RotatingFileHandler

 # Usar __file__ para rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

log_file = os.path.join(LOGS_DIR, 'recolector_phishing.log')

handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


FEED_URL = "https://openphish.com/feed.txt"

def obtener_datos_openphish(url=FEED_URL, intentos=3, delay=5):
    """Descarga URLs del feed con reintentos y manejo de errores."""
    for intento in range(1, intentos + 1):
        try:
            logging.info(f'Intento {intento} de descarga desde {url}')
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            urls = response.text.strip().split('\n')
            logging.info(f"Descargadas {len(urls)} URLs en el intento {intento}.")
            return urls
        except requests.exceptions.RequestException as e:
            logging.warning(f'Error en el intento {intento}: {e}')
            if intento < intentos:
                logging.info(f'Esperando {delay} segundos antes del siguiente intento')
                time.sleep(delay)
            else:
                logging.error(f'No se pudo descargar el feed tras {intentos} intentos.')
                return []

def procesar_datos(urls):
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    urls_unicas = list(set(urls))
    datos = []
    for url in urls_unicas:
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
