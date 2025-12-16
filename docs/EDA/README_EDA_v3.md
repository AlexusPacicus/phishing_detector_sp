# README — EDA v3

**Versión:** 3.0  
**Estado:** CERRADO  
**Fecha:** Diciembre 2024  
**Dataset analizado:** `outputs/dataset_v3_features.csv`  
**Metadata:** `outputs/dataset_v3_metadata.json`

---

## 1. Objetivo del EDA

### 1.1 Qué se pretende validar

| Objetivo | Descripción |
|----------|-------------|
| Coherencia de rangos | Verificar que cada feature respeta sus límites contractuales |
| Separación de clases | Evaluar capacidad discriminativa de cada feature |
| Integridad de datos | Confirmar ausencia de NaN y tipos correctos |
| Identificación de riesgos | Detectar colinealidad, overfitting potencial, baja cobertura |
| Trazabilidad | Validar metadata y checksums |

### 1.2 Qué NO se pretende

| Exclusión | Motivo |
|-----------|--------|
| Optimizar modelo | EDA es diagnóstico, no optimización |
| Ajustar pesos de features | Features v3 son contractuales e inmutables |
| Proponer nuevas features | Fuera del alcance de EDA |
| Modificar umbrales | Decisión de scoring, no de EDA |

---

## 2. Descripción del dataset

### 2.1 Shape y schema

| Atributo | Valor |
|----------|-------|
| Filas | 482 |
| Columnas totales | 13 |
| Columnas base (v2) | 6 |
| Features v3 | 7 |

### 2.2 Schema completo

| Columna | Tipo | Origen |
|---------|------|--------|
| `url` | string | dataset v2 |
| `label` | int | dataset v2 |
| `sector` | string | dataset v2 |
| `entidad` | string | dataset v2 |
| `notas` | string | dataset v2 |
| `campaign` | string | dataset v2 |
| `domain_complexity` | float | FEATURES_V3 |
| `domain_whitelist` | int | FEATURES_V3 |
| `trusted_token_context` | int | FEATURES_V3 |
| `host_entropy` | float | FEATURES_V3 |
| `infra_risk` | float | FEATURES_V3 |
| `brand_in_path` | int | FEATURES_V3 |
| `brand_match_flag` | int | FEATURES_V3 |

### 2.3 Balance de clases

| Clase | Count | Porcentaje |
|-------|-------|------------|
| Legítimas (label=0) | 241 | 50% |
| Phishing (label=1) | 241 | 50% |

Balance perfecto 50/50.

### 2.4 Distribución por sector

| Sector | Total | Legítimas | Phishing | Cobertura |
|--------|-------|-----------|----------|-----------|
| banca | 191 | 98 | 93 | ✓ Completa |
| logistica | 93 | 38 | 55 | ✓ Completa |
| generico | 55 | 0 | 55 | ⚠ Solo phishing |
| saas | 36 | 25 | 11 | ✓ Completa |
| cripto | 22 | 18 | 4 | ✓ Completa |
| publico | 18 | 12 | 6 | ✓ Completa |
| ecommerce | 17 | 17 | 0 | ⚠ Solo legítimas |
| teleco | 13 | 7 | 6 | ✓ Completa |
| energia | 12 | 12 | 0 | ⚠ Solo legítimas |
| streaming | 9 | 4 | 5 | ✓ Completa |
| redessociales | 6 | 5 | 1 | ✓ Completa |
| gaming | 6 | 3 | 3 | ✓ Completa |
| viajes | 2 | 2 | 0 | ⚠ Solo legítimas |
| seguros | 2 | 2 | 0 | ⚠ Solo legítimas |

### 2.5 Nota sobre selección de phishing

**⚠️ Sesgo de selección:** Las URLs de phishing fueron prefiltradas mediante scoring heurístico antes de su inclusión en el dataset. Esto implica:

- El phishing presente ya exhibe patrones detectables por features estructurales.
- Phishing sofisticado o edge cases pueden estar subrepresentados.
- Las métricas de separación pueden ser optimistas respecto a producción.

---

## 3. Validaciones contractuales

### 3.1 Tipos de datos

| Feature | Tipo esperado | Tipo observado | Estado |
|---------|---------------|----------------|--------|
| `domain_complexity` | float64 | float64 | ✓ |
| `domain_whitelist` | int64 | int64 | ✓ |
| `trusted_token_context` | int64 | int64 | ✓ |
| `host_entropy` | float64 | float64 | ✓ |
| `infra_risk` | float64 | float64 | ✓ |
| `brand_in_path` | int64 | int64 | ✓ |
| `brand_match_flag` | int64 | int64 | ✓ |

### 3.2 Rangos válidos

| Feature | Rango contractual | Rango observado | Estado |
|---------|-------------------|-----------------|--------|
| `domain_complexity` | [0.0, 1.0] | [0.0, 1.0] | ✓ |
| `domain_whitelist` | {0, 1} | {0, 1} | ✓ |
| `trusted_token_context` | {-1, 0, +1} | {-1, 0, +1} | ✓ |
| `host_entropy` | [0.0, ~3.0] | [0.0, ~3.0] | ✓ |
| `infra_risk` | [0.0, 5.0] | [0.0, 5.0] | ✓ |
| `brand_in_path` | {0, 1} | {0, 1} | ✓ |
| `brand_match_flag` | {0, 1} | {0, 1} | ✓ |

### 3.3 Ausencia de NaN

| Verificación | Resultado |
|--------------|-----------|
| `df[FEATURES_V3].isna().sum().sum()` | 0 |
| Estado | ✓ Sin NaN |

### 3.4 Trazabilidad

| Campo | Verificación |
|-------|--------------|
| `commit_hash` | Presente en metadata |
| Checksums de fuentes | Verificados contra archivos actuales |
| Fecha de extracción | Registrada en metadata |

---

## 4. Análisis por feature

### 4.1 domain_complexity

| Atributo | Valor |
|----------|-------|
| Rol esperado | Señal continua principal |
| Comportamiento | Separación fuerte entre clases |
| Legítimas | Concentradas en valores bajos (dominios simples, oficiales) |
| Phishing | Distribución amplia hacia valores altos |
| Riesgos | Posible overfitting si modelo depende excesivamente de esta feature |

### 4.2 domain_whitelist

| Atributo | Valor |
|----------|-------|
| Rol esperado | Ancla de legitimidad |
| Comportamiento | Separación perfecta en subset whitelisted |
| Legítimas | Alta proporción con valor 1 |
| Phishing | Valor 0 en todos los casos |
| Riesgos | No discrimina phishing entre sí; solo ancla negativa |

### 4.3 trusted_token_context

| Atributo | Valor |
|----------|-------|
| Rol esperado | Ancla contextual (+1/0/-1) |
| Comportamiento | +1 exclusivo de legítimas whitelisted; -1 dominante en phishing |
| Legítimas | Distribución en +1 y 0 |
| Phishing | Concentrado en -1 |
| Riesgos | Colinealidad parcial con domain_whitelist (TTC=+1 implica whitelist=1) |

### 4.4 host_entropy

| Atributo | Valor |
|----------|-------|
| Rol esperado | Señal continua de aleatoriedad |
| Comportamiento | Separación moderada-fuerte |
| Legítimas | Entropía baja (subdominios predecibles o ausentes) |
| Phishing | Entropía moderada-alta (subdominios aleatorios de kits) |
| Riesgos | Outliers en legítimas con CDNs o subdominios técnicos |

### 4.5 infra_risk

| Atributo | Valor |
|----------|-------|
| Rol esperado | Señal continua de infraestructura |
| Comportamiento | Separación fuerte |
| Legítimas | Valores cercanos a 0 (HTTPS, TLDs confiables) |
| Phishing | Valores altos (HTTP, TLDs de riesgo, hosting gratuito) |
| Riesgos | Phishing sofisticado con HTTPS y TLDs normales no penalizado |

### 4.6 brand_in_path

| Atributo | Valor |
|----------|-------|
| Rol esperado | Evidencia puntual de abuso |
| Comportamiento | Activación rara pero precisa |
| Legítimas | Valor 0 en todos los casos (bypass por whitelist) |
| Phishing | Activa en ~20% (campañas con marca en ruta) |
| Riesgos | Baja cobertura; no detecta phishing sin marca explícita en path |

### 4.7 brand_match_flag

| Atributo | Valor |
|----------|-------|
| Rol esperado | Señal de legitimidad por marca en dominio |
| Comportamiento | Separación clara |
| Legítimas | Alta proporción con valor 1 (~73%) |
| Phishing | Baja proporción con valor 1 (~4%) |
| Riesgos | Activaciones en phishing corresponden a hosting neutral (Google Sites, GitHub) |

---

## 5. Hallazgos clave

### 5.1 Features con separación fuerte

| Feature | Observación |
|---------|-------------|
| `domain_complexity` | Principal discriminador continuo |
| `host_entropy` | Detecta patrones de kits de phishing |
| `infra_risk` | Captura infraestructura de bajo coste típica de campañas |

### 5.2 Features ancla (no predictivas por sí solas)

| Feature | Observación |
|---------|-------------|
| `domain_whitelist` | Garantiza cero falsos positivos en dominios oficiales |
| `trusted_token_context` | Proporciona contexto estructurado; colineal con whitelist |

### 5.3 Features de evidencia puntual

| Feature | Observación |
|---------|-------------|
| `brand_in_path` | Señal rara (~20% phishing) pero con precisión alta |
| `brand_match_flag` | Complementa whitelist para dominios .com/.net legítimos |

### 5.4 Outliers

| Observación | Detalle |
|-------------|---------|
| Concentración en legítimas | Outliers en host_entropy y domain_complexity corresponden a diversidad real (CDNs, subdominios técnicos, dominios internacionales) |
| Phishing homogéneo | Menor dispersión; patrones repetitivos de kits |

---

## 6. Limitaciones del EDA

### 6.1 Sesgo de selección del phishing

| Limitación | Implicación |
|------------|-------------|
| Phishing prefiltrado por scoring heurístico | Métricas de separación pueden ser optimistas |
| Phishing sofisticado subrepresentado | Modelo puede fallar en edge cases |
| Campañas con acortadores excluidas | Vector de ataque real no evaluado |

### 6.2 Whitelist como fuente de optimismo

| Limitación | Implicación |
|------------|-------------|
| Legítimas dominadas por whitelist | Separación artificialmente alta en domain_whitelist y TTC |
| Legítimas no-whitelisted subrepresentadas | Modelo puede no generalizar a dominios legítimos desconocidos |

### 6.3 Dataset de legítimas reducido en complejidad

| Limitación | Implicación |
|------------|-------------|
| Legítimas mayoritariamente oficiales (.es) | Baja representación de dominios legítimos complejos |
| Sectores sin phishing | ecommerce, energia, viajes, seguros sin contraparte maliciosa |

### 6.4 Colinealidad parcial

| Features | Observación |
|----------|-------------|
| `domain_whitelist` ↔ `trusted_token_context` | TTC=+1 implica whitelist=1 |
| `domain_whitelist` ↔ `domain_complexity` | whitelist=1 fuerza complexity=0 |

---

## 7. Decisiones tomadas

| Decisión | Justificación |
|----------|---------------|
| No modificar features v3 | Vector contractual inmutable según MANIFIESTO_V3 |
| No ajustar pesos | Fuera del alcance de EDA; decisión de scoring |
| No proponer nuevas features | EDA es diagnóstico, no diseño |
| EDA v3 cerrado formalmente | Análisis completado; no se admiten revisiones sin nueva versión |

---

## 8. Próximos pasos

Decisión pendiente del agente PLAN. Opciones identificadas:

| Opción | Descripción |
|--------|-------------|
| Ampliación de legítimas | Incorporar dominios legítimos no-whitelisted para reducir sesgo |
| Entrenamiento baseline con guardrails | Proceder con dataset actual, documentando limitaciones conocidas |

**Estado:** Pendiente de decisión arquitectónica.

---

## 9. Referencias

| Documento | Ruta |
|-----------|------|
| Manifiesto v3 | `docs/MANIFIESTO_V3.md` |
| Roadmap v3 | `docs/ROADMAP_V3.md` |
| README bootstrap v3 | `docs/README_v3_bootstrap.md` |
| Modificaciones dataset v2 | `docs/limpieza/README_modificaciones_dataset_v2.md` |

---

*EDA v3 cerrado. Cualquier revisión requiere nueva versión (EDA v3.1).*
