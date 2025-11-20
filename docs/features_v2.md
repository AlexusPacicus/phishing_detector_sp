

# 🧩 Features v2 — Ingeniería de características

**Versión:** v2  
**Archivo asociado:** `features_v2.py`  
**Constantes:** `features_constantes.py`  
**Whitelist:** `docs/dominios_espanyoles.csv`  
**Tokens sectoriales:** `docs/tokens_por_sector.csv`

---

# 🧠 1. Objetivo

La versión **v2** del módulo de *Feature Engineering* redefine el sistema de señales utilizadas para detectar **phishing orientado a usuarios en España**.

Este rediseño surge como respuesta a:

- La comparación entre el los dato del prototipo y los nuevos.
- Kits modernos con dominios limpios y rutas en castellano (`/verificar`, `/paquete`, `/sms`)  
- El auge de TLDs de riesgo (`.live`, `.app`, `.shop`)  
- Los falsos positivos en portales oficiales españoles  
- Los falsos negativos en campañas recientes muy realistas  

El objetivo principal de v2 es:

### **📌 Maximizar el recall en campañas modernas y reducir falsos positivos**,  
utilizando features semánticas, de legitimidad y de riesgo agregadas, sin doble conteo.

---

# 🔍 2. Filosofía del diseño v2

La versión v2 elimina:

- Features internas que solo sirven como materia prima  
- Señales redundantes del prototipo  
- Features estructurales débiles (`protocol`, `contains_%`, `contains_=`…)  
- Doble conteo entre señales relacionadas  

y establece tres principios:

1. **Solo features agregadas finales** → nunca sus componentes internos.  
2. **Semántica española como señal principal** → rutas y tokens.  
3. **Legitimidad y riesgo contextual** → whitelist .es + infraestructura moderna.

---

# 🎯 3. Feature set final v2 (9 features)

Estas son **las únicas 9 features finales**, limpias y sin redundancia.  
Son las que se exportan al CSV y las que recibe el modelo.

---

## 📦 1) Complejidad y estructura de dominio

### **1. `domain_complexity`**
Mide densidad informativa del dominio a partir de longitud y entropía combinadas.  
Captura dominios *demasiado limpios para ser legítimos*, característicos de phishing moderno.

---

### **2. `host_entropy`**
Entropía del **subdominio**.  
Detecta kits montados en hosting temporal (`web.app`, `repl.co`, `tempsite.link`).

---

## 🛡️ 2) Legitimidad de dominio (contexto español)

### **3. `domain_whitelist_score`**
- **1** → dominio oficial o subdominio correcto incluido en la whitelist española  
- **0** → resto  

Reduce falsos positivos en banca, SaaS y administración.

---

## 🧠 3) Semántica en castellano

### **4. `suspicious_path_token`**
Detecta tokens clave en español utilizados en campañas reales:

- verificar  
- pago  
- recibir  
- confirmar  
- paquete  
- sms  
- aduanas  
- 3dsecure  

---

### **5. `token_density`**
Densidad normalizada de tokens sospechosos en la ruta.  
Combina:

- pesos individuales (`SUSPICIOUS_TOKENS_WEIGHT`)  
- sectores (`tokens_por_sector.csv`)  
- estructura de ruta (profundidad, tokens totales)

Es la **feature lingüística principal** del sistema.

---

### **6. `trusted_token_context`**
Sustituye a:

- `trusted_path_token`  
- `trusted_path_penalty`

**Valores:**

| Caso | Ejemplo | Valor |
|------|---------|--------|
| Token legítimo en dominio oficial | `clientes.bbva.es/login` | +1 |
| Token legítimo en dominio falso  | `bbva.es-login.com/login` | −1 |
| Neutro | sin token | 0 |

Corrige falsos positivos en rutas sensibles (`/login`, `/clientes`, `/portal`).

---

## 🌐 4) Infraestructura y riesgo

### **7. `infra_risk`**
Feature agregada que combina:

- HTTP (peso bajo, 0.3)  
- riesgo por TLD (`.live`, `.app`, `.shop`, `.xyz`, `.ru`, `.cn`)  
- hosting gratuito o temporal (`free_hosting`)  

---

### **8. `fake_tld_in_subdomain_or_path`**
Detecta engaños visuales:

- `bbva.es-login.com`  
- `ing.es.seguridad-app.net`  
- `/correos.es/paquete`

---

## 🔍 5) Complejidad de ruta

### **9. `param_count_boost`**
Captura el *drift confirmado* (+189%) hacia rutas con más callbacks, tokens y flujos dinámicos.

---

# 🧬 4. Dependencias internas (solo referencia)

Estas **NO son features finales**, pero alimentan las features superiores:

| Interna | Usada por | Función |
|---------|-----------|---------|
| domain_length | domain_complexity | estructura |
| domain_entropy | domain_complexity | estructura |
| is_http | infra_risk | infraestructura |
| free_hosting | infra_risk | infraestructura |
| tld_risk_weight | infra_risk | infraestructura |
| trusted_path_token | trusted_token_context | semántica |
| trusted_path_penalty | trusted_token_context | semántica |

v2 **evita el doble conteo** manteniendo solo las agregadas.

---

# 📊 5. Drift cuantitativo (Prototipo → v2)

| Señal | Drift | Impacto |
|-------|-------|---------|
| `domain_length` | −44 % | Dominios más cortos y creíbles |
| `domain_entropy` | −25 % | Menor aleatoriedad → ataques más limpios |
| `num_params` | +189 % | Más rutas dinámicas y callbacks |
| `suspicious_path_token` | +33.7 pp | Auge de tokens de acción en español |

v2 prioriza semántica y legitimidad por encima de señales estructurales antiguas.

---

# 🧪 6. Checklist técnico

✓ Solo se exportan 9 features finales
✓ No hay doble conteo entre features internas y finales
✓ domain_whitelist_score usa domininios oficiales españoles
✓ token_density usa diccionario sectorial real
✓ infra_risk combina TLD + HTTP + hosting de forma unificada
✓ Feature set compacto, estable y explicable


---

# 🧱 7. Estado final

- **Versión:** v2  
- **Estado:** cerrado y validado  
- **Compatibilidad:** modelo v2 + scoring v2.1  
- **Dataset base:** inclusión v2 (500 URLs)

---

# 🧩 8. Conclusión

El feature set **v2** ofrece:

- Mayor recall en campañas modernas  
- Menos falsos positivos en portales oficiales  
- Señales estables, agregadas y explicables  
- Eliminación total de redundancias  
- Base sólida para el reentrenamiento del modelo v2 y el desarrollo del scoring v3

> **v2 representa la primera versión madura del sistema de features para phishing español.**

# 🧩 9. Limitaciones conocidas (v2)
V2 presenta limitaciones técnicas que deben tenerse en cuenta para evitar interpretaciones erróneas:

1️⃣ Cobertura sectorial desigual

Los sectores SaaS, cripto, retail y energía están infrarrepresentados en el dataset actual.
Esto puede reducir la sensibilidad del modelo en targets poco frecuentes.

2️⃣ token_density depende del diccionario sectorial

El diccionario requiere mantenimiento periódico (revisión quincenal).

Si aparecen nuevos tokens de campañas reales, la feature puede quedar temporalmente desactualizada.

3️⃣ infra_risk no captura anomalías avanzadas

La feature unifica HTTP + TLD + hosting, pero no detecta señales complejas como:

servidores comprometidos

fingerprinting de paneles de phishing

comportamiento dinámico (redirecciones, JS)
Estas quedarán para v3.

4️⃣ trusted_token_context depende de la whitelist

Si la whitelist no incorpora una entidad española nueva (banco, SaaS, administración),
pueden aparecer falsos positivos en rutas sensibles (/login, /clientes, /portal).

5️⃣ No incluye señales semánticas profundas

v2 aún trabaja únicamente con features estáticas de URL.
Las señales semánticas (embeddings, pgvector) forman parte del diseño de v3.
