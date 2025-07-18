# Scripts

Esta carpeta contiene scripts auxiliares para las distintas fases del proyecto de detección de phishing.  


## Descripción de cada script

- **filtrado_url_es.py**  
  Filtra el dataset general de PhishTank (`../data/raw/phishtank_urls.csv`) para dejar solo URLs que contienen palabras clave asociadas a empresas españolas. Guarda el resultado en `../data/raw/phishtank_es.csv`.

- **explorar_ds.py**  
  Carga el dataset original y muestra información básica: primeras filas, columnas y dimensiones. Útil para inspección rápida del CSV original antes de procesarlo.

- **muestra_urls_es.py**  
  Muestra por pantalla las primeras URLs del dataset filtrado de empresas españolas (`../data/raw/phishtank_es.csv`). Es útil como comprobación tras el filtrado.

- **scrapping.py**  
  Script básico de prueba para hacer scraping de la web de PhishTank (actualmente solo obtiene y muestra el título de la página). No realiza scraping real de los datos, pero puede servir como punto de partida para ampliar la funcionalidad.
