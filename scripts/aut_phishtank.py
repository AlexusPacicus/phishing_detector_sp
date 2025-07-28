import requests
import pandas as pd
from datetime import datetime
import os
import logging
import time
from logging.handlers import RotatingFileHandler

# --- Rutas y logging ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')
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
SOURCE = "PhishTank"

def obtener_datos_phishtank(url=PHISHTANK_URL, intentos=3, delay=5):
    """
    Descarga el CSV de PhishTank y lo guarda localmente. Devuelve la ruta del archivo.
    """
    for intento in range(1, intentos + 1):
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f'phishtank_online_valid_{fecha_hora}.csv'
            ruta_guardado = os.path.join(DATA_DIR, nombre_archivo)
            with open(ruta_guardado, 'wb') as f:
                f.write(response.content)
            logger.info(f"[{SOURCE}] Archivo descargado y guardado en {ruta_guardado}")
            return ruta_guardado
        except requests.exceptions.RequestException as e:
            logger.warning(f"[{SOURCE}] Error en intento {intento}: {e}")
            if intento < intentos:
                logger.info(f"[{SOURCE}] Esperando {delay} segundos antes del siguiente intento")
                time.sleep(delay)
            else:
                logger.error(f"[{SOURCE}] No se pudo descargar el feed tras {intentos} intentos.")
                return None

def procesar_datos(ruta_csv):
    """
    Procesa el CSV descargado: valida, deduplica y añade metadatos.
    """
    if os.path.getsize(ruta_csv) < 100:
        logger.error(f"[{SOURCE}] El archivo descargado está vacío o corrupto: {ruta_csv}")
        raise ValueError(f"Archivo vacío o corrupto: {ruta_csv}")
    try:
        df = pd.read_csv(ruta_csv)
    except Exception as e:
        logger.error(f"[{SOURCE}] No se pudo leer el CSV: {ruta_csv} | Error: {e}")
        raise
    if 'url' not in df.columns:
        logger.error(f"[{SOURCE}] El archivo no contiene la columna 'url': columnas={df.columns.tolist()}")
        raise ValueError("El archivo descargado de PhishTank no tiene la columna 'url'.")
    antes = len(df)
    df = df.drop_duplicates(subset='url')
    logger.info(f"[{SOURCE}] Duplicados eliminados: {antes - len(df)}")
    logger.info(f"[{SOURCE}] Total URLs únicas tras limpieza: {len(df)}")
    df['fecha_hora_recoleccion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['fuente'] = SOURCE
    return df

def guardar_datos(df):
    """
    Guarda el DataFrame limpio y loguea el resultado.
    """
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'phishtank_procesado_{fecha_hora}.csv'
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)
    df.to_csv(ruta_archivo, index=False)
    logger.info(f"[{SOURCE}] Guardados {len(df)} registros procesados en {ruta_archivo}.")

if __name__ == "__main__":
    ruta = obtener_datos_phishtank()
    if ruta:
        df = procesar_datos(ruta)
        guardar_datos(df)
        print(f"[INFO] Guardados {len(df)} registros procesados en {DATA_DIR}")
    else:
        print("[WARNING] No se pudo descargar el dump de PhishTank. Ver logs para más información.")
