# 🧩 Features v2 — Especificación técnica completa (Parte 3: Fórmulas + Pseudocódigo)

**Versión:** v2  
**Estado:** cerrado  
**Responsable:** Alexis Zapico Fernández  
**Ámbito:** Especificación técnica final del extractor v2 (funcionamiento completo).  
**Dependencias:**  
- `features_v2_tecnico.md` (documento unificado Parte 1+2)  
- `features_constantes.py`  
- `spanish_whitelist`  
- `tokens_por_sector.csv`

---

# 🎯 1. Objetivo

Esta parte define:

- el **orden exacto de cálculo** del extractor v2,  
- las **fórmulas finales definitivas**,  
- la **matriz de dependencias**,  
- el **pseudocódigo contractual** del módulo,  
- el **manejo de errores**,  
- y el **formato final de salida**.

Este documento cierra el diseño del Feature Engineering v2 y permite implementar `features_v2.py` sin ambigüedades.

---

# 🧱 2. Orden obligatorio del pipeline

El extractor debe operar en este orden:

## **A) Parsing inicial**
1. obtener `extract = tldextract.extract(url)`  
2. obtener `parsed = urlparse(url)`  
3. normalizar:  
   - `domain = extract.domain.lower()`  
   - `registered = extract.registered_domain.lower()`  
   - `subdomain = extract.subdomain.lower()`  
   - `path = parsed.path.lower()`  
   - `host = parsed.netloc.lower()`

---

## **B) Features internas básicas**
1. `domain_length`  
2. `domain_entropy`  
3. `is_http`  
4. `tld_risk_weight`  
5. `free_hosting`

---

## **C) Features internas semánticas**
6. `trusted_path_token`  
7. `trusted_path_penalty`  

---

## **D) Features internas estructurales**
8. `total_tokens`  
9. `path_depth`

---

## **E) Features finales (en este orden)**
1. `domain_complexity`  
2. `host_entropy`  
3. `domain_whitelist_score`  
4. `suspicious_path_token`  
5. `token_density`  
6. `trusted_token_context`  
7. `infra_risk`  
8. `fake_tld_in_subdomain_or_path`  
9. `param_count_boost`

---

# 🧮 3. Fórmulas finales completas

## 1. **domain_complexity**
\[
domain\_complexity = domain\_length \times domain\_entropy
\]

---

## 2. **host_entropy**
\[
host\_entropy = H(subdomain)
\]

Donde H es entropía Shannon de `extract.subdomain.lower()`.

---

## 3. **domain_whitelist_score**
\[
domain\_whitelist\_score =
\begin{cases}
1 & registered\_domain \in whitelist \\
0 & \text{si no}
\end{cases}
\]

---

## 4. **suspicious_path_token**
\[
suspicious\_path\_token =
\begin{cases}
1 & \exists t \in SUSPICIOUS\_TOKENS: t \in path \\
0 & \text{si no}
\end{cases}
\]

---

## 5. **token_density**

Sea:  
- \( W = \sum \) de pesos (tokens sospechosos + sectoriales)  
- \( T = total\_tokens \)  
- \( D = path\_depth \)

\[
token\_density =
\left(
\frac{W}{T}
\right)
\times
\left(
\frac{D}{D + 2}
\right)
\]

Si \( T = 0 \) → 0.

---

## 6. **trusted_token_context**
\[
trusted\_token\_context = trusted\_path\_token - trusted\_path\_penalty
\]

Resultado ∈ { -1, 0, +1 }

---

## 7. **infra_risk**
\[
infra\_risk = 
0.3 \cdot is\_http 
+ tld\_risk\_weight 
+ free\_hosting
\]

---

## 8. **fake_tld_in_subdomain_or_path**
\[
fake\_tld\_in\_subdomain\_or\_path =
\begin{cases}
1 & \exists p \in FAKE\_TLD\_TOKENS: p \in subdomain \lor p \in path \\
0 & \text{si no}
\end{cases}
\]

---

## 9. **param_count_boost**

Sea \( P = \# \) de parámetros query.

\[
param\_count\_boost = 
\begin{cases}
\frac{P}{P + 1} & P > 0 \\
0 & P = 0
\end{cases}
\]

---

# 🧬 4. Matriz de dependencias

| Feature final | Internas necesarias |
|---------------|---------------------|
| domain_complexity | domain_length, domain_entropy |
| host_entropy | subdomain entropy |
| domain_whitelist_score | registered_domain |
| suspicious_path_token | path (normalizado) |
| token_density | total_tokens, path_depth, pesos sectoriales |
| trusted_token_context | trusted_path_token, trusted_path_penalty |
| infra_risk | is_http, tld_risk_weight, free_hosting |
| fake_tld_in_subdomain_or_path | FAKE_TLD_TOKENS, path, subdomain |
| param_count_boost | param_count |

---

# 👨‍💻 5. Pseudocódigo contractual completo

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

    # 1. domain_length
    domain_length = len(registered) if registered else 0

    # 2. domain_entropy
    if not domain:
        domain_entropy = 0
    else:
        freqs = Counter(domain)
        domain_entropy = -sum((c/len(domain)) * log2(c/len(domain))
                              for c in freqs.values())

    # 3. is_http
    is_http = 1 if url.lower().startswith("http://") else 0

    # 4. tld_risk_weight
    tld = extract.suffix.lower()
    tld_risk_weight = TLD_RISK.get(tld, 0)

    # 5. free_hosting
    free_hosting = 1 if any(h in host for h in FREE_HOSTING) else 0

    # -------- C) INTERNAS SEMÁNTICAS --------

    # 6. trusted_path_token
    trusted_path_token = 1 if any(tok in path for tok in TRUSTED_TOKENS) else 0

    # 7. trusted_path_penalty
    domain_whitelist_score = 1 if registered in SPANISH_WHITELIST else 0
    trusted_path_penalty = 1 if (trusted_path_token == 1 
                                 and domain_whitelist_score == 0) else 0

    # -------- D) INTERNAS ESTRUCTURALES --------

    # 8. total_tokens
    normalized = path
    for sep in ["-", "_", "%20", "."]:
        normalized = normalized.replace(sep, "/")
    tokens = [t for t in normalized.split("/") if t]
    total_tokens = len(tokens)

    # 9. path_depth
    segments = [s for s in path.split("/") if s]
    path_depth = len(segments)

    # -------- E) FEATURES FINALES --------

    # 1. domain_complexity
    domain_complexity = domain_length * domain_entropy

    # 2. host_entropy
    if not subdomain:
        host_entropy = 0
    else:
        freqs = Counter(subdomain)
        host_entropy = -sum((c/len(subdomain)) * log2(c/len(subdomain))
                            for c in freqs.values())

    # 3. domain_whitelist_score (ya calculado)

    # 4. suspicious_path_token
    suspicious_path_token = 1 if any(tok in path for tok in SUSPICIOUS_TOKENS) else 0

    # 5. token_density
    W = compute_weight_sum(tokens)   # pesos base + sectoriales
    if total_tokens == 0:
        token_density = 0
    else:
        token_density = (W / total_tokens) * (path_depth / (path_depth + 2))

    # 6. trusted_token_context
    trusted_token_context = trusted_path_token - trusted_path_penalty

    # 7. infra_risk
    infra_risk = 0.3 * is_http + tld_risk_weight + free_hosting

    # 8. fake_tld_in_subdomain_or_path
    fake_tld_in_subdomain_or_path = 1 if any(p in subdomain or p in path
                                             for p in FAKE_TLD_TOKENS) else 0

    # 9. param_count_boost
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

---

# 🧯 6. Manejo contractual de errores

- Ante cualquier excepción → **todas las internas = 0**  
- No se puede devolver `None`  
- No se pueden devolver strings  
- La salida debe ser SIEMPRE una lista de 9 valores numéricos  
- URL vacía o inválida → vector de **9 ceros**

Esto evita romper pipelines y garantiza robustez en entornos SOC/ETL.

---

# 🧪 7. Validación final de salida

Cada llamada a `extract_features_v2(url)` debe devolver:

- ✔ 9 valores  
- ✔ orden contractual  
- ✔ sin `None`  
- ✔ sin NaN  
- ✔ ints y floats únicamente  

Ejemplo válido:

```
[12.4, 1.8, 0, 1, 0.62, -1, 3.5, 1, 0.5]
```

---

# ✔ Fin de la Parte 3
