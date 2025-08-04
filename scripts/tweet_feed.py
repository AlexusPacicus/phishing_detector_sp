import os
import pandas as pd
from git import Repo
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone

# Configuración logger rotatorio
LOGS_DIR = './logs'
os.makedirs(LOGS_DIR, exist_ok=True)
log_file = os.path.join(LOGS_DIR, 'update_tweetfeed.log')

logger = logging.getLogger('update_tweetfeed')
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def update_repo(repo_url, local_path):
    if not os.path.exists(local_path):
        logger.info("Clonando repositorio...")
        Repo.clone_from(repo_url, local_path)
        logger.info("Repositorio clonado con éxito")
    else:
        logger.info("Repositorio ya clonado, actualizando...")
        repo = Repo(local_path)
        origin = repo.remotes.origin
        origin.pull()
        logger.info("Repositorio actualizado con éxito")

def procesar_csv_local(csv_path):
    logger.info(f"Leyendo CSV local: {csv_path}")
    df = pd.read_csv(csv_path, header=None)
    logger.info(f"Filas leídas: {len(df)}")

    df_urls = df[df[2] == 'url']
    logger.info(f"URLs filtradas: {len(df_urls)}")

    df_clean = df_urls.drop_duplicates(subset=[3]).copy()
    logger.info(f"URLs únicas después de deduplicar: {len(df_clean)}")

    df_clean.loc[:, 'processed_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    return df_clean

def guardar_datos(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    filename = f"phishing_urls_year_{timestamp}.csv"
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False, header=False)
    logger.info(f"Datos guardados en: {output_path}")
    return output_path

def main():
    REPO_URL = 'https://github.com/0xDanielLopez/TweetFeed.git'
    LOCAL_PATH = './TweetFeed'
    OUTPUT_DIR = './phishing-detector/data/raw/phishing'

    logger.info("Inicio del proceso update_tweetfeed")
    update_repo(REPO_URL, LOCAL_PATH)

    csv_path = os.path.join(LOCAL_PATH, 'year.csv')
    df_clean = procesar_csv_local(csv_path)
    guardar_datos(df_clean, OUTPUT_DIR)
    logger.info("Proceso completado correctamente")

if __name__ == "__main__":
    main()
