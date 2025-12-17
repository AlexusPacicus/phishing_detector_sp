
Estado del proyecto:
- Prototipo V2: CERRADO
- Extractor contractual: FEATURES_V3
- FEATURES_V2: OBSOLETO (prohibido)
- No existe un prototipo V3 funcional todavía


# 🛡️ Phishing Detector (Prototipo Español)

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)


## 📌 Contexto  
El phishing es uno de los vectores de ataque más comunes en España, afectando a todo tipo de sectores, siendo la **banca** el más golpeado (concentrando más del 65% de los ataques).  

Este proyecto construye un **pipeline completo** para la detección de URLs maliciosas en el **contexto español**, bajo la premisa de que cuanto más específico sea el dataset, mejores resultados se obtienen.  

---

## 🎯 Objetivo  
Desarrollar un prototipo **reproducible y explicable** de detección de phishing, capaz de:  
- Diferenciar **URLs legítimas** de **URLs de phishing**.  
- Priorizar el **recall** para minimizar falsos negativos.  
- Mantener **trazabilidad completa**: desde los datos crudos hasta el modelo entrenado.  

---

## 🗂️ Estructura del proyecto  

```
phishing-detector/
│
├── data/            # Datos crudos, intermedios y finales
├── limpieza/        # Notebooks + documentación de limpieza
├── features/        # Ingeniería de características + gráficas
├── EDA/             # Análisis exploratorio
├── entrenamiento/   # Entrenamiento del modelo y resultados
├── models/          # Modelos finales exportados (.joblib, .json)
├── scripts/         # Automatización de scraping y feeds
├── logs/            # Logs de ejecución
└── README.md        # Este archivo
```

---

## ⚙️ Instalación  

```bash
git clone https://github.com/AlexusPacicus/phishing-detector.git
cd phishing-detector
pip install -r requirements.txt
```

---

## 🚀 Uso  

1. **Recolectar datos**  
   ```bash
   python scripts/aut_openphish.py
   ```

2. **Limpieza manual / heurística**  
   Ejecutar notebooks en `limpieza/`.

3. **Entrenar modelo**  
   ```bash
   jupyter notebook entrenamiento/entrenamiento_prototipo.ipynb
   ```

4. **Modelo final guardado en**  
   ```
   models/logreg_phishing_final.joblib
   ```

---

## 📊 Resultados  

- **Modelo seleccionado**: Logistic Regression  
- **Umbral óptimo**: `0.425`  
- **Métricas clave (CV promedio, k=5–10):**  
  - Precision ≈ 0.85  
  - Recall ≈ 0.92  
  - ROC-AUC ≈ 0.95  

📈 **Gráficas principales** (en `entrenamiento/img/`):  
- Curva Precision-Recall  
- Matriz de confusión  
- ROC-AUC  
- Importancia de features  

---

## 🧩 Valor del proyecto  

- Pipeline completo y documentado.  
- Dataset curado específicamente para **phishing en España**.  
- Features explicables y fácilmente integrables en un SOC.  
- Preparado para futuras ampliaciones: **SMS, email phishing, integración con SIEM**.  

---

## 📜 Licencia  

Este proyecto se distribuye bajo licencia **MIT**.  

## 🚀 Despliegue con Docker

Este proyecto incluye un `Dockerfile` para levantar la API de forma sencilla en cualquier máquina con Docker instalado.

1. Construir la imagen
Desde la raíz del proyecto:
docker build -t phishing-detector .

2. Ejecutar el contenedor
docker run -p 8000:8000 phishing-detector

3. Acceder a la API
Swagger UI → http://127.0.0.1:8000/docs
Healthcheck → http://127.0.0.1:8000/health
Predicción (POST /predict) → enviar un JSON con la URL a analizar, por ejemplo:
{
  "url": "https://soporte-netflx.com/"
}

4. Ejemplo de respuesta

{
  "label": 1,
  "probability": 0.7517,
  "threshold": 0.425,
  "features": {
    "domain_length": 14,
    "domain_entropy": 3.37,
    "num_params": 0,
    "trusted_path_token": 0,
    "contains_percent": 0,
    "contains_equal": 0,
    "suspicious_path_token": 0,
    "free_hosting": 0,
    "protocol": 1,
    "tld_group": "com"
  }
}


---

### Tests automáticos con Pytest


# 🧪 Tests automáticos

Este proyecto incluye pruebas con **pytest** para verificar:

- Que `extract_features()` devuelve las 10 features esperadas.  
- Que la API responde correctamente en `/health` y `/predict`.  

1. Ejecutar los tests
Desde la raíz del proyecto:
pytest -q

2. Ejemplo de salida esperada
....                                                                     [100%]
4 passed in 1.64s

---

## 🔮 Próximos avances – Fase 3: Inteligencia semántica y detección de ruido

En la siguiente etapa, el proyecto incorporará **análisis vectorial y búsqueda semántica** para reforzar el sistema de scoring y mejorar la calidad del dataset.

### 🎯 Objetivos principales
1. **Representar cada URL como un embedding** → un vector numérico que capta su significado o estructura.
2. **Calcular un centroide español** → el punto medio del espacio vectorial de todas las URLs confirmadas como orientadas a España.
3. **Medir el “ruido semántico”** de cada nueva URL:
   - Se calcula la **similitud del coseno** entre la URL y el centroide español.
   - Cuanto más baja sea la similitud, más alejada está del patrón español y más probable es que sea ruido o irrelevante.
   - Esta medida (`ruido_semantico`) se combinará con el `score_total` actual como señal adicional.
4. **Almacenar los embeddings en PostgreSQL usando `pgvector`**, para permitir:
   - Búsqueda semántica de campañas parecidas.
   - Detección de variantes o clones.
   - Visualización de clusters de phishing por marca o sector.

### 🧩 Ejemplo conceptual
- URLs españolas → agrupadas en torno al centroide.  
- Nueva URL → se mide su distancia (1 - coseno) al centroide.  
- Cuanto mayor la distancia, **más ruido semántico**.  

```text
         ·        (URLs españolas)
       ·   ·
         ⊕  ← Centroide español
          \
           \_·  (URL alejada → alto ruido)



🧭 Próximos pasos – Fase 3 (desde hoy)
1️⃣ Preparar dataset de legítimas v2
Objetivo: disponer de ~150 URLs legítimas nuevas para validación y contrapeso.
Tareas:
Recolectar ~200 candidatas (banca, logística, SaaS, público, retail, cripto…).
Aplicar los gates definidos (is_https=1, sin hosting gratuito, sin /wp-, etc.).
Deduplicar semánticamente (≤95 % similitud).
Seleccionar 150 finales (keep=1) + 15–20 como holdout.
📄 Entregable: data/processed/legitimas_v2_final.csv
📘 Documentar en: docs/legitimas_v2_calidad.md
2️⃣ Validación con el modelo actual (LogReg v1)
Objetivo: medir el rendimiento real con las 209 phishing + 150 legítimas.
Tareas:
Combinar datasets → eval_set_inclusion1.csv.
Extraer features con tu extract_features() actual.
Ejecutar el modelo (logreg_phishing_final.joblib).
Exportar métricas globales y por sector:
precision, recall, F1, matriz de confusión.
Listado de falsos negativos priorizados (falsos_negativos_priorizados.csv).
📄 Entregables:
outputs/inclusion1_eval/predicciones_eval.csv
docs/evaluacion_inclusion1.md
3️⃣ Selección del nuevo bloque de entrenamiento
Objetivo: crear dataset v2 balanceado (≈300–350 URLs).
Reglas:
Incluir phishing con ruido_estimado ≤ 20 y que sean FN o TP en validación.
Capar por entidad (máx. 8–10 por marca).
Añadir las legítimas v2 seleccionadas.
📄 Entregable: data/processed/dataset_entrenamiento_v2.csv
4️⃣ Reentrenamiento de modelo (v2)
Objetivo: entrenar, comparar y calibrar modelos.
Tareas:
Entrenar Logistic Regression, RandomForest y SVC.
Usar GroupKFold (evitar leakage por campaña).
Optimizar umbral: max recall ≥ 0.9, precision ≥ 0.8.
Exportar modelo + metadata.json.
📄 Entregables:
models/logreg_phishing_v2.joblib
docs/entrenamiento_v2.md
5️⃣ Inicio de la Fase 3 – Inteligencia semántica
Objetivo: integrar embeddings y detección de ruido semántico.
Tareas:
Generar embeddings (MiniLM / multilingual-distil).
Calcular centroide español (media de embeddings de campañas confirmadas).
Medir ruido_semantico = 1 − coseno(URL, centroide).
Integrar ruido_semantico al scoring como nueva señal.
📄 Entregables:
notebooks/semantic_noise.ipynb
docs/scoring_v3_plan.md
🧩 Revisión recomendada antes de cerrar cada subfase
✅ Actualizar documentación (docs/…).
✅ Exportar métricas y CSV de salida.
✅ Anotar observaciones en avance_<fecha>.md.
✅ Publicar en LinkedIn los hitos clave (validación, embeddings, etc.).
