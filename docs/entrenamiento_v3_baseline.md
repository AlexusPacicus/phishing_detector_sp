# Contrato de Entrenamiento Baseline v3

**Version:** 3.0  
**Estado:** CONTRACTUAL  
**Fecha:** Diciembre 2024

---

## 1. Dataset de entrada

### 1.1 Archivo obligatorio

| Atributo | Valor |
|----------|-------|
| Ruta | `data/interim/dataset_v3_features.csv` |
| Encoding | UTF-8 |
| Separador | `,` |

### 1.2 Exclusiones

| Exclusion | Motivo |
|-----------|--------|
| Artefactos v2 | No compatibles con pipeline v3 |
| Loaders v2 | Reemplazados por loaders v3 |
| Datasets v2 | Schema y features incompatibles |

### 1.3 Columnas esperadas

| Columna | Tipo | Uso |
|---------|------|-----|
| url | string | Identificador |
| label | int | Target |
| sector | string | Metadata |
| entidad | string | Anti-leakage |
| notas | string | Metadata |
| campaign | string | Anti-leakage |
| domain_complexity | float | Feature |
| domain_whitelist | int | Feature |
| trusted_token_context | int | Feature |
| host_entropy | float | Feature |
| infra_risk | float | Feature |
| brand_in_path | int | Feature |
| brand_match_flag | int | Feature |

---

## 2. Vector de features

### 2.1 Features contractuales

```
FEATURES_V3 = [
    "domain_complexity",
    "domain_whitelist",
    "trusted_token_context",
    "host_entropy",
    "infra_risk",
    "brand_in_path",
    "brand_match_flag"
]
```

### 2.2 Restricciones

| Restriccion | Valor |
|-------------|-------|
| Orden | Contractual e inmutable |
| Referencia | `docs/features_v3.md` |
| Features adicionales | Prohibidas |
| Features de v2 | Prohibidas |

---

## 3. Target

| Atributo | Valor |
|----------|-------|
| Columna | `label` |
| Tipo | Binario |
| Valores | 0 (legitima), 1 (phishing) |

---

## 4. Esquema de split y anti-leakage

### 4.1 Tipo de split

| Atributo | Valor |
|----------|-------|
| Metodo | Stratified Train/Test |
| Train | 80% |
| Test | 20% |
| Semilla | 42 |

### 4.2 Regla anti-leakage

**OBLIGATORIO:** URLs de la misma `entidad` o `campaign` no pueden cruzar splits.

| Campo | Aplicacion |
|-------|------------|
| `entidad` | Agrupar por entidad antes de split |
| `campaign` | Agrupar por campaign antes de split |

### 4.3 Implementacion

```
GroupShuffleSplit o equivalente con group_key = entidad
```

Si `campaign` no es null, usar `campaign` como group_key preferente.

---

## 5. Modelo baseline

### 5.1 Algoritmo

| Atributo | Valor |
|----------|-------|
| Modelo | LogisticRegression |
| Libreria | sklearn.linear_model |
| Variantes | Ninguna |

### 5.2 Hiperparametros fijos

| Parametro | Valor |
|-----------|-------|
| solver | lbfgs |
| max_iter | 1000 |
| C | 1.0 |
| class_weight | balanced |
| random_state | 42 |

### 5.3 Umbral

| Atributo | Valor |
|----------|-------|
| Default | 0.5 |
| Recalibracion | Post-entrenamiento |
| Fijacion | En metadata tras evaluacion |

---

## 6. Artefactos de salida

### 6.1 Modelo serializado

| Atributo | Valor |
|----------|-------|
| Ruta | `models/logreg_phishing_v3.joblib` |
| Formato | joblib |
| Contenido | Pipeline o modelo entrenado |

### 6.2 Metadata

| Atributo | Valor |
|----------|-------|
| Ruta | `models/logreg_phishing_v3_metadata.json` |
| Formato | JSON |

### 6.3 Campos obligatorios en metadata

```json
{
    "version": "3.0",
    "model_type": "LogisticRegression",
    "dataset_hash": "<SHA256 de dataset_v3_features.csv>",
    "features": [
        "domain_complexity",
        "domain_whitelist",
        "trusted_token_context",
        "host_entropy",
        "infra_risk",
        "brand_in_path",
        "brand_match_flag"
    ],
    "training_date": "<ISO 8601>",
    "split": {
        "method": "GroupShuffleSplit",
        "train_size": 0.8,
        "test_size": 0.2,
        "random_state": 42,
        "group_key": "entidad"
    },
    "metrics": {
        "precision": <float>,
        "recall": <float>,
        "f1": <float>,
        "roc_auc": <float>
    },
    "threshold": <float>
}
```

---

## 7. Relacion con v2

### 7.1 Separacion contractual

| Elemento v2 | Estado en v3 |
|-------------|--------------|
| Modelos v2 | No se mezclan |
| Whitelists v2 | No se usan |
| Features v2 | No se heredan |
| Scoring v2 | No se aplica |
| Configuraciones v2 | No se reutilizan |

### 7.2 Independencia

El pipeline v3 es autosuficiente. No requiere ni admite dependencias de v2.

---

## 8. Condicion de entrega

### 8.1 Requisitos del documento

| Requisito | Estado |
|-----------|--------|
| Sin TODOs | Cumplido |
| Sin ambiguedades | Cumplido |
| Sin decisiones abiertas | Cumplido |
| Contractual | Cumplido |

### 8.2 Validacion pre-entrenamiento

| Check | Descripcion |
|-------|-------------|
| Dataset existe | `data/interim/dataset_v3_features.csv` presente |
| Schema valido | 13 columnas esperadas |
| Sin NaN en features | `df[FEATURES_V3].isna().sum() == 0` |
| Balance verificado | ~50/50 |

### 8.3 Validacion post-entrenamiento

| Check | Descripcion |
|-------|-------------|
| Modelo guardado | `models/logreg_phishing_v3.joblib` existe |
| Metadata guardada | `models/logreg_phishing_v3_metadata.json` existe |
| Metricas registradas | precision, recall, f1, roc_auc presentes |
| Umbral fijado | threshold en metadata |

---

*Contrato de entrenamiento baseline v3. Inmutable dentro de la version 3.0.*
