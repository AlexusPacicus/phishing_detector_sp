"""
Script de automatización para la descarga, limpieza y almacenamiento del feed de URLs de OpenPhish.

- Descarga el feed actualizado de URLs de phishing desde el recurso público de OpenPhish (formato TXT, lista de URLs).
- Realiza varios intentos de descarga (con logs y reintentos en caso de error).
- Procesa los datos para filtrar líneas inválidas, deduplicar y añadir metadata.
- Guarda el resultado como archivo CSV con nombre único por fecha y hora en `data/raw/phishing/`.
- Toda la actividad y errores quedan registrados en un log rotativo en `logs/recolector_openphish.log`.

Autor: Alexis Zapico Fernández
Fecha: 29/07/2025
"""

# Importación de librerías necesarias para scraping, procesado y logging
import requests                              # Para peticiones HTTP
import pandas as pd                          # Para manipulación y limpieza de datos tabulares
from datetime import datetime                # Para timestamps en los nombres y metadata
import os                                    # Para gestión de rutas y carpetas
import logging                               # Para registrar logs de ejecución y errores
import time                                  # Para retardos entre reintentos
from logging.handlers import RotatingFileHandler # Para logs rotativos por tamaño

# --- Configuración de rutas y logging ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Calcula la raíz del proyecto
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')            # Carpeta para los CSV procesados
LOGS_DIR = os.path.join(BASE_DIR, 'logs')                               # Carpeta para los logs
os.makedirs(DATA_DIR, exist_ok=True)                                    # Crea la carpeta de datos si no existe
os.makedirs(LOGS_DIR, exist_ok=True)                                    # Crea la carpeta de logs si no existe

FEED_URL = "https://openphish.com/feed.txt"                             # URL del feed de OpenPhish
SOURCE = "OpenPhish"                                                    # Nombre de la fuente
LOG_FILE = os.path.join(LOGS_DIR, f'recolector_{SOURCE.lower()}.log')   # Ruta del archivo de log específico

# Configuración del logger rotativo (máximo 5MB por archivo, hasta 3 backups)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Formato del log
handler.setFormatter(formatter)                                             # Asigna el formato al handler

logger = logging.getLogger()        # Obtiene el logger raíz
logger.setLevel(logging.INFO)       # Define el nivel de logs a INFO
if not logger.hasHandlers():        # Añade el handler solo si no existe (evita duplicados)
    logger.addHandler(handler)
else:
    logger.handlers.clear()
    logger.addHandler(handler)

def obtener_datos_feed(url=FEED_URL, intentos=3, delay=5):
    """
    Descarga el feed TXT de OpenPhish con reintentos y logging.
    Devuelve el contenido crudo (texto) si tiene éxito.
    """
    for intento in range(1, intentos + 1):                   # Controla los reintentos de descarga
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)          # Realiza la petición HTTP con un timeout de 30s
            response.raise_for_status()                       # Lanza excepción si hay error HTTP
            logger.info(f"[{SOURCE}] Descarga completada en el intento {intento}.")
            return response.text                              # Devuelve el texto plano descargado (lista de URLs)
        except requests.exceptions.RequestException as e:     # Captura errores de red o HTTP
            logger.warning(f"[{SOURCE}] Error en el intento {intento}: {e}")
            if intento < intentos:                           # Si quedan reintentos...
                logger.info(f"[{SOURCE}] Esperando {delay} segundos antes del siguiente intento")
                time.sleep(delay)                             # Espera antes del próximo intento
            else:                                            # Si es el último intento y falla, registra error grave
                logger.error(f"[{SOURCE}] No se pudo descargar el feed tras {intentos} intentos.")
                return None

def procesar_datos(contenido):
    """
    Procesa el TXT crudo de OpenPhish:
    - Filtra líneas vacías y limpia espacios
    - Deduplica por 'url'
    - Añade metadata
    Retorna un DataFrame limpio.
    """
    if not contenido:
        logger.warning(f"[{SOURCE}] No hay contenido para procesar.")
        return pd.DataFrame()                                 # Retorna DataFrame vacío si no hay datos

    lineas = [l.strip() for l in contenido.splitlines() if l.strip()]  # Filtra líneas vacías y limpia espacios
    if not lineas:
        logger.warning(f"[{SOURCE}] No se encontraron líneas válidas en el feed.")
        return pd.DataFrame()                                 # Retorna DataFrame vacío si solo había líneas vacías

    df = pd.DataFrame(lineas, columns=['url'])                # Crea el DataFrame con una columna 'url'
    antes = len(df)
    df = df.drop_duplicates(subset='url')                     # Elimina filas duplicadas por columna 'url'
    logger.info(f"[{SOURCE}] Duplicados eliminados: {antes - len(df)}")
    logger.info(f"[{SOURCE}] Total URLs únicas tras limpieza: {len(df)}")
    df['fuente'] = SOURCE                                     # Añade columna fuente para trazabilidad
    df['fecha_hora_recoleccion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp de la recolección
    return df

def guardar_datos(df):
    """
    Guarda el DataFrame limpio como CSV con nombre único por timestamp.
    """
    if df.empty:
        logger.warning(f"[{SOURCE}] El DataFrame está vacío. No se guardará archivo.")  # No guarda si no hay datos
        return
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")           # Timestamp para nombre único
    nombre_archivo = f'{SOURCE.lower()}_online_{fecha_hora}.csv'    # Nombre del archivo (por fuente y fecha)
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)           # Ruta final
    df.to_csv(ruta_archivo, index=False)                            # Guarda el DataFrame en CSV, sin índice extra
    logger.info(f"[{SOURCE}] Guardados {len(df)} registros en {ruta_archivo}.")

# --- Bloque principal: solo ejecuta si es el script principal ---

if __name__ == "__main__":
    contenido = obtener_datos_feed()                           # Descarga el feed (con reintentos y logs)
    if contenido:
        try:
            df = procesar_datos(contenido)                    # Procesa y limpia los datos recibidos
            guardar_datos(df)                                 # Guarda el DataFrame como CSV
            print(f"[INFO] Guardados {len(df)} registros procesados en {DATA_DIR}")
        except Exception as e:
            logger.error(f"[{SOURCE}] Error procesando datos: {e}")
            print(f"[ERROR] No se pudieron procesar los datos. Revisa el log.")
    else:
        print(f"[WARNING] No se pudo descargar el feed de {SOURCE}. Ver logs para más información.")
