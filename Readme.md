# Proyecto Detección de Phishing en URLs (Contexto Español)

## Descripción

Este proyecto tiene como objetivo desarrollar un modelo de detección de phishing centrado en URLs legítimas y maliciosas del contexto español, con especial atención a los bancos nacionales. Se compone de un pipeline que incluye la recolección, limpieza, clasificación y modelado de datos para mejorar la precisión y relevancia en la identificación de amenazas.

## Estructura del proyecto

- `/data`: Contiene los datasets originales (`raw`) y procesados (`processed`), incluyendo el CSV maestro de URLs legítimas.
- `/notebooks`: Notebooks con análisis exploratorio, limpieza, y modelado.
- `/models`: Modelos entrenados y scripts para inferencia.
- `/scripts`: Scripts auxiliares para procesamiento y extracción de datos.
- `/docs`: Documentación del proyecto, incluyendo la tabla maestra de empresas objetivo y documentación por sector.
- `README.md`: Documento principal de presentación y guía del proyecto.

## Dataset

El dataset se ha construido combinando URLs legítimas obtenidas mediante navegación manual en webs oficiales de bancos y herramientas OSINT como DNSDumpster y crt.sh. Se ha validado manualmente la accesibilidad y relevancia de las URLs, y se han normalizado las categorías para facilitar el análisis.

Para detalles completos, consultar el [README de la carpeta `data`](./data/Readme_data.md).

## Metodología

- Extracción de URLs y subdominios mediante scraping manual y herramientas OSINT.
- Validación manual para eliminar datos irrelevantes o falsos positivos.
- Clasificación y normalización de tipos de página con un glosario estandarizado.
- Creación de features y entrenamiento de modelos para la detección de phishing.

## Documentación complementaria

- [Tabla maestra de empresas objetivo por sector](docs/tabla_maestra_empresas.md)

---

## Estado actual y próximos pasos

- **Actualmente:** recopilando y documentando URLs legítimas de banca española mediante scraping básico.
- **Pendiente:** aplicar limpieza de datos, crawling y técnicas anti-bot para ampliar el dataset.
- **Próximo objetivo:** ampliar la recolección de datos a otros sectores clave (SaaS, retail, logística, sector público, etc.) siguiendo la tabla maestra de empresas objetivo.
