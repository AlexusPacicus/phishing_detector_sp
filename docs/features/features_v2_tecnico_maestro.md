# 🧩 Features v2 — Especificación técnica completa (Extractor v2)

**Versión:** v2  
**Estado:** cerrado  
**Responsable:** Alexis Zapico Fernández  
**Ámbito:** Diseño técnico unificado del extractor de características v2 para detección de phishing orientado a usuarios españoles.  
**Dependencias:**  
- `features_constantes.py`  
- `spanish_whitelist`  
- `tokens_por_sector.csv` está desactivado en v2; se incorporará en una versión futura.


---

# 🎯 1. Objetivo

Este documento define de forma unificada:

- el **vector final de salida** (9 features),  
- las **features internas** necesarias para construirlo,  
- las **fórmulas matemáticas completas**,  
- el **orden exacto del pipeline**,  
- el **pseudocódigo contractual**,  
- y las **reglas de manejo de errores**.

Esta especificación sirve como guía para implementar `features_v2.py` sin ambigüedades.

---

# 🧱 2. Output Schema (Orden contractual)

El extractor debe devolver exactamente este vector de 9 elementos, en este orden:

```
[
  "domain_complexity",
  "host_entropy",
  "domain_whitelist_score",
  "suspicious_path_token",
  "token_density",
  "trusted_token_context",
  "infra_risk",
  "fake_tld_in_subdomain_or_path",
  "param_count_boost"
]
```

No se permiten columnas adicionales ni cambios de orden.

---

# 🧩 3. Features finales — Definición técnica

---

## 1) domain_complexity
**Tipo:** float  
**Rango:** 0–25  

Complejidad del dominio según:
`domain_length × domain_entropy`.

---

## 2) host_entropy
**Tipo:** float  
**Rango:** 0–3  

Entropía del subdominio eliminando puntos:
subdomain_clean = extract.subdomain.lower().replace(".", "")
host_entropy = H(subdomain_clean)


---

## 3) domain_whitelist_score
**Tipo:** int  
**Rango:** {0,1}

1 si `registered_domain` pertenece a la whitelist española; 0 si no.

---

## 4) suspicious_path_token
**Tipo:** int  
**Rango:** {0,1}

1 si el path contiene tokens sospechosos (verificar, pago, paquete, envio, 3dsecure, sms…).

---

## 5) token_density
**Tipo:** float  
**Rango:** 0–2 aprox  

Densidad semántica de tokens de phishing en el path, ajustada por profundidad estructural.

---

## 6) trusted_token_context
**Tipo:** int  
**Rango:** {-1,0,+1}

Contexto de confianza:

- +1 → token legítimo + dominio oficial  
- -1 → token legítimo + dominio falso  
- 0 → sin token legítimo  

---

## 7) infra_risk
**Tipo:** float  
**Rango:** 0–5  

`0.3·is_http + tld_risk_weight + free_hosting`.

---

## 8) fake_tld_in_subdomain_or_path
**Tipo:** int  
**Rango:** {0,1}

1 si algún patrón en FAKE_TLD_TOKENS aparece como SUBSTRING en host o path,
siempre que dicho patrón NO coincida con el suffix real de la URL.

Ejemplo: 
fake="es" en "bbva.es" → NO activa señal (suffix real coincide).
fake="es" en "bbva.es-login.com" → activa señal.


## 9) param_count_boost
**Tipo:** float  
**Rango:** 0–0.9  

Penalización basada en número de parámetros query:
`P / (P + 1)`.

---

# 🧬 4. Features internas — Definición técnica

Estas features **no se exportan**, pero son necesarias para construir las finales.

---

## 🔹 1) domain_length
```python
domain_length = len(registered) if registered else 0
```

---

## 🔹 2) domain_entropy
```python
if not domain:
    domain_entropy = 0
else:
    freqs = Counter(domain)
    domain_entropy = -sum((c/len(domain)) * log2(c/len(domain)) 
                          for c in freqs.values())
```

---

## 🔹 3) is_http
```python
is_http = 1 if url.lower().startswith("http://") else 0
```

---

## 🔹 4) tld_risk_weight
```python
tld = extract.suffix.lower()
tld_risk_weight = TLD_RISK.get(tld, 0)
```

---

## 🔹 5) free_hosting
```python
free_hosting = 1 if any(h in host for h in FREE_HOSTING) else 0
```

---

## 🔹 6) trusted_path_token
```python
trusted_path_token = 1 if any(t in path for t in TRUSTED_TOKENS) else 0
```

---


## 🔹 7) total_tokens
```python
normalized = path
for sep in ["-", "_", "%20", "."]:
    normalized = normalized.replace(sep, "/")
tokens = [t for t in normalized.split("/") if t]
total_tokens = len(tokens)
```

---

## 🔹 8) path_depth
```python
segments = [s for s in path.split("/") if s]
path_depth = len(segments)
```

---

# 🧮 5. Fórmulas matemáticas finales

---

## domain_complexity
\[
domain\_complexity = domain\_length \times domain\_entropy
\]

---

## host_entropy
\[
host_entropy = H(subdomain_clean)

\]

---

## token_density
\[
token\_density =
\left(\frac{W}{total\_tokens}\right)
\times
\left(\frac{path\_depth}{path\_depth + 2}\right)
\]

---

## trusted_token_context
\[
trusted_token_context =
    +1 si hay token legítimo y el dominio está en la whitelist
    -1 si hay token legítimo y el dominio NO está en la whitelist
     0 si no hay token legítimo

\]

---

## infra_risk
\[
infra\_risk = 0.3\cdot is\_http + tld\_risk\_weight + free\_hosting
\]

---

## param_count_boost
\[
param\_count\_boost = \frac{P}{P+1}
\]

---

# 🧬 6. Matriz de dependencias

| Feature final | Internas necesarias |
|---------------|---------------------|
| domain_complexity | domain_length, domain_entropy |domain_length se calcula sobre registered_domain.
domain_entropy se calcula sobre extract.domain (core sin TLD ni subdominio).
| host_entropy | subdomain entropy |
| domain_whitelist_score | registered_domain |
| suspicious_path_token | path |
| token_density | W (suma de pesos), total_tokens, path_depth |En v2, TOKEN_DENSITY_K = 2.
| trusted_token_context | trusted_path_token, domain_whitelist_score |
| infra_risk | is_http, tld_risk_weight, free_hosting |
| fake_tld_in_subdomain_or_path | FAKE_TLD_TOKENS, subdomain, path |
| param_count_boost | param_count |

---

# 👨‍💻 7. Pseudocódigo contractual del extractor `features_v2.py`

```python
def extract_features_v2(url):

    # -------- A) PARSING --------
    extract = tldextract.extract(url)
    parsed = urlparse(url)

    domain = extract.domain.lower()
    registered = extract.registered_domain.lower()
    subdomain = extract.subdomain.lower()
    path = parsed.path.lower()
    host = parsed.netloc.lower()

    # -------- B) INTERNAS BÁSICAS --------
    domain_length = len(registered) if registered else 0

    if not domain:
        domain_entropy = 0
    else:
        freqs = Counter(domain)
        domain_entropy = -sum((c/len(domain)) * log2(c/len(domain))
                              for c in freqs.values())

    is_http = 1 if url.lower().startswith("http://") else 0
    
    tld = extract.suffix.lower()
    tld_risk_weight = TLD_RISK.get(tld, 0)

    free_hosting = 1 if any(h in host for h in FREE_HOSTING) else 0

    # -------- C) INTERNAS SEMÁNTICAS --------
    trusted_path_token = 1 if any(tok in path for tok in TRUSTED_TOKENS) else 0

    domain_whitelist_score = 1 if registered in SPANISH_WHITELIST else 0

    trusted_path_penalty = 1 if (trusted_path_token == 1 
                                 and domain_whitelist_score == 0) else 0

    # -------- D) INTERNAS ESTRUCTURALES --------
    normalized = path
    for sep in ["-", "_", "%20", "."]:
        normalized = normalized.replace(sep, "/")
    tokens = [t for t in normalized.split("/") if t]
    total_tokens = len(tokens)

    segments = [s for s in path.split("/") if s]
    path_depth = len(segments)

    # -------- E) FEATURES FINALES --------
    domain_complexity = domain_length * domain_entropy

    if not subdomain:
        host_entropy = 0
    else:
        freqs = Counter(subdomain)
        host_entropy = -sum((c/len(subdomain)) * log2(c/len(subdomain))
                            for c in freqs.values())

    suspicious_path_token = 1 if any(tok in path for tok in SUSPICIOUS_TOKENS) else 0

    W = suma de pesos descubiertos por SUBSTRING sobre el PATH completo:
     W = Σ(weight_t) para cada token_t en SUSPICIOUS_TOKENS_WEIGHT si token_t aparece en path.lower()

    if total_tokens == 0:
        token_density = 0
    else:
        token_density = (W / total_tokens) * (path_depth / (path_depth + 2))

    trusted_token_context = trusted_path_token - trusted_path_penalty

    infra_risk = 0.3 * is_http + tld_risk_weight + free_hosting

    fake_tld_in_subdomain_or_path = 1 if any(
    p != extract.suffix.lower() and (p in host or p in path)
    for p in FAKE_TLD_TOKENS
) else 0

    params = parse_qs(parsed.query)
    P = len(params)
    param_count_boost = P / (P + 1) if P > 0 else 0

    # -------- SALIDA CONTRACTUAL --------
    return [
        domain_complexity,
        host_entropy,
        domain_whitelist_score,
        suspicious_path_token,
        token_density,
        trusted_token_context,
        infra_risk,
        fake_tld_in_subdomain_or_path,
        param_count_boost
    ]
```


# 🧯 8. Manejo de errores

- Cualquier excepción → devolver vector de 9 ceros  
- Nunca devolver `None`  
- Nunca devolver strings  
- Siempre devolver 9 valores numéricos  
- URL vacía → vector de ceros  



# ✔ 9. Validación final de salida

Cada ejecución debe retornar:

- 9 valores  
- orden contractual  
- sin `None`, sin NaN  
- solo ints y floats  

Ejemplo válido:

```
[12.4, 1.8, 0, 1, 0.62, -1, 3.5, 1, 0.5]
```
