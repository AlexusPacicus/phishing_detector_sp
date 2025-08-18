"""
Script de automatización para la descarga, limpieza y almacenamiento del feed de URLs de [NOMBRE_DEL_FEED].

- Descarga el feed actualizado desde la fuente oficial ([URL]).
- Realiza varios intentos de descarga (con logs y reintentos en caso de error).
- Procesa el resultado para filtrar líneas inválidas, deduplicar y añadir metadata.
- Guarda el resultado como archivo CSV con nombre único por fecha y hora en `data/raw/phishing/`.
- Toda la actividad y errores quedan registrados en un log rotativo en `logs/recolector_[feed].log`.

Autor: Alexis Zapico Fernández
Fecha: [AAAA-MM-DD]
"""

import requests
import pandas as pd
from datetime import datetime
import os
import logging
import time
from logging.handlers import RotatingFileHandler
from io import StringIO

# --- Configuración de rutas y logging ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

FEED_URL = "[URL_DEL_FEED]"           # Cambia aquí la URL
SOURCE = "[NOMBRE_DEL_FEED]"          # Ej: "OpenPhish", "NewFeed"
LOG_FILE = os.path.join(LOGS_DIR, f'recolector_{SOURCE.lower()}.log')

handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    logger.addHandler(handler)
else:
    logger.handlers.clear()
    logger.addHandler(handler)

def obtener_datos_feed(url=FEED_URL, intentos=3, delay=5):
    """
    Descarga el feed con reintentos y logging.
    Devuelve el contenido crudo (texto o JSON) si tiene éxito.
    """
    for intento in range(1, intentos + 1):
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            logger.info(f"[{SOURCE}] Descarga completada en el intento {intento}.")
            return response.text  # O .json() si el feed es JSON
        except requests.exceptions.RequestException as e:
            logger.warning(f"[{SOURCE}] Error en el intento {intento}: {e}")
            if intento < intentos:
                logger.info(f"[{SOURCE}] Esperando {delay} segundos antes del siguiente intento")
                time.sleep(delay)
            else:
                logger.error(f"[{SOURCE}] No se pudo descargar el feed tras {intentos} intentos.")
                return None

def procesar_datos(contenido):
    """
    Procesa el feed descargado:
    - (Personaliza aquí según el formato del feed: CSV, JSON, TXT...)
    - Elimina duplicados, añade metadata, etc.
    Retorna un DataFrame limpio.
    """
    if not contenido:
        logger.warning(f"[{SOURCE}] No hay contenido para procesar.")
        return pd.DataFrame()

    # EJEMPLO para un CSV donde la cabecera puede estar precedida de comentarios:
    lineas = contenido.splitlines()
    for idx, linea in enumerate(lineas):
        if 'url' in linea and 'id' in linea:
            cabecera_idx = idx
            break
    else:
        logger.error(f"[{SOURCE}] No se encontró la cabecera en el feed.")
        return pd.DataFrame()

    cabecera = lineas[cabecera_idx]
    datos = [l for l in lineas[cabecera_idx+1:] if l.strip() and not l.startswith('#')]
    csv_limpio = "\n".join([cabecera] + datos)

    try:
        df = pd.read_csv(
            StringIO(csv_limpio),
            sep=',',  # Cambia a ';' si el feed lo necesita
            encoding='utf-8',
            engine="python",
            on_bad_lines="skip"
        )
    except Exception as e:
        logger.error(f"[{SOURCE}] Error leyendo el feed: {e}")
        return pd.DataFrame()

    df.columns = df.columns.str.strip()
    if 'url' not in df.columns:
        logger.error(f"[{SOURCE}] No se encontró la columna 'url' en el feed. Columnas encontradas: {df.columns}")
        return pd.DataFrame()

    antes = len(df)
    df = df.drop_duplicates(subset='url')
    logger.info(f"[{SOURCE}] Duplicados eliminados: {antes - len(df)}")
    logger.info(f"[{SOURCE}] Total URLs únicas tras limpieza: {len(df)}")
    df['fuente'] = SOURCE
    df['fecha_hora_recoleccion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return df

def guardar_datos(df):
    """
    Guarda el DataFrame limpio como CSV con nombre único por timestamp.
    """
    if df.empty:
        logger.warning(f"[{SOURCE}] El DataFrame está vacío. No se guardará archivo.")
        return
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'{SOURCE.lower()}_online_{fecha_hora}.csv'
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)
    df.to_csv(ruta_archivo, index=False)
    logger.info(f"[{SOURCE}] Guardados {len(df)} registros en {ruta_archivo}.")

if __name__ == "__main__":
    contenido = obtener_datos_feed()
    if contenido:
        try:
            df = procesar_datos(contenido)
            guardar_datos(df)
            print(f"[INFO] Guardados {len(df)} registros procesados en {DATA_DIR}")
        except Exception as e:
            logger.error(f"[{SOURCE}] Error procesando datos: {e}")
            print(f"[ERROR] No se pudieron procesar los datos. Revisa el log.")
    else:
        print(f"[WARNING] No se pudo descargar el feed de {SOURCE}. Ver logs para más información.")
