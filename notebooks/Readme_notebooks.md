# Notebooks

Esta carpeta contiene los notebooks usados en el desarrollo del proyecto de detección de phishing en diferentes sectores 

- `phishing_detector.ipynb`: Notebook principal, incluye el pipeline completo de análisis y modelado.
- `filtrado_empresas_es.ipynb`: Descarga y filtrado de URLs de empresas españolas.
- `filtrado.ipynb`: Análisis exploratorio de datos, visualizaciones y estadísticas.
- `scraping_url_leg.ipynb`: Scraping básico de URLs legítimas de banca (sin limpieza ni crawling, en desarrollo).
- `scraping_saas.ipynb`: Scraping básico de URLs legítimas de servicios SaaS, cloud y correo electrónico.
- `scraping_secundarios.ipynb`: Pruebas de scraping en otros sectores (en desarrollo).

## Estado actual

- Los notebooks de scraping implementan scraping básico (home/login) tanto sobre banca como sobre SaaS/cloud/correo.
- No se ha realizado limpieza avanzada, crawling profundo, uso de palabras clave ni Selenium en ninguna de las fases iniciales.
- El scraping básico ha demostrado ser eficaz solo en webs con muchas rutas internas públicas (ej: Box, Slack), pero insuficiente para la mayoría de grandes servicios SaaS/cloud y bancos modernos.
- Está documentado un importante desbalance en la cantidad de URLs obtenidas por empresa/sector.

## Limitaciones actuales

- **Scraping básico**: Muchas webs presentan estructuras minimalistas o requieren JavaScript/interacción, lo que limita la extracción de URLs útiles solo con requests+BeautifulSoup.
- **Dataset español**: El dataset "español" se ha generado filtrando el dataset global de PhishTank por coincidencias en `.es` y nombres de empresas. Esto no asegura campañas 100% dirigidas a España, y pueden existir falsos positivos.
- No se ha realizado aún filtrado por palabras clave relevantes (login, signin, recover, etc.) ni deduplicado avanzado.
- Los notebooks de scraping de otros sectores distintos a banca/SaaS están en desarrollo.

## Próximos pasos

- Implementar crawling profundo y pruebas con Selenium en servicios con baja cobertura de URLs o bloqueo anti-bot.
- Aplicar limpieza y filtrado de URLs por relevancia para phishing.
- Mejorar la cobertura y diversidad de empresas en los datasets.
- Documentar y comparar el impacto de cada técnica en los resultados.

---

*Este README se actualizará conforme avance el proyecto y se completen nuevas fases de scraping y análisis.*
“Se revisaron manualmente 2.694 URLs candidatas. Se completó la columna ruido_estimado y se dividió el dataset en campañas válidas para España vs. descartadas LatAm/PT/otros. Este proceso está documentado en docs/limpieza_manual_pt.md.”