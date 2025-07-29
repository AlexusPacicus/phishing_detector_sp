# 🛠️ Scripts de Automatización y Scraping de Feeds de Phishing

Esta carpeta contiene los **scripts profesionales** que automatizan la recolección, limpieza y almacenamiento de feeds de phishing para su análisis posterior.

---

## 📜 ¿Qué hace cada script?

- **aut_phishtank.py**  
  Descarga, limpia y guarda el feed CSV de PhishTank, deduplicando y añadiendo metadatos para trazabilidad.

- **aut_haus.py**  
  Automatiza la descarga y limpieza del feed CSV de URLhaus, filtrando líneas corruptas y asegurando un dataset usable.

- **automatizacion_openphish.py**  
  Descarga el feed TXT de OpenPhish (lista de URLs), lo transforma en CSV, elimina duplicados y añade metadatos.

- **aut_phishstats.py**  
  Procesa el feed JSON de PhishStats, normaliza, deduplica y enriquece los datos con metadatos.

---

## ⚙️ Lógica común de los scripts

- **Descarga el feed** correspondiente desde la fuente oficial.
- **Limpia y valida** la estructura de los datos (eliminando duplicados, líneas corruptas o vacías).
- **Añade columnas estándar**:  
  - `fuente`: nombre de la fuente.
  - `fecha_hora_recoleccion`: timestamp de la ejecución.
- **Guarda el resultado** en la carpeta `../data/raw/phishing/` con nombre único por fecha y hora.
- **Registra toda la actividad** (intentos, éxitos, errores) en un archivo rotativo de logs en `../logs/`.

---

## 🚦 Ejecución

Lanza cualquier script desde la terminal, dentro de la carpeta `/scripts`:

```bash
python aut_phishtank.py
python aut_haus.py
python automatizacion_openphish.py
python aut_phishstats.py
