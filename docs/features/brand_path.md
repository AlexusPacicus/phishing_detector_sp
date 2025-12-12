# Feature: brand_in_path — Especificación v3 FINAL

**Estado:** CERRADO  
**Posición en vector:** 6  
**Dependencia crítica:** `constants["BRANDS_FROM_DOMAINS_ES"]`

---

## 1. Definición

Detecta presencia de una marca española en el path de la URL, activándose únicamente cuando el dominio NO es legítimo.

| Atributo | Valor |
|----------|-------|
| Tipo | int |
| Valores | {0, 1} |
| Activación | Solo si `domain_whitelist == 0` |

---

## 2. Fuente de verdad de marcas españolas

### 2.1 Origen

Las marcas se derivan **exclusivamente** de `docs/dominios_espanyoles.csv`.

**NO se derivan de:**
- Whitelist
- Dataset de entrenamiento
- Listas manuales

### 2.2 Construcción de `brands_set`

```python
brands_set = constants["BRANDS_FROM_DOMAINS_ES"]
```

### 2.3 Requisito de inicialización

```python
load_brands_from_domains_es(constants)
```

Debe ejecutarse **antes** de cualquier llamada a `extract_features_v3()`.

---

## 3. Algoritmo

### 3.1 Extracción del path

```python
path = url.split("/", 3)[-1].lower()
```

Devuelve el segmento final tras el tercer `/`.

### 3.2 Tokenización

```python
tokens = re.split(r"[\/\-\_\.\=\&\?\%]", path)
```

Separadores: `/`, `-`, `_`, `.`, `=`, `&`, `?`, `%`

### 3.3 Detección de marca

```python
brand_in_path_raw = int(any(t in brands_set for t in tokens if t))
```

Comparación **exacta** de tokens, no substrings.

### 3.4 Protección por dominio legítimo

```python
brand_in_path = brand_in_path_raw if domain_whitelist == 0 else 0
```

---

## 4. Ejemplos

| URL | Tokens | domain_whitelist | Resultado |
|-----|--------|------------------|-----------|
| `https://seguridad-bbva.live/bbva/login` | [bbva, login] | 0 | 1 |
| `https://correos.es/estado/paquete` | [estado, paquete] | 1 | 0 |
| `https://aq29qx.top/correos/verify` | [correos, verify] | 0 | 1 |
| `https://random.xyz/bbvaseguridad` | [bbvaseguridad] | 0 | 0 (no exacto) |

---

## 5. Propiedades

| Propiedad | Estado |
|-----------|--------|
| Falsos positivos | 0 confirmados |
| Recall en campañas ES | Alto (banca, logística, telco) |
| Dependencia de path | Solo segmento final |
| Solapamiento con TTC | Ninguno (TTC no analiza path) |

---

## 6. Relación con otras features

| Feature | Relación |
|---------|----------|
| domain_whitelist | brand_in_path solo activa si esta = 0 |
| trusted_token_context | Complementarias; TTC no usa path |
| brand_match_flag | brand_in_path detecta marca en path; brand_match_flag en dominio |
| infra_risk | Se combinan bien: host random + marca en path |

---

*Feature contractual del vector v3.*
