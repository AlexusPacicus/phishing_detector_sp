# recolector_phishtank.py
import requests
import pandas as pd
from datetime import datetime
import os
import logging
import time
from logging.handlers import RotatingFileHandler

# Configuración rutas igual que OpenPhish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')  # misma carpeta
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

log_file = os.path.join(LOGS_DIR, 'recolector_phishtank.log')
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

PHISHTANK_URL = "https://data.phishtank.com/data/online-valid.csv"

def obtener_datos_phishtank(url=PHISHTANK_URL, intentos=3, delay=5):
    for intento in range(1, intentos + 1):
        try:
            logger.info(f'Intento {intento} de descarga desde {url}')
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Guardamos el CSV con timestamp
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f'phishtank_online_valid_{fecha_hora}.csv'
            ruta_guardado = os.path.join(DATA_DIR, nombre_archivo)

            with open(ruta_guardado, 'wb') as f:
                f.write(response.content)

            logger.info(f"Archivo descargado y guardado en {ruta_guardado}")
            return ruta_guardado

        except requests.exceptions.RequestException as e:
            logger.warning(f'Error en intento {intento}: {e}')
            if intento < intentos:
                logger.info(f'Esperando {delay} segundos antes del siguiente intento')
                time.sleep(delay)
            else:
                logger.error(f'No se pudo descargar el feed tras {intentos} intentos.')
                return None

def procesar_datos(ruta_csv):
    # Solo cargamos el CSV y añadimos metadatos mínimos (ejemplo)
    df = pd.read_csv(ruta_csv)
    df['fecha_hora_recoleccion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['fuente'] = 'PhishTank'
    return df

def guardar_datos(df):
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'phishtank_procesado_{fecha_hora}.csv'
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)
    df.to_csv(ruta_archivo, index=False)
    logger.info(f"Guardados {len(df)} registros procesados en {ruta_archivo}.")

if __name__ == "__main__":
    ruta = obtener_datos_phishtank()
    if ruta:
        df = procesar_datos(ruta)
        guardar_datos(df)
        print(f"[INFO] Guardados {len(df)} registros procesados en {DATA_DIR}")
    else:
        print("[WARNING] No se pudo descargar el dump de PhishTank. Ver logs para más información.")
