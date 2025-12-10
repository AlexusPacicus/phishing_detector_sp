# 🧩 Features v2 — Especificación técnica (Parte 2: Features internas)

**Versión:** v2  
**Estado:** cerrado  
**Responsable:** Alexis Zapico Fernández  
**Ámbito:** Definición técnica de las features internas requeridas para construir las 9 features finales.  
**Dependencias:** `features_constantes.py`, `features_v2_tecnico_parte1.md`

---

# 🎯 1. Objetivo

Este documento define las **features internas** necesarias para construir las features finales de v2.

Estas features **NO se exportan** al modelo, pero son esenciales para la construcción de:

- `domain_complexity`  
- `host_entropy`  
- `token_density`  
- `trusted_token_context`  
- `infra_risk`  

Su función es ofrecer soporte estructural y semántico coherente al Feature Engineering.

---

# 🧪 2. Features internas — Definición técnica

---

## 🔹 1) `domain_length`

**Tipo:** int  
**Rango esperado:** 3–30  

**Definición:**  
Longitud del `registered_domain` (`extract.registered_domain.lower()`).

**Cálculo:**  
```python
domain = extract.registered_domain.lower()
domain_length = len(domain) if domain else 0
```

**Errores:** → 0

---

## 🔹 2) `domain_entropy`

**Tipo:** float  
**Rango esperado:** 0–3  

**Definición:**  
Entropía Shannon del dominio (`extract.domain.lower()`), sin TLD ni subdominio.

**Cálculo:**  
```python
domain = extract.domain.lower()
if not domain:
    entropy = 0
else:
    # freq table
    entropy = -sum((c_count/len(domain)) * log2(c_count/len(domain))
                   for c_count in character_counts)
```

**Errores:** → 0

---

## 🔹 3) `is_http`

**Tipo:** int  
**Rango:** {0,1}

**Definición:**  
1 si la URL comienza por `"http://"` (no cifrada).  
0 en cualquier otro caso.

```python
is_http = 1 if url.lower().startswith("http://") else 0
```

---

## 🔹 4) `tld_risk_weight`

**Tipo:** float  
**Rango:** 0–3  

**Definición:**  
Peso asociado al TLD (`extract.suffix.lower()`), según el diccionario `TLD_RISK`.

```python
tld = extract.suffix.lower()
tld_risk_weight = TLD_RISK.get(tld, 0)
```

---

## 🔹 5) `free_hosting`

**Tipo:** int  
**Rango:** {0,1}

**Definición:**  
1 si el host completo contiene algún patrón definido en `FREE_HOSTING`.  
0 si no.

```python
host = urlparse(url).netloc.lower()
free_hosting = 1 if any(h in host for h in FREE_HOSTING) else 0
```

---

## 🔹 6) `trusted_path_token`

**Tipo:** int  
**Rango:** {0,1}

**Definición:**  
1 si el path contiene tokens legítimos (`TRUSTED_TOKENS`).  
0 si no.

```python
path = urlparse(url).path.lower()
trusted_path_token = 1 if any(t in path for t in TRUSTED_TOKENS) else 0
```

---

## 🔹 7) `trusted_path_penalty`

**Tipo:** int  
**Rango:** {0,1}

**Definición:**  
Penalización si aparece un token legítimo en un dominio NO oficial.

```python
trusted_path_penalty = 1 if (trusted_path_token == 1 and 
                             domain_whitelist_score == 0) else 0
```

---

## 🔹 8) `total_tokens`

**Tipo:** int  
**Rango:** 0–15

**Definición:**  
Número total de tokens del path después de normalizar separadores.

**Separadores normalizados:** `"-"`, `"_"`, `"%20"`, `"."`

```python
path = urlparse(url).path.lower()
for sep in ["-", "_", "%20", "."]:
    path = path.replace(sep, "/")

tokens = [t for t in path.split("/") if t]
total_tokens = len(tokens)
```

---

## 🔹 9) `path_depth`

**Tipo:** int  
**Rango:** 0–10

**Definición:**  
Número de segmentos estructurales del path.  
(Solo se divide por `/`, NO por otros separadores.)

```python
path = urlparse(url).path.lower()
segments = [s for s in path.split("/") if s]
path_depth = len(segments)
```

---

# ✔ 3. Estado de la Parte 2

- Todas las features internas están **cerradas y definidas técnicamente**.  
- No existen ambigüedades ni comportamientos indefinidos.  
- La documentación es consistente con `features_v2_tecnico_parte1.md`.  
- El módulo `features_v2.py` puede implementarse sin dudas.  

---

# ✔ Fin de la Parte 2
