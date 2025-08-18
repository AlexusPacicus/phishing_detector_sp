import requests
import zipfile
import io
import pandas as pd
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data', 'raw', 'phishing')
LOGS_DIR = os.path.join(BASE_DIR, '..', 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

log_file = os.path.join(LOGS_DIR, 'recolector_urlhaus.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[RotatingFileHandler(log_file, maxBytes=200000, backupCount=5)]
)

def recoger_urlhaus():
    try:
        FEED_URL = "https://urlhaus.abuse.ch/downloads/csv/"
        logging.info(f"Descargando datos de {FEED_URL}")
        response = requests.get(FEED_URL)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            nombre_csv = z.namelist()[0]
            with z.open(nombre_csv) as csvfile:
                # Deja que pandas procese todo el CSV (no limpies nada tú)
                df = pd.read_csv(
                    csvfile,
                    comment="#",
                    engine="python",
                    on_bad_lines="skip"
                )
        
        if 'url' not in df.columns:
            logging.error(f"Columnas encontradas: {df.columns}")
            logging.error("No se encontró la columna 'url' en el CSV descargado.")
            return

        urls = df['url'].dropna().unique()
        fecha = datetime.now().strftime('%Y-%m-%d_%H-%M')
        output_file = os.path.join(DATA_DIR, f"urlhaus_{fecha}.txt")
        with open(output_file, 'w') as f:
            for url in urls:
                f.write(f"{url}\n")
        logging.info(f"Guardadas {len(urls)} URLs en {output_file}")

    except Exception as e:
        logging.error(f"Error en la recogida de URLhaus: {e}")

if __name__ == '__main__':
    recoger_urlhaus()
