# Notebooks

Esta carpeta contiene los notebooks usados en el desarrollo del proyecto.

- `phishing_detector.ipynb`: Notebook principal, incluye el pipeline completo de análisis y modelado.
- `filtrado_empresas_es.ipynb`: Descarga y filtrado de URLs de empresas españolas.
- `filtrado.ipynb`: Análisis exploratorio de datos, visualizaciones y estadísticas.
- `scraping_url_leg.ipynb`: Scraping básico de URLs legítimas de banca (sin limpieza ni crawling, en desarrollo).
- `scraping_secundarios.ipynb`: Pruebas de scraping en otros sectores (en desarrollo).

## Estado actual

- Actualmente los notebooks de scraping solo implementan scraping básico sobre banca, sin limpieza, crawling ni uso de Selenium.
- En próximas fases se añadirá procesamiento avanzado y automatización del scraping para otros sectores.

## Limitaciones del dataset filtrado

El dataset “español” se ha generado filtrando el dataset global de PhishTank por coincidencias en palabras clave relacionadas con empresas españolas (por ejemplo, `.es`, nombres de bancos, etc.).

- Esto no asegura que todas las URLs sean campañas realmente dirigidas a España, ya que pueden incluir campañas internacionales o falsos positivos.
- Una revisión manual de una muestra aleatoria sugiere que aproximadamente X% parecen efectivamente adaptadas al contexto español.
- Este enfoque es una primera aproximación dada la falta de datasets públicos específicamente españoles, pero debe mejorarse en futuras versiones.
