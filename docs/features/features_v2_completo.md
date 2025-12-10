# 🧩 Features v2 — Especificación técnica completa  
**Versión:** v2  
**Estado:** cerrado  
**Responsable:** Alexis Zapico Fernández  
**Ámbito:** Especificación técnica unificada del vector final de características y las features internas del extractor v2.  
**Dependencias:**  
- `features_constantes.py`  
- `spanish_whitelist`  
- `tokens_por_sector.csv`

---

# 🎯 1. Objetivo

Este documento consolida **todas las features finales e internas** utilizadas por `features_v2.py`.  
Define el diseño contractual del extractor v2, incluyendo:

- Esquema de salida (9 features finales)  
- Tipos y rangos  
- Definiciones técnicas  
- Features internas necesarias para construir las finales  

Este archivo es la referencia oficial para implementación, mantenimiento y auditoría del Feature Engineering v2.

---

# 🧱 2. Output schema v2 (orden contractual)

El extractor debe devolver **exactamente** este vector, en este orden:

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

## 1) **domain_complexity**
**Tipo:** float  
**Rango:** 0–25  
**Descripción:**  
Complejidad del dominio principal basada en:  
`domain_length × domain_entropy`.

---

## 2) **host_entropy**
**Tipo:** float  
**Rango:** 0–3  
**Descripción:**  
Entropía Shannon del subdominio (`extract.subdomain`).  
Detecta subdominios aleatorios o generados automáticamente (web.app, repl.co, ewp.live…).

---

## 3) **domain_whitelist_score**
**Tipo:** int  
**Rango:** {0,1}  
**Descripción:**  
1 si `registered_domain` ∈ whitelist española.  
0 en cualquier otro caso.

---

## 4) **suspicious_path_token**
**Tipo:** int  
**Rango:** {0,1}  
**Descripción:**  
1 si el path contiene tokens sospechosos en castellano  
(verificar, pago, paquete, envio, aduanas, sms, 3dsecure…).  
0 si no.

---

## 5) **token_density**
**Tipo:** float  
**Rango:** 0–2 aprox  
**Descripción:**  
Densidad semántica fraudulenta de la ruta, combinando:

- pesos base (`SUSPICIOUS_TOKENS_WEIGHT`)  
- pesos sectoriales (`tokens_por_sector.csv`)  
- normalización por número de tokens (`total_tokens`)  
- profundización estructural (`path_depth`)

---

## 6) **trusted_token_context**
**Tipo:** int  
**Rango:** {-1,0,+1}  
**Descripción:**  
Contexto de legitimidad según ruta y dominio:

- **+1:** token legítimo + dominio oficial  
- **-1:** token legítimo + dominio falso  
- **0:** no aplica  

Depende de `trusted_path_token` y `trusted_path_penalty`.

---

## 7) **infra_risk**
**Tipo:** float  
**Rango:** 0–5  
**Descripción:**  
Riesgo técnico agregado:  
`0.3·is_http + tld_risk_weight + free_hosting`.

---

## 8) **fake_tld_in_subdomain_or_path**
**Tipo:** int  
**Rango:** {0,1}  
**Descripción:**  
1 si el subdominio o el path contienen TLDs falsos incrustados  
(es-, -es, com-, gob-, es-login…).  
0 si no.

---

## 9) **param_count_boost**
**Tipo:** float  
**Rango:** 0–0.9  
**Descripción:**  
Captura el drift hacia URLs con callbacks y flujos dinámicos.  
Normalización:  
`param_count / (param_count + 1)`.

---

# 🧬 4. Features internas — Definición técnica

Estas features **NO se exportan**, pero son necesarias para construir las finales.

---

## 🔹 1) `domain_length`
**Tipo:** int  
**Definición:** longitud del `registered_domain`.

```python
domain = extract.registered_domain.lower()
domain_length = len(domain) if domain else 0
```

---

## 🔹 2) `domain_entropy`
**Tipo:** float  
**Definición:** entropía Shannon de `extract.domain`.

```python
domain = extract.domain.lower()
if not domain:
    entropy = 0
else:
    entropy = -sum((c/len(domain)) * log2(c/len(domain)) for c in counts)
```

---

## 🔹 3) `is_http`
**Tipo:** int  
**Definición:** 1 si la URL empieza por `"http://"`; 0 si no.

---

## 🔹 4) `tld_risk_weight`
**Tipo:** float  
**Definición:**  
Peso según `TLD_RISK`.

```python
tld = extract.suffix.lower()
tld_risk_weight = TLD_RISK.get(tld, 0)
```

---

## 🔹 5) `free_hosting`
**Tipo:** int  
**Definición:**  
1 si el `netloc` contiene hostings temporales (web.app, repl.co, ewp.live…).

```python
host = urlparse(url).netloc.lower()
free_hosting = 1 if any(h in host for h in FREE_HOSTING) else 0
```

---

## 🔹 6) `trusted_path_token`
**Tipo:** int  
**Definición:**  
1 si el path contiene tokens legítimos de `TRUSTED_TOKENS`.

```python
path = urlparse(url).path.lower()
trusted_path_token = 1 if any(t in path for t in TRUSTED_TOKENS) else 0
```

---

## 🔹 7) `trusted_path_penalty`
**Tipo:** int  
**Definición:**  

```python
trusted_path_penalty = 1 if (
    trusted_path_token == 1 and 
    domain_whitelist_score == 0
) else 0
```

---

## 🔹 8) `total_tokens`
**Tipo:** int  
**Definición:** tokens del path tras normalización de separadores.

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
**Definición:** número de segmentos del path (solo por `/`).

```python
path = urlparse(url).path.lower()
segments = [s for s in path.split("/") if s]
path_depth = len(segments)
```

---

# ✔ 5. Estado del documento

- Features finales **cerradas**  
- Features internas **cerradas**  
- Esquema contractual definido  
- Total coherencia con diseño v2  
- Listo para implementación en `features_v2.py`

---

# ✔ Fin del documento
