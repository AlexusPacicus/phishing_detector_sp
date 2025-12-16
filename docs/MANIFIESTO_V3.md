# MANIFIESTO v3 — Contrato del Pipeline de Features

**Versión:** 3.0  
**Estado:** CONTRACTUAL  
**Fecha:** Diciembre 2024  
**Ámbito:** Features, loaders, dataset, bootstrap, reproducibilidad

---

## 1. Fuentes canónicas v3

### 1.1 Dataset base

| Atributo | Valor |
|----------|-------|
| Fuente | Dataset v2 limpio |
| Archivo | `notebooks/dataset_v2.csv` |
| Schema | `url`, `label`, `sector`, `entidad`, `notas`, `campaign` |
| Filas | 482 |
| Balance | 50/50 |

### 1.2 Whitelist v3

| Atributo | Valor |
|----------|-------|
| Archivo | `docs/whitelist.csv` |
| Loader exclusivo | `load_whitelist_v3()` |
| Contenido | Dominios oficiales españoles + proveedores globales verificados |
| Uso | `domain_whitelist`, `domain_complexity`, `trusted_token_context (+1)` |

### 1.3 Brands set v3

| Atributo | Valor |
|----------|-------|
| Archivo | `docs/dominios_espanyoles.csv` |
| Loader exclusivo | `load_brands_set_v3()` |
| Contenido | Marcas españolas derivadas de dominios .es (ranking Tranco) |
| Constante | `constants["BRANDS_FROM_DOMAINS_ES"]` |
| Uso | `brand_in_path`, `brand_match_flag`, `trusted_token_context (0)` |

### 1.4 Global neutral domains

| Atributo | Valor |
|----------|-------|
| Archivo | `docs/global_neutral_domains.csv` |
| Contenido | Dominios de infraestructura neutra (Google, GitHub, Cloudflare, etc.) |
| Uso | Exclusión de penalizaciones en features estructurales |

### 1.5 Prohibiciones absolutas

| Acción | Estado |
|--------|--------|
| Usar loaders v2 (`load_whitelist()`, `load_brands_from_domains_es()`) | ❌ PROHIBIDO |
| Pasar whitelists externas a `extract_features_v3()` | ❌ PROHIBIDO |
| Construir `brands_set` manualmente | ❌ PROHIBIDO |
| Cargar CSVs sin los loaders v3 oficiales | ❌ PROHIBIDO |
| Modificar fuentes canónicas sin nueva versión | ❌ PROHIBIDO |

---

## 2. Contrato del dataset v3

### 2.1 Schema final obligatorio

| Columna | Tipo | Origen | Nulos permitidos |
|---------|------|--------|------------------|
| `url` | string | dataset v2 | No |
| `label` | int | dataset v2 | No |
| `sector` | string | dataset v2 | No |
| `entidad` | string | dataset v2 | No |
| `notas` | string | dataset v2 | Sí |
| `campaign` | string | dataset v2 | Sí |
| `domain_complexity` | float | FEATURES_V3 | No |
| `domain_whitelist` | int | FEATURES_V3 | No |
| `trusted_token_context` | int | FEATURES_V3 | No |
| `host_entropy` | float | FEATURES_V3 | No |
| `infra_risk` | float | FEATURES_V3 | No |
| `brand_in_path` | int | FEATURES_V3 | No |
| `brand_match_flag` | int | FEATURES_V3 | No |

### 2.2 Tipos de datos

| Feature | Tipo Python | Rango |
|---------|-------------|-------|
| `domain_complexity` | float64 | [0.0, 1.0] |
| `domain_whitelist` | int64 | {0, 1} |
| `trusted_token_context` | int64 | {-1, 0, +1} |
| `host_entropy` | float64 | [0.0, ~4.5] |
| `infra_risk` | float64 | [0.0, ~3.5] |
| `brand_in_path` | int64 | {0, 1} |
| `brand_match_flag` | int64 | {0, 1} |

**Nota sobre rangos:**
- `host_entropy`: Entropía Shannon raw del subdominio, sin normalizar. Rango observado empíricamente.
- `infra_risk`: Suma aditiva de componentes de riesgo, sin normalizar. Rango observado empíricamente.
- Interpretación de ambas features es relativa al dataset; no son scores 0–1.

### 2.3 Invariantes

| Invariante | Condición |
|------------|-----------|
| Sin NaN en features | `df[FEATURES_V3].isna().sum().sum() == 0` |
| Sin NaN en columnas críticas | `df[["url", "label"]].isna().sum().sum() == 0` |
| Balance de clases | `df["label"].value_counts()` ≈ 50/50 |
| URLs únicas | `df["url"].duplicated().sum() == 0` |

### 2.4 Reglas de inclusión/exclusión (heredadas de v2)

| Regla | Aplicación |
|-------|------------|
| URLs con acortadores | Excluidas |
| URLs con patrones WordPress (`/wp-content/`, `/wp-includes/`) | Excluidas |
| Sectores válidos | 14 valores cerrados |
| Entidad requerida | Obligatoria para todas las filas |

### 2.5 Orden de columnas

```
[url, label, sector, entidad, notas, campaign] + FEATURES_V3
```

El orden de `FEATURES_V3` es contractual e inmutable.

---

## 3. Contrato de FEATURES_V3

### 3.1 Vector contractual (orden fijo e inmutable)

```python
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

### 3.2 Definiciones

| # | Feature | Tipo | Descripción |
|---|---------|------|-------------|
| 1 | `domain_complexity` | float | Complejidad estructural del dominio (entropía + longitud + penalizaciones) |
| 2 | `domain_whitelist` | int | 1 si dominio ∈ whitelist_v3, 0 en caso contrario |
| 3 | `trusted_token_context` | int | Contexto de legitimidad: +1 (whitelist), 0 (marca), -1 (resto) |
| 4 | `host_entropy` | float | Entropía Shannon del subdominio |
| 5 | `infra_risk` | float | Riesgo agregado de infraestructura (HTTP + TLD + hosting) |
| 6 | `brand_in_path` | int | 1 si marca española detectada en path (solo si no whitelist) |
| 7 | `brand_match_flag` | int | 1 si núcleo del dominio coincide con marca española |

### 3.3 Reglas de precedencia y bypass

#### 3.3.1 Bypass por whitelist

Cuando `domain_whitelist == 1`:

| Feature | Valor forzado | Motivo |
|---------|---------------|--------|
| `domain_complexity` | 0.0 | Dominio oficial no requiere análisis de complejidad |
| `brand_in_path` | 0 | No hay abuso de marca en dominio legítimo |
| `trusted_token_context` | +1 | Máxima confianza |

#### 3.3.2 Lógica de trusted_token_context

```
trusted_token_context =
    +1  si domain_whitelist == 1
     0  si domain_whitelist == 0 AND brand_match_flag == 1
    -1  en otro caso
```

TTC depende **exclusivamente** de `domain_whitelist` y `brand_match_flag`.  
TTC **no analiza** el path.

#### 3.3.3 Condición de brand_in_path

```
brand_in_path se evalúa solo si domain_whitelist == 0
```

Si `domain_whitelist == 1`, `brand_in_path = 0` sin evaluación.

### 3.4 Inmutabilidad

| Restricción | Ámbito |
|-------------|--------|
| Lista de features | Inmutable en v3 |
| Orden de features | Inmutable en v3 |
| Tipos de datos | Inmutables en v3 |
| Reglas de bypass | Inmutables en v3 |

Cualquier modificación requiere nueva versión (v3.1 o v4).

---

## 4. Bootstrap v3

### 4.1 Función única de inicialización

```python
from features.loaders_v3 import initialize_v3

whitelist, constants = initialize_v3()
```

### 4.2 Operaciones de initialize_v3()

| Paso | Operación |
|------|-----------|
| 1 | `whitelist = load_whitelist_v3()` |
| 2 | `load_brands_set_v3(constants)` |
| 3 | Assert: `whitelist is not None and len(whitelist) > 0` |
| 4 | Assert: `"BRANDS_FROM_DOMAINS_ES" in constants` |
| 5 | Assert: `len(constants["BRANDS_FROM_DOMAINS_ES"]) > 0` |
| 6 | Return: `(whitelist, constants)` |

### 4.3 Prohibiciones del bootstrap

| Acción | Estado |
|--------|--------|
| Omitir `initialize_v3()` antes de extracción | ❌ PROHIBIDO |
| Pasar whitelist externa a `extract_features_v3()` | ❌ PROHIBIDO |
| Cargar marcas manualmente | ❌ PROHIBIDO |
| Usar loaders v2 como fuente v3 | ❌ PROHIBIDO |
| Modificar `constants` después de inicialización | ❌ PROHIBIDO |

### 4.4 Integración con extractores

| Componente | Inicialización |
|------------|----------------|
| `extract_features_v3(url, whitelist, constants)` | Requiere `initialize_v3()` previo |
| `extract_features_dataset_v3(df)` | Ejecuta `initialize_v3()` internamente |

---

## 5. Artefactos de salida v3

### 5.1 Dataset con features

| Atributo | Valor |
|----------|-------|
| Archivo | `dataset_v3_features.csv` |
| Encoding | UTF-8 |
| Separador | `,` |
| Schema | Columnas v2 + FEATURES_V3 |

### 5.2 Metadata obligatoria (JSON)

Archivo: `dataset_v3_metadata.json`

```json
{
  "version": "3.0",
  "extraction_date": "YYYY-MM-DD HH:MM:SS",
  "commit_hash": "<hash del commit>",
  "sources": {
    "dataset_base": {
      "path": "notebooks/dataset_v2.csv",
      "rows": 482,
      "checksum": "<SHA256>"
    },
    "whitelist": {
      "path": "docs/whitelist.csv",
      "entries": <N>,
      "checksum": "<SHA256>"
    },
    "dominios_espanyoles": {
      "path": "docs/dominios_espanyoles.csv",
      "entries": <N>,
      "checksum": "<SHA256>"
    },
    "global_neutral_domains": {
      "path": "docs/global_neutral_domains.csv",
      "entries": <N>,
      "checksum": "<SHA256>"
    }
  },
  "extractor": {
    "module": "features.features_v3",
    "deterministic": true,
    "features": ["domain_complexity", "domain_whitelist", "trusted_token_context", "host_entropy", "infra_risk", "brand_in_path", "brand_match_flag"]
  },
  "output": {
    "path": "dataset_v3_features.csv",
    "rows": 482,
    "columns": 13,
    "nan_count": 0
  }
}
```

### 5.3 Campos obligatorios del metadata

| Campo | Requerido | Descripción |
|-------|-----------|-------------|
| `version` | Sí | Versión del pipeline |
| `extraction_date` | Sí | Timestamp de extracción |
| `commit_hash` | Sí | Hash del commit del código |
| `sources.*.path` | Sí | Ruta de cada fuente |
| `sources.*.checksum` | Sí | SHA256 de cada fuente |
| `extractor.deterministic` | Sí | Debe ser `true` |
| `output.nan_count` | Sí | Debe ser `0` |

### 5.4 Requisitos de reproducibilidad

| Requisito | Condición |
|-----------|-----------|
| Determinismo | Mismas fuentes + mismo código → mismo output |
| Trazabilidad | Metadata vincula output con fuentes exactas |
| Modelo .joblib | Debe incluir referencia al `commit_hash` y checksums de fuentes |
| Validación | `nan_count == 0` obligatorio antes de entrenamiento |

### 5.5 Modelo entrenado

| Atributo | Requisito |
|----------|-----------|
| Formato | `.joblib` |
| Metadata asociada | `commit_hash`, checksums de fuentes, fecha de entrenamiento |
| Reproducibilidad | Reentrenable con mismas fuentes y código |

---

## 6. Validación contractual

### 6.1 Checklist de cumplimiento

| # | Verificación | Comando/Assert |
|---|--------------|----------------|
| 1 | Bootstrap ejecutado | `whitelist is not None` |
| 2 | Brands cargadas | `"BRANDS_FROM_DOMAINS_ES" in constants` |
| 3 | Sin NaN en features | `df[FEATURES_V3].isna().sum().sum() == 0` |
| 4 | Tipos correctos | `df[FEATURES_V3].dtypes` |
| 5 | Metadata generada | `os.path.exists("dataset_v3_metadata.json")` |
| 6 | Checksums válidos | Comparar con metadata |

### 6.2 Violaciones contractuales

| Violación | Consecuencia |
|-----------|--------------|
| NaN en features | Dataset v3 inválido |
| Bootstrap omitido | Extracción inválida |
| Loaders v2 usados | Contaminación de fuentes |
| Metadata ausente | Output no reproducible |
| Checksums no coinciden | Trazabilidad rota |

---

*Documento contractual del pipeline v3. Inmutable dentro de la versión 3.0.*
