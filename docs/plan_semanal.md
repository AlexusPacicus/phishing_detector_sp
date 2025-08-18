Lunes — Plan, repo y 2 CV
 Planificar: copia este checklist a docs/plan_semana.md y ajusta horas. X
 Revisión de notebooks: anota huecos y prioridades en docs/backlog_scraping.md.
 Automatización en línea (estructura):
 Crear .github/workflows/collect.yml (esqueleto con 1 job).
 Convertir 1 script a CLI con --outdir (recomiendo openphish.py).
 Añadir automation/README.md explicando cron de Actions y outputs.
 CVs: enviar 2 candidaturas (apunta empresa/enlace/estado en docs/candidaturas.md).
 Práctica Python 30–45’ (strings y funciones puras sobre URLs).
DoD: workflow subido y ejecutado manualmente una vez; dos CV con enlace.
Artefactos: collect.yml, openphish.py con CLI, automation/README.md, docs/candidaturas.md.


Martes — Ingesta + Limpieza/Deduplicado
 Actions: ejecutar workflow; validar que genera archivos con timestamp en raw/phishing/openphish/.
 Limpieza: notebook/py que:
 Deduplica por URL normalizada.
 Filtra por keywords (login|signin|secure|account|verify|update).
 Guarda processed/phishing_provisional.csv.
 Conteos: log rápido (nº total, nº tras filtros, % HTTPS).
 Práctica Python 45’ (regex y normalización de URLs).
DoD: processed/phishing_provisional.csv con ≥60 URLs únicas.
Artefactos: notebooks/limpieza_phishing.ipynb (o scripts/limpieza_phishing.py), gráfico/tabla simple, commit.


Miércoles — Baseline prototipo (fase 1)
 Features simples (mínimo 8):
longitud URL, nº /, nº ., nº -, si contiene IP, nº dígitos, si usa https, longitud dominio.
 Modelo: RandomForest o XGBoost con split estratificado.
 Métricas: Accuracy, Precision, Recall, F1. Guarda semillas y versión de datos.
 Informe corto en docs/baseline.md (qué features, qué modelo, resultados, limitaciones).
 Práctica Python 45’ (listas/dicts para contadores).
DoD: models/baseline.pkl + docs/baseline.md con métricas reproducibles.
Artefactos: notebooks/baseline.ipynb o scripts/train_baseline.py, models/, docs/baseline.md.


Jueves — Automatización en línea (completa) + 2 CV
 Añadir fuentes a Actions: PhishTank (+ token), PhishStats (si aplica).
 Sanity check en workflow (falla si filas < 20).
 Artifacts o rama data (elige uno y documéntalo).
 Alerta básica: si falla, que el job marque error (ya con el sanity).
 CVs: enviar 2 más (total 4).
 Práctica Python 45’ (crawler básico: requests+queue limitado a 1 dominio).
DoD: workflow programado “cada 12h” con ≥2 fuentes y sanity check activo; 4 CV enviados.
Artefactos: workflow actualizado, captura/log del run en docs/automation_runs.md.


Viernes — Consolidación + LinkedIn
 Revisión de semana: limpia carpetas, nombres consistentes, .gitignore.
 Dataset provisional: merge de phishing (limpio) + legítimas (muestra) para baseline.
 Post LinkedIn: 6–8 líneas sobre:
Ingesta automatizada, 100 URLs alcanzadas (o progreso), baseline y próximos pasos.
 Práctica Python 45’ (pandas: groupby por dominio, top 10).
DoD: todo comiteado, post publicado, processed/ actualizado.
Artefactos: docs/changelog_semana.md, link al post en docs/social.md.


Sábado — Paper/Reporte + Microproyecto
 Leer 1 (ENISA/INCIBE o paper phishing ML).
 Anotar 2–3 acciones aplicables (ej: nuevas keywords, feature de entropía del host, etc.).
 Microproyecto: notebook que compare distribución de longitudes y nº de / entre phishing vs legítimas (gráfico simple).
 Práctica Python 60’ (matplotlib básico).
DoD: docs/paper_semana.md (1 página) + notebook con 2 gráficos y comentario.
Artefactos: docs/paper_semana.md, notebooks/analisis_distribuciones.ipynb.


Domingo — 1 CV + Plan siguiente semana
 Enviar 1 CV (total 5).
 Escribir plan de la semana siguiente (foco: crawling/Selenium + features nuevas).
 Revisar issues abiertos y priorizar 5 para el lunes.
DoD: docs/plan_semana_next.md creado + 5/5 CVs.
Artefactos: docs/plan_semana_next.md, actualización de docs/candidaturas.md.
