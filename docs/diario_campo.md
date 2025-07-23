# Bitácora Técnica del Proyecto: Detector de Phishing

---

## 2025-07-20

**Actividad principal:**  
- Inicio de la recolección manual de URLs legítimas de entidades y servicios en sectores especialmente afectados por el phishing en España (banca, SaaS, ecommerce, etc.).
- Investigación y listado de empresas objetivo por sector.
- Primeros scripts/notebooks para scraping básico de las homepages de cada entidad.

**Decisiones y justificación:**  
- Se priorizaron sectores más atacados según informes actuales de ciberseguridad en España.
- Se optó por scraping sencillo para avanzar rápido en la obtención de datos.
- Se decidió crear una estructura clara de carpetas para los datos (`data/raw/legitimas/`).

**Limitaciones detectadas:**  
- El scraping inicial devuelve pocos enlaces útiles en homepages muy minimalistas.
- Algunas webs bloquean el scraping automatizado.

**Problemas encontrados:**  
- Pocos resultados en entidades con páginas muy simples o protegidas.
- Dificultad para extraer URLs desde servicios muy cerrados.

**Próximos pasos:**  
- Buscar fuentes alternativas (listas públicas, crawling más profundo, Selenium…).
- Ampliar la lista de empresas objetivo y sectores.
- Documentar el proceso de obtención y resultados por empresa.

---

## 2025-07-21

**Actividad principal:**  
- Continuación y ampliación de la recolección de URLs legítimas.
- Mejora de los scripts para scraping y almacenamiento de datos.
- Primeras pruebas de organización de los archivos en la estructura de datos.

**Decisiones y justificación:**  
- Se organizó la recolección por sectores y empresas, documentando cantidad y calidad de las URLs por cada una.
- Se decidió guardar los datos crudos y, en paralelo, avanzar en la limpieza básica (eliminación de duplicados, estandarización de formato).

**Limitaciones detectadas:**  
- Persisten dificultades en webs con pocos enlaces o protección antiautomática.
- El volumen de datos legítimos por sector es desigual.

**Problemas encontrados:**  
- Necesidad de depuración manual en algunos casos.
- Scripts no siempre generalizables a todas las empresas/sectores.

**Próximos pasos:**  
- Seguir ampliando el dataset de URLs legítimas.
- Empezar a planificar la limpieza avanzada y estructura definitiva de los datos.
- Documentar todo el proceso para futuras referencias y entrevistas.

---

## 2025-07-22

**Actividad principal:**  
- Organización y documentación inicial de la estrategia de recolección automática de URLs de phishing.
- Definición y creación de la estructura del proyecto en carpetas (`data/`, `docs/`, `notebooks/`, `scripts/`, etc.).
- Creación del documento `estrategia_recoleccion_phishing.md` en `/docs`.

**Decisiones y justificación:**  
- Se decidió documentar toda la estrategia en `/docs` en lugar de saturar el README.
- Se priorizó dejar la estructura de carpetas clara y modular antes de empezar la automatización.
- Se planificó comenzar la automatización con PhishTank como fuente principal.

**Limitaciones detectadas:**  
- Ninguna crítica hoy (fase de organización).

**Problemas encontrados:**  
- Ninguno significativo (trabajo organizativo y de documentación).

**Próximos pasos:**  
- Automatizar la descarga de URLs de phishing.
- Revisar validez y cobertura de las fuentes elegidas.
- Guardar los primeros datos en bruto.

---

## 2025-07-23

**Actividad principal:**  
- Automatización de la descarga de URLs de phishing desde el Community Feed de OpenPhish (`https://openphish.com/feed.txt`).

**Decisiones y justificación:**  
- Se eligió OpenPhish por su facilidad de automatización y frecuencia de actualización (12h).
- Se ha guardado el archivo en formato CSV, en la carpeta `data/raw/phishing/`, con timestamp y columnas mínimas (url, fecha, fuente).
- No se realizó limpieza ni enriquecimiento, solo captura en crudo.

**Limitaciones detectadas:**  
- La mayoría de URLs son de campañas internacionales; no se observa presencia relevante de entidades españolas.
- El feed gratuito no ofrece metadatos adicionales.

**Problemas encontrados:**  
- Caída/indisponibilidad del feed de PhishTank (error SSL 525), documentado y justificado el cambio de fuente.

**Próximos pasos:**  
- Documentar la automatización en el README.
- Programar la recolección automática cada 12 horas (cron o equivalente).
- Investigar y añadir fuentes centradas en phishing a entidades españolas.

---

## Plantilla para nuevas entradas

## AAAA-MM-DD

**Actividad principal:**  

**Decisiones y justificación:**  

**Limitaciones detectadas:**  

**Problemas encontrados:**  

**Próximos pasos:**  

