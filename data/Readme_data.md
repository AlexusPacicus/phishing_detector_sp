# ESTRUCTURA DE LA CARPETA "DATA"

Aquí se encuentran los archivos de datos usados en el proyecto.  
Se subdivide en "processed" (los datos ya procesados) y "raw" (datos originales).

## Raw 
Contiene los archivos **originales**, sin modificar.  
Incluye datasets descargados automáticamente (feeds globales y nacionales), datos recolectados por scraping o recopilación manual, y logs de los procesos de descarga.

### 📑 **Fuentes de datos de phishing**

#### **URLhaus**
- **Fuente:** [URLhaus](https://urlhaus.abuse.ch/)
- **Script:** `auto_urlhaus_csv_online.py`
- **Formato:** CSV (`csv_online`), solo URLs activas
- **Columnas extraídas:**
  - `url`: dirección maliciosa
  - `dateadded`: fecha de inclusión
  - `threat`: tipo de amenaza
- **Notas:**
  - Se descarta la API por bloqueos a IPs españolas y el feed completo ZIP por dificultad de procesamiento.
  - El feed ya viene filtrado por URLs activas, lo que facilita el uso.
- **Problemas resueltos:** Bloqueos por IP en la API, formato ZIP inconsistente en el feed completo.

#### **PhishTank**
- **Fuente:** [PhishTank](https://phishtank.org/)
- **Script:** `aut_phishtank.py`
- **Formato:** CSV convertido desde XML o JSON
- **Columnas extraídas:**
  - `url`: dirección sospechosa
  - `submission_time`: fecha de reporte
  - `verified`, `verification_time`: verificación por la comunidad
  - `online`: si la URL sigue activa
  - `target`: objetivo del phishing (si está disponible)
- **Notas:**
  - Se filtra para quedarse solo con URLs `online` y con `verified=True`.
  - Puede haber diferencias en el formato según la versión del feed.
  - **Mejora recomendada:** Renombrar `submission_time` como `dateadded` para homogeneizar con el resto de fuentes.

#### **OpenPhish**
- **Fuente:** [OpenPhish](https://openphish.com/)
- **Script:** `automatizacion_openphish.py`
- **Formato:** TXT (una URL por línea) o CSV en versión premium
- **Columnas extraídas:**
  - `url`: dirección detectada como phishing
  - (opcional) `date`: fecha de detección
  - (opcional) `threat`: tipo de amenaza
- **Notas:**
  - El feed gratuito solo da la URL, sin más metadatos.
  - **Mejora recomendada:** Si solo hay `url`, añade columna `source` con `"OpenPhish"` y la fecha de descarga como `dateadded`.

**Todos los feeds se almacenan individualmente en `/raw/phishing/` para trazabilidad, control de calidad y futura auditoría.**  
En la fase de preprocesado, los datasets son fusionados, deduplicados y normalizados, guardando siempre la columna `source` para saber su origen.

---

## Processed

Archivos de datos ya filtrados, fusionados o transformados, listos para su análisis o entrenamiento.

### **Ejemplo de archivos:**
- `processed/phishing_clean.csv` – dataset combinado, deduplicado y filtrado para entrenamiento del modelo.
- `processed/legit_urls_filtered.csv` – dataset de URLs legítimas, tras limpieza y verificación.

---

## Datasets principales

### Dataset Phishing  
- Fuentes: URLhaus, PhishTank, OpenPhish.
- Métodos: Descarga automática con scripts en `/scripts/`, fusión y limpieza en `/notebooks/`.
- Nota: Para detalles técnicos, consulta el README de cada fuente en `/data/raw/phishing/` (si lo creas).

### URLs legítimas  
- Fuentes: Principales bancos españoles, scraping manual, OSINT.
- Métodos: Navegación manual, Google Dorks, validación manual, exclusión de rutas no relevantes.

---

---
## Cambios recientes y mejoras en la recogida de datos (28/07/2025)

- Añadido control de duplicados (`drop_duplicates(subset='url')`) antes de guardar en todos los scripts de feeds (URLhaus, OpenPhish, PhishTank).
- Mejorado el logging: ahora cada fase (descarga, limpieza, guardado) registra intentos, errores, número de URLs, duplicados eliminados, fuente y ruta de archivos.
- Modularización y docstrings en todas las funciones principales para máxima claridad y mantenibilidad.
- Todos los scripts añaden las columnas `fuente` y `fecha_hora_recoleccion` para trazabilidad completa.
- El script de PhishTank está preparado y documenta errores correctamente, aunque la descarga automática no es posible actualmente por limitaciones de acceso externas.
- Documentación y ejemplos actualizados para reflejar estas mejoras.

## Próximos pasos

- Ampliar el dataset legítimo con más sectores y fuentes.
- Integrar todos los datos en el pipeline de preprocesamiento y modelado.
- Documentar el proceso completo en notebooks y scripts, y mantener trazabilidad de los cambios y decisiones tomadas.

---

*Para más detalles sobre el pipeline y la estructura global, consulta el README principal del proyecto.*
