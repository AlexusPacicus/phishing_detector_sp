# Proyecto Detección de Phishing en URLs (Contexto Español)

## Descripción

Este proyecto busca desarrollar un modelo robusto para detectar phishing en URLs, centrado en el contexto español, con énfasis en banca y sectores críticos. El pipeline cubre desde la recolección y limpieza de datos, hasta el entrenamiento y despliegue del modelo.

## Estructura del proyecto

- `/data`: Almacena los datos originales (`raw`) y procesados (`processed`). Todos los feeds de phishing (URLhaus, OpenPhish, PhishTank) se recogen, documentan y guardan de forma individual para asegurar trazabilidad y control de calidad.
- `/notebooks`: Análisis, limpieza y modelado.
- `/models`: Modelos entrenados y scripts de inferencia.
- `/scripts`: Automatizaciones para descarga, limpieza y organización de datos.
- `/docs`: Documentación por sectores y fuentes.
- `README.md`: Guía general del proyecto.

## Recolección y gestión de datos de phishing

- **Feeds principales:**  
  - **URLhaus:** Feed `csv_online` (solo URLs activas). No se usa la API por bloqueos a IPs españolas.  
  - **PhishTank:** Dataset global filtrado, guardando fechas, estado online y verificación.
  - **OpenPhish:** Feed gratuito, normalmente solo URLs; si es posible, se añade fecha y tipo de amenaza.
- Todos los datos se almacenan individualmente en `/data/raw/phishing/` para permitir análisis por fuente y máxima transparencia.
- Durante el preprocesado, los datasets se fusionan, deduplican y normalizan, añadiendo siempre una columna `source`.

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
