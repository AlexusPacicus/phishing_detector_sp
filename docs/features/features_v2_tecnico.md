# 🧩 Features v2 — Especificación técnica (Parte 1: Features finales)

**Versión:** v2  
**Estado:** cerrado  
**Responsable:** Alexis Zapico Fernández  
**Ámbito:** Especificación técnica del vector final de características para el modelo v2  
**Dependencias:** `features_constantes.py`, `spanish_whitelist`, `tokens_por_sector.csv`

---

# 🎯 1. Objetivo

Este documento define **las 9 features finales** que genera `features_v2.py`.  
Son las únicas señales que se entregan al modelo y forman el **schema oficial de salida** del extractor.

Recogen información estructural, semántica, contextual y técnica del phishing moderno en España.

Este documento **NO cubre** fórmulas internas ni parsing (eso corresponde a *Parte 2*).

---

# 🧱 2. Output schema v2 (orden contractual)

El extractor debe devolver **exactamente** este vector, en **este orden**:

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


Sin columnas adicionales y sin alterar el orden.

---

# 🧩 3. Features finales — Definición técnica

## 1) domain_complexity
- **Tipo:** float  
- **Rango esperado:** 0–25  
- **Descripción:**  
  Complejidad del dominio principal basada en `entropía × longitud`.  
  Captura dominios cortos o limpios usados en campañas modernas.

---

## 2) host_entropy
- **Tipo:** float  
- **Rango esperado:** 0–3  
- **Descripción:**  
  Entropía Shannon del **subdominio**.  
  Detecta subdominios aleatorios en hostings temporales (web.app, repl.co, ewp.live…).

---

## 3) domain_whitelist_score
- **Tipo:** int  
- **Rango esperado:** {0,1}  
- **Descripción:**  
  1 si el `registered_domain` está en la whitelist española.  
  0 si no.

---

## 4) suspicious_path_token
- **Tipo:** int  
- **Rango esperado:** {0,1}  
- **Descripción:**  
  1 si el path contiene tokens sospechosos en castellano  
  (verificar, pago, recibir, paquete, envio, aduanas, sms, 3dsecure…).  
  0 si no aparece ninguno.

---

## 5) token_density
- **Tipo:** float  
- **Rango esperado:** 0–2 aprox  
- **Descripción:**  
  Densidad semántica fraudulenta.  
  Combina pesos base (`SUSPICIOUS_TOKENS_WEIGHT`) y pesos sectoriales (`tokens_por_sector.csv`),  
  normalizados por número de tokens y profundidad del path.

---

## 6) trusted_token_context
- **Tipo:** int  
- **Rango esperado:** {-1, 0, +1}  
- **Descripción:**  
  Señal contextual de legitimidad:  
  - **+1:** token legítimo en dominio oficial  
  - **-1:** token legítimo en dominio falso  
  - **0:** sin token de confianza o sin contexto

---

## 7) infra_risk
- **Tipo:** float  
- **Rango esperado:** 0–5  
- **Descripción:**  
  Riesgo técnico agregado:  
  `0.3·is_http + tld_risk_weight + free_hosting`  
  Detecta TLD de riesgo, HTTP no seguro y hosting temporal.

---

## 8) fake_tld_in_subdomain_or_path
- **Tipo:** int  
- **Rango esperado:** {0,1}  
- **Descripción:**  
  1 si el subdominio o el path contienen TLDs falsos incrustados  
  (es-, es., -es, com-, gob-, es-login…).  
  0 si no.

---

## 9) param_count_boost
- **Tipo:** float  
- **Rango esperado:** 0–0.9  
- **Descripción:**  
  Captura el drift hacia callbacks y flujos dinámicos.  
  Normalización:  
  `param_count / (param_count + 1)`.

---

# 🧱 4. Dependencias internas (NO exportadas)

Estas variables internas se utilizan para construir las features finales:

- `domain_length`  
- `domain_entropy`  
- `is_http`  
- `free_hosting`  
- `tld_risk_weight`  
- `trusted_path_token`  
- `trusted_path_penalty`  
- `total_tokens`  
- `path_depth`

Las fórmulas exactas se documentarán en **Parte 2**.

---

# 🧩 5. Estado del documento

✔ Features finales cerradas  
✔ Tipos y rangos definidos  
✔ Orden contractual definido  
✔ Coherente con Features v2 (conceptual)  
✘ Pendiente: fórmulas internas (Parte 2)

---


