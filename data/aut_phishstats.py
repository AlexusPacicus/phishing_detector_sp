# Automatización de Descarga de URLs de Phishing desde PhishStats

import requests
from datetime import datetime
import os

# Definimos la ruta base y la carpeta donde se almacenarán los datos descargados
BASE_DIR = os.path.abspath('')  # Ruta del directorio actual
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'phishing') # Ruta donde se guardarán los datos en crudo

# Crear la carpeta de destino si no existe (evita errores si la carpeta ya existe)
os.makedirs(DATA_DIR, exist_ok=True)

def descargar_phishstats():
    """
    Descarga las URLs de phishing desde la API de PhishStats y las almacena en un archivo CSV con timestamp.
    No se realiza ningún filtrado; los datos se guardan en bruto.
    """
    # Definir la URL de la API de PhishStats, sin filtros adicionales por ahora
    url = "https://api.phishstats.info/api/phishing?_sort=-id"
    
    try:
        # Realizar la petición HTTP GET a la API
        response = requests.get(url)
        
        # Comprobar que la respuesta fue exitosa (código 200)
        response.raise_for_status()
        
        # Convertir la respuesta a formato JSON (lista de diccionarios)
        data = response.json()
        
        # Generar un nombre de archivo único usando la fecha y hora actual
        fecha = datetime.now().strftime('%Y%m%d_%H%M')  # Formato: AñoMesDía_HoraMinuto
        filename = f"phishstats_{fecha}.csv"            # Nombre del archivo resultante
        
        # Unir la ruta de la carpeta y el nombre del archivo
        path = os.path.join(DATA_DIR, filename)
        
        # Convertir los datos JSON a un DataFrame de pandas
        df = pd.DataFrame(data)
        
        # Guardar el DataFrame como un archivo CSV en la ruta indicada, sin índice adicional
        df.to_csv(path, index=False)
        
        # Mostrar por pantalla el resultado del proceso
        print(f"[INFO] Guardadas {len(df)} URLs en {path}")

    except Exception as e:
        # En caso de cualquier error, mostrar un mensaje y el error encontrado
        print(f"[ERROR] No se pudo descargar o guardar los datos: {e}")

# Ejecutar solo si se lanza como script principal
if __name__ == "__main__":
    descargar_phishstats()
