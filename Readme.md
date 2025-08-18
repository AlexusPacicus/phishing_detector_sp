# Proyecto Detección de Phishing en URLs (Contexto Español)

## Descripción

Este proyecto busca desarrollar un modelo robusto para detectar phishing en URLs, centrado en el contexto español, con énfasis en banca y sectores críticos. El pipeline cubre desde la recolección y limpieza de datos, hasta el entrenamiento y despliegue del modelo.

## Estructura del proyecto

- data/
    - raw/
        - legitimas/<sector>/*.csv # fuentes crudas legítimas por sector
        - phishing/<fuente>/*.csv # fuentes crudas de feeds phishing
    - processed/
- notebooks/limpieza/legitimas/.ipynb # plantilla + notebooks por sector
- scripts/.py # utilidades y runners
- results/* # informes/figuras/métricas (no datasets)
- models/* # checkpoints/modelos
docs/daily_log.md # log de ejecuciones


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
