# README — Inclusión phishing v2

Generado: 2025-10-21T14:50:31.277253Z

## Resumen

- Fuente: `phishing_v2.csv`

- Total filas con inclusion==1 en el origen: 209

- Seleccionadas para `phishing_v2_150.csv`: 150

- Restantes en `phishing_v2_holdout.csv`: 59


## Criterios de inclusión

- Se consideran sólo URLs con `inclusion == 1` (curadas manualmente)

- Orden de preferencia: `ruido` ascendente, `confianza` descendente, `score_total_v2` descendente

- Normalización de sectores y asignación por buckets objetivo

- Si un sector no tiene suficientes candidatos, se rellenó con las mejores URLs restantes


## Objetivos por sector

- Banca: objetivo 50 URLs

- Logística: objetivo 30 URLs

- SaaS: objetivo 15 URLs

- Telecomunicaciones: objetivo 10 URLs

- Cripto: objetivo 10 URLs

- Retail / e-commerce: objetivo 10 URLs

- Administración pública: objetivo 10 URLs

- Energía / Seguros: objetivo 10 URLs

- Genérico / Otros: objetivo 5 URLs


## Distribución final en el archivo seleccionado

- Banca: 75

- Logística: 56

- Genérico / Otros: 18

- Administración pública: 1


## Observaciones

- El dataset original está muy sesgado hacia Banca y Logística. Se cubrieron los huecos con 'Genérico / Otros' y mejores restantes.

- Recomendación: recolectar activamente URLs en SaaS, Telecomunicaciones, Cripto, Retail y Energía/Seguros para futuras versiones.


## Archivos generados

- `phishing_v2_150.csv` — dataset principal v2 (150 URLs)

- `phishing_v2_holdout.csv` — holdout (resto de URLs verificadas)


La validación de inclusión v2 concluye con 0.85 accuracy y 0.93 ROC-AUC.
Se identifican errores concentrados en kits .live y en portales legítimos con rutas /login.
Próxima etapa: revisión de features y reentrenamiento v2.”
