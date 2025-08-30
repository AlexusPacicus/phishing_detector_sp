# Proyecto Detección de Phishing en URLs (Contexto Español)

## Descripción

Objetivo: construir un pipeline reproducible para detectar phishing a nivel URL en contexto español (.es y marcas locales), con datos reales, documentación clara y trazabilidad para entrevistas técnicas.

## Estructura del proyecto

.
├── data/
│ ├── raw/ # Datos crudos por fuente (NO tocar)
│ ├── clean/ # Datos tras limpieza inicial (por fuente)
│ └── final/ # Datasets listos para modelar (unificados/equilibrados)
├── docs/
│ ├── datasets/ # Fichas por fuente (README por dataset)
│ ├── plan/ # Roadmaps, decisiones, resúmenes
│ └── README_notebooks.md # Índice y estado de notebooks
├── logs/ # Bitácoras de limpiezas/ejecuciones
├── models/ # Modelos/artefactos de entrenamiento
├── notebooks/ # EDA, scraping, limpieza por pasos
├── results/ # Figuras, informes, métricas
├── scripts/ # CLIs: ingest/clean/merge
├── requirements.txt
└── README.md # (este archivo)

## Datasets (estado actual)

PhishTank — limpieza inicial completada → data/clean/phishtank_es.csv (42 URLs)
Ficha: docs/datasets/phishtank.md
Tweetfeed — pendiente de limpieza (objetivo ≈ 58 URLs) para alcanzar ≥ 100 phishing totales
Ficha: docs/datasets/tweetfeed.md
URLhaus / OpenPhish — definidos como fuentes adicionales; integración posterior a Tweetfeed.
Legítimas (ES) — recogida sectorial (banca y críticos) en data/raw/legitimas/<sector>/; limpieza por sector en data/clean/legitimas_<sector>.csv.
Nota de sesgo: filtrar por .es/marca no garantiza campaña exclusivamente española. Se realizará spot‑check manual y documentación de falsos positivos.
## Dataset de URLs legítimas

URLs recogidas manualmente de bancos españoles y otras fuentes relevantes, priorizando rutas de acceso y autenticación, excluyendo secciones irrelevantes.

## Metodología

- Automatización y logging de todo el proceso de scraping y recolección.
- Validación manual y eliminación de falsos positivos.
- Normalización de campos y análisis exploratorio en notebooks.

## Documentación complementaria

- [Estructura detallada de datos y fuentes](data/Readme_data.md)
- [Tabla maestra de empresas objetivo por sector](docs/tabla_maestra_empresas.md)

---

## Estado actual y próximos pasos

- **Actualmente:** automatizando la recogida y documentación de datos de phishing y URLs legítimas.
- **Próximos pasos:** ampliar sectores, fusionar datasets y comenzar el análisis de features y modelado.

---

## Automatización de la recolección de URLs de phishing

Se ha implementado un sistema automatizado para la descarga y procesamiento de feeds de URLs phishing desde el repositorio [TweetFeed](https://github.com/0xDanielLopez/TweetFeed).

### Características principales:

- Clonación y actualización automática del repositorio TweetFeed utilizando GitPython.  
- Procesamiento del archivo `year.csv` para filtrar URLs phishing y eliminar duplicados.  
- Añadido de metadatos con timestamp UTC para cada ejecución.  
- Guardado de los datos procesados en archivos CSV con nombre único por fecha y hora, asegurando histórico.  
- Registro detallado de todas las operaciones mediante logs rotatorios para facilitar auditoría y depuración.  
- Programación mediante `crontab` para ejecutar el script dos veces al día (11:00 y 23:00).

Esta automatización garantiza que el dataset se mantenga actualizado sin intervención manual, mejorando la trazabilidad y la calidad del proyecto.
