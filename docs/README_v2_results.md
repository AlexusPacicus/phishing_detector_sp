# Cierre del Prototipo V2 — Deteccion de Phishing Orientado a Espana

**Version:** 2.0 (cierre)  
**Estado:** CERRADO  
**Fecha:** Diciembre 2025

---

## 1. Resumen ejecutivo

El prototipo historico V2 fue la primera version funcional del sistema de deteccion de phishing orientado a Espana. Se baso en curacion manual de URLs, scoring heuristico (v1 y v2), y features V2 (hoy obsoletas), con un umbral operativo historico **0.425**.

El cierre final del prototipo V2 se realiza aplicando el extractor contractual actual **FEATURES_V3** sobre el dataset V2. Este cierre tiene tres objetivos:

1. Consolidar el cierre con un extractor estable, interpretable y sin redundancias.
2. Dejar una linea base comparable con versiones futuras.
3. Establecer explicitamente la transicion V2 → FEATURES_V3 como contrato oficial.

Este cierre constituye una **revalidacion retrospectiva** del dataset V2 bajo el extractor contractual actual: se conserva el dataset oficial y se reextraen las 7 features V3 para medir el rendimiento final del prototipo bajo el contrato vigente.

---

## 2. Dataset del prototipo V2

### 2.1 Identificacion (dataset oficial)

| Atributo | Valor |
|----------|-------|
| Ruta oficial | `data/clean/dataset_v2.csv` |
| Registros totales | 482 |
| Balance | 241 legitimas (50%) / 241 phishing (50%) |
| Hash SHA256 dataset V2 | `135cf41a8b5be74cba6a9a130fcf15f0dbdae2d41e158bd1eef3dbd16f07e6f7` |

### 2.2 Origen del dataset

| Clase | Fuente |
|-------|--------|
| Phishing | Feeds publicos (PhishTank, OpenPhish, PhishStats) filtrados por scoring V2 + curacion manual |
| Legitimas | Dominios espanoles oficiales (Tranco, whitelist manual) + curacion manual |

### 2.3 Nota sobre reextraccion con FEATURES_V3

El cierre final V2 **no modifica** `data/clean/dataset_v2.csv`. El cierre consiste en reextraer features con el vector contractual **FEATURES_V3** para generar `data/interim/dataset_v3_features.csv` (13 columnas: 6 base + 7 features V3) y poder medir el cierre con el extractor vigente.

---

## 3. Extractor de features usado en el cierre

### 3.1 FEATURES_V3 (vector contractual)

El cierre del prototipo V2 utiliza exactamente este vector contractual:

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

### 3.2 Justificacion tecnica

| Razon | Descripcion |
|-------|-------------|
| Estabilidad | El extractor V3 elimina features redundantes y dependencias fragiles del prototipo V2 |
| Interpretabilidad | Cada feature tiene significado auditable y coeficientes directos |
| Contractualidad | FEATURES_V3 pasa a ser el contrato oficial para scoring y entrenamiento |

### 3.3 Declaracion explicita de obsolescencia (features V2)

Las features historicas V2 quedan declaradas **OBSOLETAS**. El cierre V2 se mide exclusivamente con **FEATURES_V3** como extractor contractual vigente.

### 3.4 Relacion FEATURES_V2 → FEATURES_V3 (aclaracion contractual)

| Aspecto | FEATURES_V2 (historico) | FEATURES_V3 (contractual) |
|---------|-------------------------|---------------------------|
| Estado | **OBSOLETO** | Vigente |
| Uso en cierre V2 | No | Si |
| Uso en entrenamientos futuros | **Prohibido** | Obligatorio |

**Contexto**: FEATURES_V2 formaba parte del pipeline historico del prototipo V2. Durante el desarrollo se identificaron features rotas o inestables (`suspicious_path_token`, `param_count`, `token_density`, logica anterior de `brand_path`).

**Correccion estructural**: FEATURES_V3 no es una nueva version funcional del proyecto. Es la correccion estructural obligatoria del extractor V2: elimina features redundantes e inestables, consolida la logica de marcas, y fija un vector de 7 features interpretables.

**Consecuencias contractuales**:
1. Ningun entrenamiento final del prototipo V2 utiliza FEATURES_V2.
2. El cierre retrospectivo del prototipo V2 aplica exclusivamente FEATURES_V3.
3. El artefacto `models/logreg_phishing_v3.joblib` es el modelo final del prototipo V2 (el sufijo `_v3` indica el extractor usado, no una version funcional distinta).

---

## 4. Modelo final del prototipo V2

### 4.1 Algoritmo (Logistic Regression)

| Atributo | Valor |
|----------|-------|
| Algoritmo | Logistic Regression |
| Libreria | `sklearn.linear_model` |
| Solver | `lbfgs` |
| Regularizacion | C = 1.0 |
| Class weight | `balanced` |
| Max iterations | 1000 |
| Random state | 42 |

### 4.2 Artefactos oficiales del cierre V2 (sin renombrado)

| Atributo | Valor |
|----------|-------|
| Modelo serializado | `models/logreg_phishing_v3.joblib` |
| Metadata | `models/logreg_phishing_v3_metadata.json` |

Este artefacto es simultaneamente el **modelo final del prototipo V2** y el **baseline entrenado con FEATURES_V3**, aplicado sobre `data/clean/dataset_v2.csv`.

Artefactos historicos obsoletos (experimentos V2 previos; no representan el cierre):
- `models/best_pipeline_logreg.joblib`
- `models/logreg_phishing_final.joblib`

### 4.3 Umbral (threshold) contractual 0.50 (justificado)

| Atributo | Valor |
|----------|-------|
| Threshold | 0.50 |
| Justificacion | Maximiza F1 (0.921), equilibrio precision/recall, estabilidad operativa |

El prototipo historico V2 utilizaba un umbral operativo **0.425**. Tras reextraer con FEATURES_V3 y recalcular la tabla de metricas por umbral, el cierre del prototipo V2 fija **0.50** como threshold contractual por maximizar F1 y estabilidad operativa.

### 4.4 Esquema de validacion (GroupShuffleSplit) y aclaracion historica

| Parametro | Valor |
|-----------|-------|
| Metodo | `GroupShuffleSplit` |
| Train | 80% |
| Test | 20% |
| Semilla | 42 |
| Clave de agrupacion | `entidad` |

GroupShuffleSplit por entidad no formaba parte del prototipo V2. Se adopta unicamente para el cierre final tras aplicar FEATURES_V3, con el fin de eliminar leakage por entidad y evaluar generalizacion real.

### 4.5 Hash del dataset de features (cierre V2 con FEATURES_V3)

Hash SHA256 dataset de features (`data/interim/dataset_v3_features.csv`): `b16e13c0c2b42fafc8c625a63da438cf811234ea3974d83f0674674f4e4a78f4`

---

## 5. Resultados del cierre

### 5.1 Metricas test

| Metrica | Valor |
|---------|-------|
| ROC-AUC | 0.9876 |
| Precision | 0.9351 |
| Recall | 0.9863 |
| F1-Score | 0.9600 |

### 5.2 Metricas dataset completo

| Metrica | Valor |
|---------|-------|
| ROC-AUC | 0.9720 |
| PR-AUC | 0.9721 |

### 5.3 Tabla de thresholds

| Threshold | Precision | Recall | F1 | FP Rate |
|-----------|-----------|--------|-----|---------|
| 0.10 | 0.748 | 0.996 | 0.854 | 0.336 |
| 0.20 | 0.784 | 0.992 | 0.875 | 0.274 |
| 0.30 | 0.807 | 0.992 | 0.890 | 0.237 |
| 0.40 | 0.824 | 0.992 | 0.900 | 0.212 |
| **0.50** | **0.898** | **0.946** | **0.921** | **0.108** |
| 0.60 | 0.913 | 0.830 | 0.870 | 0.079 |
| 0.70 | 0.921 | 0.776 | 0.842 | 0.066 |
| 0.80 | 0.988 | 0.656 | 0.788 | 0.008 |
| 0.90 | 0.994 | 0.572 | 0.727 | 0.004 |

### 5.4 Matriz de confusion

|  | Predicho: Legitima | Predicho: Phishing |
|--|--------------------|--------------------|
| **Real: Legitima** | TN = 215 | FP = 26 |
| **Real: Phishing** | FN = 13 | TP = 228 |

### 5.5 Metricas derivadas

| Metrica | Valor |
|---------|-------|
| Accuracy | 91.9% |
| Specificity | 89.2% |
| Recall (Sensitivity) | 94.6% |
| Precision | 89.8% |
| False Positive Rate | 10.8% |
| False Negative Rate | 5.4% |

### 5.6 Coeficientes

| Feature | Coeficiente | Direccion |
|---------|-------------|-----------|
| domain_complexity | +3.052 | Phishing |
| infra_risk | +2.279 | Phishing |
| host_entropy | +0.455 | Phishing |
| brand_match_flag | +0.193 | Phishing |
| brand_in_path | +0.105 | Phishing |
| domain_whitelist | -0.370 | Legitimo |
| trusted_token_context | -0.869 | Legitimo |

### 5.7 Interpretacion

**Senales hacia phishing**:
- `domain_complexity` (+3.05): principal discriminador. Dominios con estructuras complejas son altamente sospechosos.
- `infra_risk` (+2.28): infraestructura anomala (hosting gratuito, IPs dinamicas) refuerza deteccion.
- `host_entropy` (+0.45): hostnames aleatorios sugieren generacion automatica.
- `brand_match_flag` (+0.19): coincidencia con marca conocida fuera de whitelist indica suplantacion.
- `brand_in_path` (+0.11): presencia de marcas espanolas en path de URLs sospechosas.

**Senales hacia legitimo**:
- `trusted_token_context` (-0.87): tokens de confianza reducen probabilidad de phishing.
- `domain_whitelist` (-0.37): pertenencia a whitelist oficial es indicador de legitimidad.

---

## 6. Limitaciones reconocidas del prototipo V2

| Limitacion | Descripcion |
|------------|-------------|
| Dataset pequeno | 482 muestras limitan generalizacion a sectores no representados |
| Sesgo sectorial | Banca y logistica dominan; otros sectores (telecomunicaciones, energia) subrepresentados |
| Origen del phishing | URLs prefiltradas por scoring V2, posible sesgo hacia patrones detectables por reglas |
| Sin validacion externa | No se ha probado en distribucion real de produccion |
| Whitelist limitada | Cobertura de dominios espanoles puede ser incompleta |

---

## 7. Estado contractual del prototipo V2

| Declaracion | Estado |
|-------------|--------|
| V2 | **CERRADO** |
| Dataset V2 | Congelado |
| Features V2 | **OBSOLETAS Y PROHIBIDAS** |
| FEATURES_V3 | Contrato oficial |
| Modelo final | `models/logreg_phishing_v3.joblib` |
| Threshold contractual | 0.50 |

**Declaracion contractual**: FEATURES_V2 quedan obsoletas y **prohibidas** para cualquier entrenamiento o scoring futuro. Solo FEATURES_V3 es valido.

Camino a V3:
- Nuevos datos (no modifican `data/clean/dataset_v2.csv`).
- FEATURES_V3 como linea base contractual para comparabilidad.
- Validacion por entidad y umbral contractual como referencia.

---

*Documento final de cierre del prototipo V2. Referencias: `data/clean/dataset_v2.csv`, `data/interim/dataset_v3_metadata.json`, `models/logreg_phishing_v3_metadata.json`, `docs/scoring/scoring.md`.*

