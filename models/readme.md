# 📂 Carpeta `models/`

Esta carpeta contiene los **modelos entrenados** y sus **metadatos**. Los archivos permiten reproducir y utilizar directamente el prototipo sin necesidad de reentrenar.

## Archivos incluidos

- **`logreg_phishing_final.joblib`**  
  Modelo final del prototipo (pipeline completo: preprocesamiento + Regresión Logística).  
  Entrenado con todas las URLs seleccionadas y usando un **umbral de decisión = 0.425**.  
  → Este es el **modelo oficial** para replicar resultados.

- **`best_pipeline_logreg.joblib`**  
  Pipeline intermedio con la mejor regresión logística encontrada en validaciones.  
  No incorpora el ajuste de umbral final.

- **`best_pipeline_metadata.json`**  
  Archivo auxiliar con información del modelo (`best_pipeline_logreg`):  
  - Fecha de entrenamiento  
  - Hiperparámetros usados  
  - Métricas de validación  

## Uso en Python

Cargar un modelo y predecir:

```python
import joblib
import pandas as pd

# Cargar el modelo final
model = joblib.load("models/logreg_phishing_final.joblib")

# Ejemplo con un dataset
X_test = pd.read_csv("dataset/dataset_prototipo.csv").drop("label", axis=1)
y_pred = model.predict(X_test)

print(y_pred[:10])
