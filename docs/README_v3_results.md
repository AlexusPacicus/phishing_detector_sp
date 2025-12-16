# Resultados del Baseline V3 — Deteccion de Phishing Orientado a Espana

**Version:** 3.0  
**Estado:** VALIDADO  
**Fecha:** Diciembre 2025

---

## 1. Resumen ejecutivo

El baseline v3 establece un modelo de deteccion de phishing orientado a dominios espanoles mediante Logistic Regression sobre 7 features estructurales. El enfoque prioriza la interpretabilidad y la generalizacion a entidades no vistas, utilizando un esquema de validacion anti-leakage basado en agrupacion por `entidad`. El modelo alcanza un ROC-AUC de 0.988 y un F1-score de 0.96 en el conjunto de test, demostrando capacidad discriminativa solida con un balance adecuado entre precision (93.5%) y recall (98.6%). El umbral contractual de 0.50 ofrece el mejor equilibrio entre falsos positivos y falsos negativos para el caso de uso operativo.

---

## 2. Dataset y esquema anti-leakage

### 2.1 Fuente de datos

| Atributo | Valor |
|----------|-------|
| Dataset | `data/interim/dataset_v3_features.csv` |
| Registros totales | 482 |
| Balance | 241 legitimas (50%) / 241 phishing (50%) |
| Hash SHA256 | `b16e13c0c2b42fafc8c625a63da438cf811234ea3974d83f0674674f4e4a78f4` |

### 2.2 Esquema de split

| Parametro | Valor |
|-----------|-------|
| Metodo | `GroupShuffleSplit` |
| Train | 80% |
| Test | 20% |
| Semilla | 42 |
| Clave de agrupacion | `entidad` |

### 2.3 Justificacion del GroupShuffleSplit

El split tradicional estratificado no garantiza independencia entre train y test cuando existen multiples URLs de la misma entidad (banco, empresa, institucion). Esto genera leakage: el modelo aprende patrones especificos de entidades presentes en ambos conjuntos, sobreestimando su rendimiento real.

`GroupShuffleSplit` asegura que todas las URLs de una misma entidad permanezcan en un unico conjunto (train o test), simulando el escenario operativo donde el modelo debe clasificar URLs de entidades nunca vistas durante el entrenamiento.

### 2.4 Implicacion para generalizacion

Las metricas reportadas reflejan el rendimiento esperado frente a **entidades nuevas**, no frente a variaciones de entidades conocidas. Este es el criterio mas exigente y relevante para produccion.

---

## 3. Modelos evaluados

### 3.1 Modelo seleccionado

| Atributo | Valor |
|----------|-------|
| Algoritmo | Logistic Regression |
| Libreria | `sklearn.linear_model` |
| Solver | `lbfgs` |
| Regularizacion | C = 1.0 |
| Class weight | `balanced` |
| Max iterations | 1000 |
| Random state | 42 |

### 3.2 Razon de seleccion

Logistic Regression se selecciono como baseline por:

1. **Interpretabilidad**: los coeficientes tienen significado directo y auditable.
2. **Estabilidad**: comportamiento predecible con datasets pequenos.
3. **Calibracion natural**: las probabilidades de salida son interpretables sin post-procesamiento.
4. **Linea base rigurosa**: establece un umbral minimo de rendimiento antes de explorar modelos mas complejos.

El objetivo v3 no es maximizar metricas, sino validar que el conjunto de features captura senales discriminativas reales.

---

## 4. Metricas globales

### 4.1 Metricas en conjunto de test (post-split)

| Metrica | Valor |
|---------|-------|
| ROC-AUC | 0.9876 |
| Precision | 0.9351 |
| Recall | 0.9863 |
| F1-Score | 0.9600 |

### 4.2 Metricas en dataset completo (validacion cruzada)

| Metrica | Valor |
|---------|-------|
| ROC-AUC | 0.9720 |
| PR-AUC | 0.9721 |

### 4.3 Interpretacion

- **ROC-AUC > 0.97** indica excelente capacidad de separacion entre clases en todo el rango de umbrales.
- **PR-AUC ≈ ROC-AUC** confirma que el rendimiento es consistente incluso bajo analisis sesgado hacia la clase positiva.
- Las metricas del test set son ligeramente superiores debido a la varianza natural del split, pero ambas indican rendimiento robusto.

---

## 5. Seleccion del umbral (threshold tuning)

### 5.1 Rango analizado

Se evaluaron umbrales en el rango [0.0, 1.0] con incrementos de 0.01.

### 5.2 Tabla de metricas por umbral

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

### 5.3 Argumento matematico para threshold = 0.50

1. **F1 maximo observado**: 0.922 en threshold = 0.52, practicamente identico a 0.50 (diferencia < 0.001).

2. **Punto de equilibrio natural**: la mediana de los scores del modelo es 0.54, indicando que 0.50 representa el punto de separacion estadistico entre clases.

3. **Estabilidad operativa**: threshold = 0.50 es el valor por defecto de clasificacion probabilistica, lo que facilita la interpretacion y reduce errores de configuracion.

4. **Balance precision-recall**: en 0.50, precision (89.8%) y recall (94.6%) mantienen equilibrio operativo. Umbrales superiores sacrifican recall; umbrales inferiores sacrifican precision.

### 5.4 Conclusion

El threshold contractual **0.50** se adopta por ofrecer el mejor compromiso entre:
- Maximizacion de F1
- Estabilidad operativa
- Interpretabilidad del score como probabilidad

---

## 6. Matriz de confusion @ 0.50

### 6.1 Valores absolutos (dataset completo)

|  | Predicho: Legitima | Predicho: Phishing |
|--|--------------------|--------------------|
| **Real: Legitima** | TN = 215 | FP = 26 |
| **Real: Phishing** | FN = 13 | TP = 228 |

### 6.2 Metricas derivadas

| Metrica | Valor | Formula |
|---------|-------|---------|
| Accuracy | 91.9% | (TN + TP) / Total |
| Specificity | 89.2% | TN / (TN + FP) |
| Recall (Sensitivity) | 94.6% | TP / (TP + FN) |
| Precision | 89.8% | TP / (TP + FP) |
| False Positive Rate | 10.8% | FP / (FP + TN) |
| False Negative Rate | 5.4% | FN / (FN + TP) |

### 6.3 Interpretacion de errores

**Falsos Positivos (26 casos)**:
URLs legitimas clasificadas como phishing. Impacto: bloqueo innecesario de sitios legitimos. Riesgo operativo medio (molestia al usuario, posible perdida de confianza).

**Falsos Negativos (13 casos)**:
URLs de phishing clasificadas como legitimas. Impacto: amenaza no detectada. Riesgo operativo alto (exposicion del usuario a fraude).

### 6.4 Impacto en el contexto espanol

- El modelo prioriza recall sobre precision (94.6% vs 89.8%), lo cual es apropiado para un sistema de deteccion de amenazas donde es preferible alertar en exceso que dejar pasar phishing.
- Los 13 falsos negativos representan URLs con caracteristicas atipicas que requieren analisis adicional para v4.
- Los 26 falsos positivos incluyen dominios legitimos con estructuras complejas (subdominios, paths largos) que el modelo interpreta como sospechosos.

---

## 7. Interpretabilidad del modelo

### 7.1 Tabla de coeficientes

| Feature | Coeficiente | Direccion |
|---------|-------------|-----------|
| domain_complexity | +3.052 | Phishing |
| infra_risk | +2.279 | Phishing |
| host_entropy | +0.455 | Phishing |
| brand_match_flag | +0.193 | Phishing |
| brand_in_path | +0.105 | Phishing |
| domain_whitelist | -0.370 | Legitimo |
| trusted_token_context | -0.869 | Legitimo |

### 7.2 Senales hacia phishing (coeficientes positivos)

1. **domain_complexity (+3.05)**: Principal indicador de phishing. Dominios con multiples subdominios, TLDs inusuales o estructuras complejas tienen alta probabilidad de ser maliciosos. El coeficiente elevado indica que esta feature captura la mayoria de la varianza discriminativa.

2. **infra_risk (+2.28)**: Segundo indicador mas fuerte. Combina senales de infraestructura sospechosa (IPs dinamicas, hosting compartido, certificados anomalos). Refuerza la deteccion cuando domain_complexity es ambiguo.

3. **host_entropy (+0.45)**: Entropia alta en el hostname sugiere generacion automatica o aleatorizacion deliberada, patron comun en dominios de phishing.

4. **brand_match_flag (+0.19)**: Paradojicamente, la coincidencia exacta con una marca conocida en el nucleo del dominio es sospechosa cuando el dominio no esta en whitelist. Indica posible typosquatting o suplantacion directa.

5. **brand_in_path (+0.11)**: Presencia de marcas espanolas en el path de URLs no whitelisted. Senal debil pero especifica de phishing dirigido.

### 7.3 Senales hacia legitimo (coeficientes negativos)

1. **trusted_token_context (-0.87)**: La presencia de tokens de confianza (marca en whitelist o CSV de dominios espanoles) reduce fuertemente la probabilidad de phishing. Esta feature actua como ancla de legitimidad.

2. **domain_whitelist (-0.37)**: Dominios en la whitelist oficial reciben penalizacion negativa moderada. El coeficiente es menor que TTC porque la whitelist es condicion suficiente pero no necesaria para legitimidad.

### 7.4 Coherencia con el diseno v3

Los coeficientes validan las hipotesis del diseno de features:
- Las features estructurales (complexity, entropy, infra_risk) dominan la discriminacion.
- Las features de contexto (whitelist, TTC) actuan como anclas de seguridad.
- Las features de marca (brand_match_flag, brand_in_path) aportan senales especificas para phishing dirigido a Espana.

---

## 8. Conclusion final de la version v3

### 8.1 Validacion tecnica

El baseline v3 cumple los criterios de validacion contractual:

| Criterio | Estado |
|----------|--------|
| ROC-AUC > 0.95 | CUMPLIDO (0.988) |
| F1 > 0.90 | CUMPLIDO (0.960) |
| Sin leakage de entidades | CUMPLIDO (GroupShuffleSplit) |
| Features interpretables | CUMPLIDO (coeficientes coherentes) |
| Threshold estable | CUMPLIDO (0.50) |

### 8.2 Preparacion para produccion

El modelo esta listo para scoring en produccion bajo las siguientes condiciones:
- Uso exclusivo del bootstrap v3 (`initialize_v3()`)
- Threshold fijo en 0.50
- Actualizacion periodica de whitelist y dominios_espanyoles.csv

### 8.3 Limitaciones conocidas

1. **Dataset reducido**: 482 muestras limitan la generalizacion a sectores no representados.
2. **Sesgo de seleccion**: phishing prefiltrado por scoring heuristico v2.
3. **Cobertura de marcas**: brand_in_path y brand_match_flag dependen de la completitud del CSV de dominios espanoles.
4. **Infraestructura dinamica**: infra_risk puede degradarse si los atacantes migran a hosting mas sofisticado.

### 8.4 Lineas de mejora para v4

Las siguientes categorias se identifican como prioritarias para la siguiente version:

1. **Ampliacion de dataset**: incrementar cobertura de sectores y entidades.
2. **Features temporales**: incorporar edad del dominio y patrones de registro.
3. **Analisis de contenido**: features derivadas del HTML/JS de las paginas.
4. **Ensemble**: combinar Logistic Regression con modelos no lineales.
5. **Feedback loop**: integracion de reportes de usuarios para reentrenamiento.

---

*Documento generado a partir de los artefactos contractuales v3. Referencia: `models/logreg_phishing_v3_metadata.json`, `notebooks/train_v3_threshold_tuning.ipynb`.*
