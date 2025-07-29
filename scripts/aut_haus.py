"""
Script de automatización para la descarga, limpieza y almacenamiento del feed de URLs de URLhaus.

- Descarga el CSV actualizado desde el feed público de URLhaus.
- Realiza varios intentos de descarga (con logs y reintentos en caso de error).
- Procesa el archivo para filtrar líneas inválidas, deduplicar, validar estructura y añadir metadata.
- Guarda el resultado como archivo CSV con nombre único por fecha y hora en `data/raw/phishing/`.
- Toda la actividad y errores quedan registrados en un log rotativo en `logs/recolector_urlhaus.log`.

Autor: Alexis Zapico Fernández
Fecha: 29/07/2025
"""

# Importa las librerías estándar necesarias para el scraping y logging
import requests                              # Para realizar la petición HTTP al feed
import pandas as pd                          # Para procesar y limpiar el CSV como DataFrame
from datetime import datetime                # Para gestionar timestamps (nombres y metadata)
import os                                    # Para manejar rutas y crear carpetas
import logging                               # Para registrar logs de ejecución y errores
import time                                  # Para aplicar retardos entre reintentos de descarga
from logging.handlers import RotatingFileHandler  # Para logs rotativos que no crecen sin límite
from io import StringIO                      # Para leer el CSV a partir de un string en memoria

# --- Configuración de rutas y logging ---

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Calcula la raíz del proyecto desde el script
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing')            # Carpeta para los CSV procesados
LOGS_DIR = os.path.join(BASE_DIR, 'logs')                               # Carpeta para los logs del recolector
os.makedirs(DATA_DIR, exist_ok=True)                                    # Crea la carpeta de datos si no existe
os.makedirs(LOGS_DIR, exist_ok=True)                                    # Crea la carpeta de logs si no existe

FEED_URL = "https://urlhaus.abuse.ch/downloads/csv_online/"             # URL del feed de URLhaus
SOURCE = "URLhaus"                                                      # Nombre de la fuente, para metadata y logs
LOG_FILE = os.path.join(LOGS_DIR, f'recolector_{SOURCE.lower()}.log')   # Ruta del archivo de log específico

# Configura el logger rotativo (máximo 5MB por archivo, hasta 3 archivos de backup)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')   # Formato del log (fecha, nivel, mensaje)
handler.setFormatter(formatter)                                             # Asigna el formato al handler

logger = logging.getLogger()          # Obtiene el logger raíz
logger.setLevel(logging.INFO)         # Define el nivel de logs a INFO (ajusta si quieres más detalle)
if not logger.hasHandlers():          # Añade el handler solo si no existe (evita duplicar logs en importaciones)
    logger.addHandler(handler)
else:
    logger.handlers.clear()
    logger.addHandler(handler)

def obtener_datos_feed(url=FEED_URL, intentos=3, delay=5):
    """
    Descarga el feed CSV con reintentos y logging.
    Devuelve el contenido crudo (texto) del feed si tiene éxito.
    """
    for intento in range(1, intentos + 1):                # Bucle para controlar los reintentos de descarga
        try:
            logger.info(f"[{SOURCE}] Intento {intento} de descarga desde {url}")
            response = requests.get(url, timeout=30)       # Realiza la petición HTTP con un timeout de 30s
            response.raise_for_status()                    # Lanza excepción si el servidor devuelve error HTTP
            logger.info(f"[{SOURCE}] Descarga completada en el intento {intento}.")
            return response.text                           # Devuelve el texto plano descargado (CSV)
        except requests.exceptions.RequestException as e:  # Captura errores de red o HTTP
            logger.warning(f"[{SOURCE}] Error en el intento {intento}: {e}")
            if intento < intentos:                        # Si quedan reintentos...
                logger.info(f"[{SOURCE}] Esperando {delay} segundos antes del siguiente intento")
                time.sleep(delay)                          # Espera antes del próximo intento
            else:                                         # Si es el último intento y falla, registra error grave
                logger.error(f"[{SOURCE}] No se pudo descargar el feed tras {intentos} intentos.")
                return None

def procesar_datos(contenido):
    """
    Procesa el CSV crudo del feed de URLhaus (csv_online).
    Encuentra la cabecera real y procesa todas las filas a continuación.
    """
    if not contenido:
        logger.warning(f"[{SOURCE}] No hay contenido para procesar.")
        return pd.DataFrame()

    lineas = contenido.splitlines()  # NO filtres comentarios todavía

    # Busca la línea de cabecera real
    for idx, linea in enumerate(lineas):
        if 'id' in linea and 'url' in linea and 'dateadded' in linea:
            cabecera_idx = idx
            break
    else:
        logger.error(f"[{SOURCE}] No se encontró la cabecera en el CSV")
        return pd.DataFrame()

    cabecera = lineas[cabecera_idx]  # Esta es la línea tipo: id,dateadded,url,...
    datos = [l for l in lineas[cabecera_idx+1:] if l.strip() and not l.startswith('#')]
    csv_limpio = "\n".join([cabecera] + datos)

    try:
        df = pd.read_csv(
            StringIO(csv_limpio),
            sep=',',  # Importante: coma, no punto y coma
            encoding='utf-8',
            engine="python",
            on_bad_lines="skip"
        )
    except Exception as e:
        logger.error(f"[{SOURCE}] Error leyendo el CSV: {e}")
        return pd.DataFrame()

    df.columns = df.columns.str.strip()
    if 'url' not in df.columns:
        logger.error(f"[{SOURCE}] No se encontró la columna 'url' en el CSV descargado. Columnas encontradas: {df.columns}")
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
        logger.warning(f"[{SOURCE}] El DataFrame está vacío. No se guardará archivo.")   # No guarda si no hay datos
        return
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")            # Timestamp para nombre único
    nombre_archivo = f'{SOURCE.lower()}_online_{fecha_hora}.csv'     # Nombre del archivo (por fuente y fecha)
    ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)            # Ruta final
    df.to_csv(ruta_archivo, index=False)                             # Guarda el DataFrame en CSV, sin índice extra
    logger.info(f"[{SOURCE}] Guardados {len(df)} registros en {ruta_archivo}.")

# --- Bloque principal: solo ejecuta si es el script principal ---

if __name__ == "__main__":
    contenido = obtener_datos_feed()                 # Descarga el feed (controla reintentos y logs)
    if contenido:                                   # Si la descarga tuvo éxito...
        try:
            df = procesar_datos(contenido)          # Procesa y limpia los datos
            guardar_datos(df)                       # Guarda el resultado en CSV
            print(f"[INFO] Guardados {len(df)} registros procesados en {DATA_DIR}")
        except Exception as e:
            logger.error(f"[{SOURCE}] Error procesando datos: {e}")
            print(f"[ERROR] No se pudieron procesar los datos. Revisa el log.")
    else:
        print(f"[WARNING] No se pudo descargar el feed de {SOURCE}. Ver logs para más información.")
