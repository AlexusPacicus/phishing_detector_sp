# ESTRUCTURA DE LA CARPETA "DATA


Aquí se encuentran los archivos de datos usados en el proyecto.
Se subdivide en "processed", los datos ya procesados, y "raw", datos originales.

## Raw 
Contiene los archivos **originales**, sin modificar.

## Processed

Archivos de datos ya filtrados, fusionados o transformados, listos para su análisis o entrenamiento.
# Carpeta DATA

En esta carpeta se almacenan los datos usados en el proyecto de detección de phishing adaptado al contexto español.

## Estructura

- **raw/**  
  Contiene los archivos originales, sin modificar.  
  Incluye datasets descargados, datos recolectados por scraping o recopilación manual.

- **processed/**  
  Archivos de datos ya filtrados, fusionados o transformados, listos para su análisis, preprocesamiento o entrenamiento.

## Datasets principales

### Dataset Phishing  
- Fuente: Base global de PhishTank filtrada para el contexto español mediante palabras clave específicas.  
- Fecha de obtención: [poner fecha]  
- Nota: Puede contener falsos positivos o URLs no exclusivamente españolas, dada la naturaleza de la base global.

### URLs legítimas  
- Fuentes: Principales bancos españoles (BBVA, Santander, CaixaBank, Sabadell).  
- Métodos:  
  - Navegación manual para identificar rutas y subdominios relevantes (login, acceso, recuperación, banca online).  
  - Búsquedas avanzadas en Google (Google Dorks) para ampliar con URLs sensibles indexadas públicamente.  
- Criterios de inclusión:  
  - Solo rutas y subdominios relacionados con accesos críticos y procesos de autenticación.  
  - Exclusión de rutas genéricas o informativas (ejemplo: /contacto, /tarjetas).  
- Limitaciones:  
  - Restricciones y caídas temporales de herramientas OSINT (crt.sh, VirusTotal).  
  - Uso de CDN y protecciones que limitan la visibilidad de subdominios legítimos.

## Archivos en esta carpeta

- `raw/phishing_global.csv`  
- `raw/urls_legitimas_bancos.csv`  
- `processed/phishing_clean.csv`  
- `processed/legit_urls_filtered.csv`  

## Próximos pasos

- Continuar ampliando el dataset legítimo con más sectores y fuentes.  
- Integrar los datos en el pipeline de preprocesamiento y modelado.  
- Documentar el proceso completo en notebooks y scripts.


```python

```
