import requests
import pandas as pd
from datetime import datetime
import os
import logging
import time
from logging.handlers import RotatingFileHandler
from io import StringIO

# --- Rutas y logging ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

log_file = os.path.join(LOGS_DIR, 'recolector_urlhaus.log')
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

FEED_URL = "https://urlhaus.abuse.ch/downloads/csv_online/"
SOURCE = "URLhaus"

def obtener_datos_urlhaus(url=FEED_URL, intentos=3, delay=5):
    """
    Descarga el feed CSV de URLhaus y lo retorna como lista de líneas válidas.
    Registra logs de cada intento, éxito o fallo.
    """
    for intento in range(1, intentos + 1):
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            contenido = response.text
            # Filtrar líneas útiles
            lineas = [l for l in contenido.splitlines() if not l.startswith('#') and l.strip()]
            logger.info(f"[{SOURCE}] Descargadas {len(lineas)-1} URLs en el intento {intento}.")
            return lineas
        except requests.exceptions.RequestException as e:
            logger.warning(f"[{SOURCE}] Error en el intento {intento}: {e}")
            if intento < intentos:
                logger.info(f"[{SOURCE}] Esperando {delay} segundos antes del siguiente intento")
                time.sleep(delay)
            else:
                logger.error(f"[{SOURCE}] No se pudo descargar el feed tras {intentos} intentos.")
                return []

def procesar_datos(lineas):
    """
    Procesa las líneas CSV en un DataFrame limpio, deduplicado y normalizado.
    """
    logger.info(f"[{SOURCE}] Procesando {len(lineas)-1} líneas válidas del feed.")
    cabecera = lineas[0]
    datos = [l for l in lineas[1:] if l.count(';') == cabecera.count(';')]
    csv_limpio = "\n".join([cabecera] + datos)
    df = pd.read_csv(StringIO(csv_limpio), sep=';', encoding='utf-8')
    df.columns = df.columns.str.strip()
    antes = len(df)
    df = df.drop_duplicates(subset='url')
    logger.info(f"[{SOURCE}] Duplicados eliminados: {antes - len(df)}")
    logger.info(f"[{SOURCE}] Total URLs únicas tras limpieza: {len(df)}")
    df['fuente'] = SOURCE
    df['fecha_hora_recoleccion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df

def guardar_datos(df):
    """
    Guarda el DataFrame limpio y loguea el resultado.
    """
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'urlhaus_online_{fecha_hora}.csv'
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)
    df.to_csv(ruta_archivo, index=False)
    logger.info(f"[{SOURCE}] Guardados {len(df)} registros en {ruta_archivo}.")

if __name__ == "__main__":
    lineas = obtener_datos_urlhaus()
    if lineas:
        df = procesar_datos(lineas)
        guardar_datos(df)
        print(f"[INFO] Guardados {len(df)} registros procesados en {DATA_DIR}")
    else:
        print("[WARNING] No se pudo descargar el feed de URLhaus. Ver logs para más información.")
