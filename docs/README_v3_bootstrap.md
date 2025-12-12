# README — Bootstrap v3

**Versión:** 3.0  
**Estado:** CONTRACTUAL  
**Ubicación:** `docs/README_v3_bootstrap.md`

---

## 1. Objetivo del bootstrap v3

Centralizar la carga de las dos fuentes de verdad del extractor v3:

| Recurso | Fuente | Constante |
|---------|--------|-----------|
| whitelist v3 | `docs/whitelist.csv` | retornada por `initialize_v3()` |
| brands_set v3 | `docs/dominios_espanyoles.csv` | `constants["BRANDS_FROM_DOMAINS_ES"]` |

**Propósito:**
- Garantizar consistencia entre scripts, notebooks y pipeline de scoring.
- Eliminar construcciones manuales de whitelist o brands_set.
- Evitar mezclas con loaders v2.

---

## 2. Contrato de inicialización v3

### 2.1 Fuentes exclusivas

| Dato | Fuente única | Loader |
|------|--------------|--------|
| whitelist | `docs/whitelist.csv` | `load_whitelist_v3()` |
| brands_set | `docs/dominios_espanyoles.csv` | `load_brands_set_v3()` |

### 2.2 Función `initialize_v3()`

```python
def initialize_v3():
    whitelist = load_whitelist_v3()
    load_brands_set_v3(constants)
    
    # Asserts contractuales
    assert whitelist is not None and len(whitelist) > 0
    assert "BRANDS_FROM_DOMAINS_ES" in constants
    assert len(constants["BRANDS_FROM_DOMAINS_ES"]) > 0
    
    return whitelist, constants
```

### 2.3 Asserts contractuales

| Assert | Motivo |
|--------|--------|
| `len(whitelist) > 0` | Whitelist vacía invalida domain_whitelist y TTC |
| `"BRANDS_FROM_DOMAINS_ES" in constants` | brands_set requerido por brand_in_path, brand_match_flag, TTC |
| `len(brands_set) > 0` | brands_set vacío invalida detección de marcas |

---

## 3. Uso obligatorio

### 3.1 Código mínimo correcto

```python
from features.loaders_v3 import initialize_v3

whitelist, constants = initialize_v3()
```

### 3.2 Prohibiciones

| Acción | Estado |
|--------|--------|
| Pasar whitelist externa a `extract_features_v3()` | ❌ PROHIBIDO |
| Construir `brands_set` manualmente | ❌ PROHIBIDO |
| Usar `load_whitelist()` de v2 como fuente v3 | ❌ PROHIBIDO |
| Usar `load_brands_from_domains_es()` de v2 | ❌ PROHIBIDO |
| Omitir `initialize_v3()` | ❌ PROHIBIDO |

---

## 4. Flujo de extracción v3

### 4.1 Extracción individual

```python
from features.loaders_v3 import initialize_v3
from features.features_v3 import extract_features_v3

whitelist, constants = initialize_v3()
features = extract_features_v3(url, whitelist, constants)
```

### 4.2 Extracción batch (dataset)

```python
from extract_features_dataset_v3 import extract_features_dataset_v3

df_features = extract_features_dataset_v3(df)
```

`extract_features_dataset_v3` ejecuta `initialize_v3()` internamente. No requiere inicialización previa.

### 4.3 Diagrama de flujo

```
┌─────────────────────────────────────────────────────┐
│                  initialize_v3()                    │
├─────────────────────────────────────────────────────┤
│  load_whitelist_v3()     → whitelist                │
│  load_brands_set_v3()    → constants["BRANDS_..."]  │
│  asserts contractuales                              │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│           extract_features_v3(url, wl, c)           │
├─────────────────────────────────────────────────────┤
│  domain_complexity(url, whitelist)                  │
│  domain_whitelist(url, whitelist)                   │
│  trusted_token_context(url, whitelist, brands_set)  │
│  host_entropy(url)                                  │
│  infra_risk(url)                                    │
│  brand_in_path(url, brands_set)                     │
│  brand_match_flag(url, brands_set)                  │
└─────────────────────────────────────────────────────┘
```

---

## 5. Advertencias contractuales

| Violación | Consecuencia |
|-----------|--------------|
| Bypass de `initialize_v3()` | Extracción v3 inválida |
| Whitelist externa | Inconsistencia en domain_whitelist y TTC |
| brands_set manual | Inconsistencia en brand_in_path, brand_match_flag, TTC |
| Mezcla con loaders v2 | Contaminación de fuentes de verdad |

### 5.1 Separación v2 / v3

| Componente | Debe usar |
|------------|-----------|
| `scoring_v3.py` | `initialize_v3()` |
| `extract_features_v3.py` | `initialize_v3()` |
| `scoring_v2.py` | loaders v2 (NO bootstrap v3) |
| `features_v2.py` | loaders v2 (NO bootstrap v3) |
| limpieza / EDA v2 | loaders v2 (NO bootstrap v3) |

---

*Documento contractual del bootstrap v3.*
