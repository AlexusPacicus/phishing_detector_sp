# README — Modificaciones del Dataset v2

**Versión:** 2.0  
**Estado:** CERRADO  
**Fecha:** Diciembre 2024  
**Fuentes:** `notebooks/limpieza_dataset_v2.ipynb`, `notebooks/limpieza_2_dataset_v2.ipynb`

---

## Estado contractual

| Atributo | Valor |
|----------|-------|
| Versión | 2.0 |
| Estado | CERRADO — No se admiten modificaciones sin nueva versión |
| Compatibilidad | features_v2, scoring_v2 |
| Output oficial | `notebooks/dataset_v2.csv` |
| Esquema | 6 columnas, 482 filas, balance 50/50 |

### Checksums de integridad

| Archivo | Filas | Columnas |
|---------|-------|----------|
| `dataset_base_v21.csv` (input) | 492 | 31 |
| `dataset_v2.csv` (output) | 482 | 6 |

---

## Resumen ejecutivo

**Qué:** Reducción del dataset de 492→482 URLs y de 31→6 columnas, con normalización de sectores/entidades y balance 50/50.

**Por qué:** El dataset base contenía ruido estructural (columnas intermedias), inconsistencias semánticas (variantes sin normalizar) y contaminación por URLs en acortadores o infraestructura comprometida que distorsionaban las features.

**Impacto en el modelo:** Dataset limpio que permite recalcular features sin leakage, con esquema mínimo y clases balanceadas para entrenamiento del modelo v2.

**Riesgos principales:**
- 5 sectores sin cobertura cruzada (ecommerce, energia, viajes, seguros solo tienen legítimas; generico solo tiene phishing)
- Vectores de ataque excluidos: sitios WordPress comprometidos y campañas con acortadores
- Variantes de entidad no consolidadas (unicajabanco/unicaja banco, bancosantander/banco santander)

---

## Advertencias de uso

### Exclusiones que afectan generalización

| Exclusión | URLs | Implicación |
|-----------|------|-------------|
| Acortadores (`bit.ly`, `l.ead.me`, etc.) | 4 | Modelo NO detecta smishing con URLs acortadas |
| WordPress comprometido (`/wp-content/`, `/wp-includes/`) | 4 | Modelo NO detecta webs legítimas hackeadas |
| Sectores sin phishing | 4 sectores | Modelo NO aprende patrones de phishing en ecommerce, energia, viajes, seguros |

### Restricciones de compatibilidad

| Componente | Compatibilidad | Notas |
|------------|----------------|-------|
| `features_v2.py` | ✓ Compatible | Diseñado para este dataset |
| `scoring_v2.py` | ✓ Compatible | Entrenado con este dataset |
| `features_v3.py` | ⚠ Parcial | Requiere validación; ver limitaciones |
| `scoring_v3.py` | ⚠ Parcial | Puede requerir reentrenamiento |

### Limitaciones para uso en v3

| Limitación | Motivo | Acción recomendada |
|------------|--------|-------------------|
| URLs con acortadores excluidas | No extraíbles por v2; v3 tampoco las procesa | No reincorporar sin resolver redirección |
| WordPress comprometido excluido | Señales contradictorias en features | Evaluar si v3 maneja mejor este patrón |
| Sectores sin cobertura cruzada | Sesgo inherente | Ampliar dataset antes de entrenar v3 |
| Variantes de entidad | Inconsistencia semántica | Consolidar antes de v3 |

---

## 1. Contexto y motivación

El dataset base v21 contenía 492 URLs con 31 columnas, incluyendo features calculadas, metadatos de scoring y campos auxiliares de distintas fuentes. Este exceso de información generaba:

- **Ruido estructural:** Columnas redundantes o específicas de procesos intermedios.
- **Inconsistencias semánticas:** Sectores y entidades sin normalizar, con variantes y acentos.
- **Contaminación por infraestructura:** URLs en hostings comprometidos (WordPress) o acortadores que dificultan el análisis de features.
- **Desbalance de clases:** 248 phishing vs 244 legítimas.

**Objetivo:** Producir un dataset limpio, balanceado y con esquema mínimo para entrenamiento del modelo v2.

---

## 2. Métricas de transformación

| Métrica | Antes | Después | Δ |
|---------|-------|---------|---|
| Filas | 492 | 482 | -10 |
| Columnas | 31 | 6 | -25 |
| Phishing | 248 | 241 | -7 |
| Legítimas | 244 | 241 | -3 |
| Balance | 50.4% / 49.6% | 50% / 50% | ✓ |
| Sectores | sin normalizar | 14 valores cerrados | ✓ |

**Esquema final:** `url`, `label`, `sector`, `entidad`, `notas`, `campaign`

---

## 3. Decisiones de diseño

### 3.1 Eliminación de URLs con acortadores (4 URLs)

**Justificación:** Los acortadores (`bit.ly`, `l.ead.me`, etc.) ocultan la URL real. Las features estructurales (dominio, path, TLD) se calculan sobre el acortador, no sobre el destino, generando señales falsas.

**Trade-off:** Se pierde representatividad de campañas reales que usan acortadores en SMS.

### 3.2 Separación de infraestructura comprometida (4 URLs)

**Justificación:** URLs con patrones WordPress (`/wp-content/`, `/wp-includes/`) representan sitios legítimos hackeados. Mezclan señales de legitimidad (dominio .es real) con phishing (ruta maliciosa), confundiendo `infra_risk` y `domain_whitelist_score`.

**Trade-off:** Se excluye un vector de ataque real (web comprometida) que el modelo no aprenderá a detectar.

### 3.3 Reducción a 6 columnas

**Justificación:** Las 25 columnas eliminadas eran:
- Features calculadas (se regeneran con `features_v2.py`)
- Metadatos de scoring intermedio
- Campos auxiliares de fuentes externas

Conservar solo datos semánticos evita leakage y permite recalcular features con cualquier versión del extractor.

### 3.4 Normalización de sector y entidad

**Justificación:** Unificar variantes (`"logística"` → `"logistica"`, `"banco sabadell"` → `"sabadell"`) permite:
- Agregación correcta por sector
- Análisis de recall por entidad
- Detección de sobrerrepresentación

### 3.5 Balanceo 50/50

**Justificación:** Eliminar 2 URLs legítimas de `energia` (sector con más margen) para lograr balance perfecto. Un dataset balanceado simplifica la interpretación de métricas y evita sesgo hacia la clase mayoritaria.

**Trade-off:** Pérdida mínima de cobertura en sector ya infrarrepresentado.

---

## 4. Criterios de filtrado

### 4.1 Exclusión

| Criterio | URLs eliminadas | Motivo |
|----------|-----------------|--------|
| Acortadores conocidos | 4 | Features no analizables |
| Patrones WordPress/CMS | 4 | Señales contradictorias |
| Balanceo de clases | 2 | Ajuste 50/50 |

### 4.2 Inclusión

| Criterio | Aplicación |
|----------|------------|
| Sector válido | 14 valores cerrados; resto → `generico` |
| Entidad requerida | Inferencia por tokens de marca en URL |
| URL única | Deduplicación exacta |

### 4.3 Reasignaciones de sector

| Entidades | Sector asignado |
|-----------|-----------------|
| instagram, twitter, linkedin, whatsapp, yahoo | redessociales |
| aws, auth0, cloudflare, ionos, azure, okta, stripe, paypal | saas |
| redsys | cripto |
| financieraelcorteingles | ecommerce |
| unicismadrid | publico |

---

## 5. Transformaciones aplicadas

### 5.1 Phishing (label=1)

- **Inferencia de entidad:** 32 URLs recibieron entidad inferida desde tokens de marca en dominio/subdominio/path.
- **Sector `generico`:** 55 URLs sin marca atribuible asignadas a este sector.

### 5.2 Legítimas (label=0)

- **Completado desde whitelist:** 74 URLs recibieron entidad desde `docs/whitelist.csv`.
- **Eliminación para balanceo:** 2 URLs del sector `energia`.

---

## 6. Esquema final del dataset

### 6.1 Columnas

| Columna | Tipo | Nulos | Descripción |
|---------|------|-------|-------------|
| `url` | string | 0% | URL completa |
| `label` | int | 0% | 0=legítima, 1=phishing |
| `sector` | string | 0% | Sector normalizado |
| `entidad` | string | 0% | Marca objetivo |
| `notas` | string | 31% | Justificación de inclusión |
| `campaign` | string | 82% | ID de campaña (solo phishing) |

### 6.2 Distribución por sector

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

---

## 7. Limitaciones y trade-offs

### 7.1 Sectores sin cobertura cruzada

| Sector | Problema | Implicación |
|--------|----------|-------------|
| ecommerce | 0 phishing | Modelo no aprende patrones de phishing retail |
| energia | 0 phishing | Modelo no aprende patrones de phishing energético |
| viajes | 0 phishing | Modelo no aprende patrones de phishing turístico |
| seguros | 0 phishing | Modelo no aprende patrones de phishing asegurador |
| generico | 0 legítimas | Cualquier URL `generico` será inherentemente sospechosa |

### 7.2 Variantes de entidad no consolidadas

| Variante 1 | Variante 2 | Acción pendiente |
|------------|------------|------------------|
| unicajabanco | unicaja banco | Unificar |
| bancosantander | banco santander | Unificar |
| bancsabadell | sabadell | Unificar |

### 7.3 Vectores de ataque excluidos

- **Sitios WordPress comprometidos:** Excluidos por ruido en features; no representados.
- **Campañas con acortadores:** Excluidas; patrón real de smishing no capturado.

### 7.4 Campos con alta proporción de nulos

- `campaign` (82% nulos): Solo phishing tiene este campo poblado.
- `notas` (31% nulos): URLs legítimas de whitelist sin justificación explícita.

---

## 8. Archivos de referencia

| Archivo | Rol | Estado |
|---------|-----|--------|
| `data/clean/dataset_base_v21.csv` | Input (31 columnas) | Histórico |
| `data/interim/dataset_entrenamiento_v2.csv` | Intermedio | Histórico |
| `notebooks/dataset_v2.csv` | Output final (6 columnas) | **Contractual** |
| `docs/whitelist.csv` | Whitelist de dominios españoles | Vigente |

---

## 9. Historial de versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 2.0 | Dic 2024 | Versión inicial cerrada |

---

*Documento contractual del dataset v2. Cualquier modificación requiere nueva versión.*
