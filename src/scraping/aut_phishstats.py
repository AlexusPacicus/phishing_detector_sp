"""
Script de automatización para la descarga, limpieza y almacenamiento del feed de URLs de PhishStats.

- Descarga el feed actualizado de URLs de phishing desde la API pública de PhishStats (formato JSON).
- Realiza varios intentos de descarga (con logs y reintentos en caso de error).
- Procesa el resultado para filtrar registros inválidos, deduplicar y añadir metadata.
- Guarda el resultado como archivo CSV con nombre único por fecha y hora en `data/raw/phishing/`.
- Toda la actividad y errores quedan registrados en un log rotativo en `logs/recolector_phishstats.log`.

Autor: Alexis Zapico Fernández
Fecha: 27/07/2025
"""

# Importación de librerías estándar necesarias
import requests                               # Para hacer peticiones HTTP
import pandas as pd                           # Para procesar datos tabulares en DataFrame
from datetime import datetime                 # Para manejar fechas y horas (timestamp y nombres de archivo)
import os                                     # Para gestionar rutas y crear carpetas
import logging                                # Para registrar logs de información, advertencias y errores
import time                                   # Para retardos entre reintentos de descarga
from logging.handlers import RotatingFileHandler # Para logs rotativos (archivos de tamaño fijo)

# --- Configuración de rutas y logging ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Calcula la raíz del proyecto
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')            # Carpeta para los CSV procesados
LOGS_DIR = os.path.join(BASE_DIR, 'logs')                               # Carpeta para los logs
os.makedirs(DATA_DIR, exist_ok=True)                                    # Crea la carpeta de datos si no existe
os.makedirs(LOGS_DIR, exist_ok=True)                                    # Crea la carpeta de logs si no existe

FEED_URL = "https://api.phishstats.info/api/phishing?_sort=-id"         # URL de la API de PhishStats (JSON)
SOURCE = "PhishStats"                                                   # Nombre de la fuente
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
    Descarga el feed de PhishStats con reintentos y logging.
    Devuelve la lista de diccionarios JSON del feed si tiene éxito.
    """
    for intento in range(1, intentos + 1):                         # Bucle para controlar los reintentos de descarga
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)               # Realiza la petición HTTP con un timeout de 30s
            response.raise_for_status()                            # Lanza excepción si hay error HTTP
            data = response.json()                                 # Parsea el contenido como JSON
            logger.info(f"[{SOURCE}] Descargados {len(data)} registros en el intento {intento}.")
            return data                                            # Devuelve la lista de registros
        except requests.exceptions.RequestException as e:          # Captura errores de red o HTTP
            logger.warning(f"[{SOURCE}] Error en el intento {intento}: {e}")
            if intento < intentos:                                # Si quedan reintentos...
                logger.info(f"[{SOURCE}] Esperando {delay} segundos antes del siguiente intento")
                time.sleep(delay)                                 # Espera antes del próximo intento
            else:                                                 # Si es el último intento y falla, registra error grave
                logger.error(f"[{SOURCE}] No se pudo descargar el feed tras {intentos} intentos.")
                return None

def procesar_datos(data):
    """
    Procesa la lista de registros JSON de PhishStats:
    - Valida que haya datos
    - Elimina duplicados por 'url'
    - Añade columnas de metadata
    Retorna un DataFrame limpio.
    """
    if not data:
        logger.warning(f"[{SOURCE}] No hay datos para procesar.")
        return pd.DataFrame()                                     # Retorna DataFrame vacío si no hay datos

    df = pd.DataFrame(data)                                       # Convierte la lista de dicts a DataFrame de pandas
    if 'url' not in df.columns:
        logger.error(f"[{SOURCE}] No se encuentra la columna 'url' en los datos recibidos.")
        return pd.DataFrame()                                     # Retorna DataFrame vacío si falta columna clave

    antes = len(df)
    df = df.drop_duplicates(subset='url')                         # Elimina filas duplicadas por columna 'url'
    logger.info(f"[{SOURCE}] Duplicados eliminados: {antes - len(df)}")
    logger.info(f"[{SOURCE}] Total URLs únicas tras limpieza: {len(df)}")
    df['fuente'] = SOURCE                                         # Añade columna fuente para trazabilidad
    df['fecha_hora_recoleccion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Timestamp de la recolección
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
    data = obtener_datos_feed()                              # Descarga la lista de registros (con reintentos y logs)
    if data:
        try:
            df = procesar_datos(data)                        # Procesa y limpia los datos recibidos
            guardar_datos(df)                                # Guarda el DataFrame como CSV
            print(f"[INFO] Guardados {len(df)} registros procesados en {DATA_DIR}")
        except Exception as e:
            logger.error(f"[{SOURCE}] Error procesando datos: {e}")
            print(f"[ERROR] No se pudieron procesar los datos. Revisa el log.")
    else:
        print(f"[WARNING] No se pudo descargar el feed de {SOURCE}. Ver logs para más información.")
