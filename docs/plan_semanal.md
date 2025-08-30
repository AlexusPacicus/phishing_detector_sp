# Plan semanal (del miércoles al domingo)

## ✅ Miércoles
🎯 Objetivo: dejar el dataset listo  
- [ ] Revisar notebooks de scraping → anotar en `docs/backlog_scraping.md` qué dataset está limpio y cuál no  
- [ ] Unificar phishing + legítimas en un CSV  
- [ ] Guardar dataset en `data/processed/urls_dataset.csv`  
- [ ] Candidatura 1 → registrar en `docs/candidaturas.md`  
- [ ] 30 min Python: funciones puras para limpiar/normalizar URLs  

---

## ✅ Jueves
🎯 Objetivo: feature engineering básico  
- [ ] Crear `features_urls.ipynb`  
- [ ] Implementar 6 features mínimas: longitud, nº guiones, nº subdominios, “@” en URL, nº parámetros, longitud dominio  
- [ ] Exportar dataset con features a `data/features/urls_features.csv`  
- [ ] 30 min Python: práctica con `lambda` y `map` en URLs  

---

## ✅ Viernes
🎯 Objetivo: primer modelo entrenado  
- [ ] Entrenar modelo (RandomForest y XGBoost)  
- [ ] Generar métricas: accuracy, precision, recall, F1, matriz de confusión  
- [ ] Documentar resultados en `phishing_detector.ipynb`  
- [ ] Candidatura 2 → registrar en `docs/candidaturas.md`  
- [ ] 30 min Python: repaso de `sklearn`  

---

## ✅ Sábado
🎯 Objetivo: documentación y presentación  
- [ ] Completar README del repo con apartado **“Prototipo v1”**  
- [ ] Añadir gráficas de distribución de features y matriz de confusión al notebook  
- [ ] Dejar claros los **límites actuales** (dataset desbalanceado, scraping básico, sin Selenium)  
- [ ] 30 min Python: práctica con `matplotlib`  

---

## ✅ Domingo
🎯 Objetivo: cierre de sprint semanal  
- [ ] Revisión de todo lo hecho → actualizar checklist en `docs/plan_semana.md`  
- [ ] Escribir reflexión en `docs/progreso.md`: qué salió bien, qué bloqueó, próximos pasos  
- [ ] Descanso activo: repaso ligero del bootcamp o vídeos cortos  
