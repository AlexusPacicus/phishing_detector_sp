"""
Plantilla de script de scraping automatizado para feeds de phishing/ciberamenazas.

Personaliza:
- FEED_URL: URL del feed.
- SOURCE: Nombre de la fuente (para logs y metadata).
- función procesar_datos(): cómo convertir la respuesta en DataFrame estándar.

El resto del script es común a todos los feeds: rutas, logging, estructura de carpetas, automatización.

Autor: [Tu nombre o user]
Fecha: [aaaa-mm-dd]
"""

import requests
import pandas as pd
from datetime import datetime
import os
import logging
import time
from logging.handlers import RotatingFileHandler
from io import StringIO

# --- CONFIGURACIÓN GENERAL ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Personaliza para cada feed
FEED_URL = "PON_AQUI_LA_URL_DEL_FEED"
SOURCE = "NombreFuente"

# Logging rotativo
log_file = os.path.join(LOGS_DIR, f'recolector_{SOURCE.lower()}.log')
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# --- FUNCIONES PRINCIPALES ---

def obtener_datos_feed(url=FEED_URL, intentos=3, delay=5):
    """
    Descarga el feed (indica si es JSON, CSV o TXT) con reintentos y logging.
    Devuelve el contenido crudo (para ser procesado).
    """
    for intento in range(1, intentos + 1):
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            logger.info(f"[{SOURCE}] Descarga completada en el intento {intento}.")
            return response.content  # Puedes cambiar a response.text si es texto
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
    Procesa el contenido descargado según el tipo de feed.
    Convierte el contenido en un DataFrame con columnas estándar ['url', 'fuente', 'fecha_hora_recoleccion', ...].
    PERSONALIZA esta función para cada fuente.
    """
    # ---- EJEMPLOS DE PARSEADO ----
    # Si el feed es JSON con lista de dicts:
    # data = json.loads(contenido)
    # df = pd.DataFrame(data)
    # Si el feed es CSV (con comentarios):
    # lineas = [l for l in contenido.decode('utf-8').splitlines() if not l.startswith('#') and l.strip()]
    # csv_limpio = "\n".join(lineas)
    # df = pd.read_csv(StringIO(csv_limpio), sep=';', encoding='utf-8')
    # Si el feed es lista de URLs en texto plano:
    # lineas = [l.strip() for l in contenido.decode('utf-8').splitlines() if l.strip()]
    # df = pd.DataFrame(lineas, columns=['url'])
    # ------

    # --- PERSONALIZA DESDE AQUÍ ---
    raise NotImplementedError("Debes personalizar la función 'procesar_datos' según el formato del feed.")
    # --- AÑADE METADATA ---
    # df['fuente'] = SOURCE
    # df['fecha_hora_recoleccion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # df = df.drop_duplicates(subset='url')
    # return df

def guardar_datos(df):
    """
    Guarda el DataFrame como CSV con nombre único.
    """
    if df.empty:
        logger.warning(f"[{SOURCE}] El DataFrame está vacío. No se guardará archivo.")
        return
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f'{SOURCE.lower()}_online_{fecha_hora}.csv'
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)
    df.to_csv(ruta_archivo, index=False)
    logger.info(f"[{SOURCE}] Guardados {len(df)} registros en {ruta_archivo}.")

# --- BLOQUE PRINCIPAL ---
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
