"""
Script de automatización para la descarga, limpieza y almacenamiento del feed de URLs de PhishTank.

- Descarga el CSV actualizado de URLs válidas desde el feed público de PhishTank.
- Realiza varios intentos de descarga (con logs y reintentos en caso de error).
- Procesa el archivo para filtrar líneas inválidas, deduplicar, validar estructura y añadir metadata.
- Guarda el resultado como archivo CSV con nombre único por fecha y hora en `data/raw/phishing/`.
- Toda la actividad y errores quedan registrados en un log rotativo en `logs/recolector_phishtank.log`.

Autor: Alexis Zapico Fernández
Fecha: 25/07/2025
"""

# Importación de librerías necesarias para scraping, procesado y logging
import requests                              # Para peticiones HTTP
import pandas as pd                          # Para manipulación y limpieza de datos
from datetime import datetime                # Para timestamps en los nombres y metadata
import os                                    # Para gestión de rutas y carpetas
import logging                               # Para registrar logs de ejecución y errores
import time                                  # Para retardos entre reintentos
from logging.handlers import RotatingFileHandler # Para logs rotativos por tamaño
from io import StringIO                      # Para leer CSV en memoria desde texto

# --- Configuración de rutas y logging ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Calcula la raíz del proyecto
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')            # Carpeta para los CSV procesados
LOGS_DIR = os.path.join(BASE_DIR, 'logs')                               # Carpeta para los logs
os.makedirs(DATA_DIR, exist_ok=True)                                    # Crea la carpeta de datos si no existe
os.makedirs(LOGS_DIR, exist_ok=True)                                    # Crea la carpeta de logs si no existe

FEED_URL = "http://data.phishtank.com/data/online-valid.csv"            # URL del feed CSV de PhishTank
SOURCE = "PhishTank"                                                    # Nombre de la fuente
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
    Descarga el feed CSV de PhishTank con reintentos y logging.
    Devuelve el contenido crudo (texto) si tiene éxito.
    """
    for intento in range(1, intentos + 1):                   # Controla los reintentos de descarga
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)          # Realiza la petición HTTP con un timeout de 30s
            response.raise_for_status()                       # Lanza excepción si hay error HTTP
            logger.info(f"[{SOURCE}] Descarga completada en el intento {intento}.")
            return response.text                              # Devuelve el texto plano descargado (CSV)
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
    Procesa el CSV crudo de PhishTank:
    - Filtra líneas vacías y valida estructura por número de columnas
    - Deduplica por 'url'
    - Añade metadata
    Retorna un DataFrame limpio.
    """
    if not contenido:
        logger.warning(f"[{SOURCE}] No hay contenido para procesar.")
        return pd.DataFrame()                                 # Retorna DataFrame vacío si no hay datos

    lineas = [l for l in contenido.splitlines() if l.strip()] # Filtra líneas vacías
    if not lineas:
        logger.warning(f"[{SOURCE}] No se encontraron líneas válidas en el feed.")
        return pd.DataFrame()                                 # Retorna DataFrame vacío si solo había líneas vacías

    cabecera = lineas[0]                                      # La primera línea es la cabecera del CSV
    # Solo acepta filas que tienen el mismo número de separadores que la cabecera (evita líneas corruptas)
    datos = [l for l in lineas[1:] if l.count(',') == cabecera.count(',')]
    csv_limpio = "\n".join([cabecera] + datos)                # Construye el CSV final como string (cabecera + datos limpios)
    df = pd.read_csv(StringIO(csv_limpio), sep=',', encoding='utf-8')  # Lee el string como CSV usando pandas
    df.columns = df.columns.str.strip()                       # Elimina espacios extra en los nombres de columna
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
