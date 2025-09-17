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
