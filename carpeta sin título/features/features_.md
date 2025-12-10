# 🧩 Features v2 — Ingeniería de características

**Versión:** 2.2 (implementación final consolidada)  
**Fecha de cierre:** 04/11/2025  
**Responsable:** *Alexis Zapico Fernández*  
**Archivo principal:** `features_v2.py`  
**Constantes:** `features_constantes.py`  
**Dataset base:** `dataset_full_v2_2.csv` (500 URLs: 250 phishing / 250 legítimas)

---

## 🧠 1️⃣ Objetivo

La versión 2 del módulo de *Feature Engineering* redefine por completo el enfoque del prototipo inicial para adaptarlo al **phishing moderno en España (2024–2025)**.

Las campañas actuales se caracterizan por:
- **Dominios cortos y realistas**, con HTTPS casi siempre activo.  
- **Tokens en castellano** en rutas coherentes (`/verificar`, `/paquete`, `/clientes`).  
- **Hostings temporales o baratos** (`.live`, `.app`, `.shop`, `.web.app`).  
- **Redirecciones OAuth / SSO legítimas** empleadas como disfraz.  

🎯 **Objetivo principal:**  
Reducir falsos positivos en portales oficiales y mejorar el recall en campañas recientes, añadiendo **contexto semántico y técnico** (TLD, whitelist, tokens sectoriales).

---

## ⚙️ 2️⃣ Comparativa v1 → v2

| Aspecto | v1 | v2 | Evolución |
|----------|----|----|-----------|
| Nº total de features | 10 | 14 | +4 nuevas o derivadas |
| Enfoque dominante | Estructural | Contextual / semántico | Cambio de paradigma |
| Peso de infraestructura | Alto | Bajo / contextualizado | ↓ menor dependencia |
| Uso de whitelist | No | Sí (`spanish_domains.csv`) | Legitimidad contextual |
| Señales lingüísticas | Básicas (`login`, `cliente`) | Extendidas (`verificar`, `paquete`, `sms`, `pago`) | ↑ Recall |
| Features derivadas | Ninguna | 4 combinadas | +4 interacciones |
| Foco principal | Detección genérica | Phishing real español | ↑ Precisión contextual |

---

## 🔬 3️⃣ Lista de features v2

| Feature | Tipo | Descripción breve |
|----------|------|-------------------|
| `domain_length` | Numérica | Longitud del dominio principal. |
| `domain_entropy` | Numérica | Aleatoriedad de caracteres del dominio. |
| `domain_complexity` | Numérica | Producto `entropy × length`. |
| `tld_risk_weight` | Numérica | Riesgo asociado al TLD (.live, .app, .shop, .xyz, .ru…). |
| `host_entropy` | Numérica | Aleatoriedad del subdominio (kits dinámicos). |
| `param_count_boost` | Numérica | Nº de parámetros normalizado por longitud. |
| `token_density` | Numérica | Densidad de tokens sospechosos en la ruta. |
| `trusted_token_context` | Binaria | Evalúa coherencia entre tokens legítimos y dominio oficial. |
| `suspicious_path_token` | Binaria | Tokens fraudulentos (`verificar`, `sms`, `pago`). |
| `domain_whitelist_score` | Numérica | Coincidencia exacta con dominios españoles (`spanish_domains.csv`). |
| `infra_risk` | Numérica | Riesgo técnico agregado (HTTP + TLD + hosting). |
| `oauth_like_relief` | Binaria | Reduce penalización en flujos OAuth legítimos. |
| `fake_tld_in_subdomain_or_path` | Binaria | Detecta engaños visuales (`bbva.es-login.com`). |

---

## 🧱 4️⃣ Bloques funcionales

### 🔹 Bloque 1 — Complejidad y legitimidad de dominio

- **`domain_complexity`** = `domain_length × domain_entropy`  
  Captura densidad informativa y ofuscación de dominios.  
  - Dominios cortos y simples → legítimos (`bbva.es`).  
  - Dominios largos y aleatorios → sospechosos (`authline-checkappr0v.com.es`).

- **`host_entropy`** mide la aleatoriedad del subdominio, útil para detectar kits sobre hostings legítimos.

- **`domain_whitelist_score`** valida si el dominio pertenece a la lista `spanish_domains.csv`.  
  - 1.0 → dominio oficial (`bbva.es`)  
  - 0.6 → subdominio legítimo (`clientes.bbva.es`)  
  - 0.0 → fuera de la whitelist  

📘 *Método de cálculo:*  
Basado en coincidencia exacta de `tldextract.registered_domain` contra `spanish_domains.csv` (no búsqueda por substring).

📘 *Relación:*  
`domain_complexity` y `host_entropy` aportan riesgo estructural, mientras `domain_whitelist_score` corrige falsos positivos mediante legitimidad nacional.

---

### 🔹 Bloque 2 — Contexto semántico de confianza

Feature principal: **`trusted_token_context`**

Sustituye `trusted_path_token` y `trusted_path_penalty` por una señal unificada.  
Evalúa coherencia entre los tokens legítimos (`login`, `clientes`, `banca`) y el dominio al que pertenecen:

| Caso | Ejemplo | Resultado |
|------|----------|-----------|
| Token legítimo en dominio oficial | `clientes.bbva.es/login` | +1 |
| Token legítimo en dominio falso | `bbva.es-login.com/login` | −1 |
| Sin token o neutro | `paquete-live.com/envio` | 0 |

🔁 **Dependencia interna:**  
`trusted_token_context ← trusted_path_token + domain_whitelist_score`

📈 *Impacto:*  
- Reduce FP en banca y SaaS (~−34 %).  
- Mantiene recall global en ≈ 0.91.  
- Aporta explicabilidad semántica.

---

### 🔹 Bloque 3 — Riesgo de infraestructura

`infra_risk` combina en una única métrica las señales técnicas:

\[
infra\_risk = 0.3 × is\_http + tld\_risk\_weight + free\_hosting
\]

| Componente | Descripción | Peso |
|-------------|--------------|------|
| `is_http` | 1 si la URL usa HTTP sin cifrado | 0.3 |
| `tld_risk_weight` | Riesgo del TLD (frecuencia / geopolítica) | 0–3 |
| `free_hosting` | Hosting gratuito o temporal | 1.0 |

✅ *Ventajas:*  
- Elimina duplicidades (`protocol`, `tld_risk_weight` como feature independiente).  
- El componente `is_http` mantiene un peso bajo (0.3) para evitar sobrerreacción ante sitios no cifrados.  
- Mejora estabilidad (ΔF1 ≈ ± 0.01).  
- Mantiene coherencia con *scoring v2.1*.

---

## 📖 5️⃣ Diccionario sectorial de tokens — `docs/tokens_por_sector.csv`

Define asociaciones entre tokens en castellano y su sector más probable, mejorando la sensibilidad contextual.

| Sector | Ejemplos | Rango de pesos |
|:-------|:----------|:---------------|
| Banca / Fintech | verificar, acceso, seguridad, pin, tarjeta | 0.8–2.0 |
| Logística | paquete, envio, aduanas, seguimiento, recibir | 1.0–1.5 |
| SaaS / Cloud | login, auth, portal, dashboard, soporte | 0.5–1.0 |
| Público / Gobierno | sede, tramite, cita, certificado | 0.8–1.2 |
| Cripto / Fintech | wallet, transferencia, token | 0.8–1.2 |
| Retail / e-commerce | pedido, factura, compra, devolucion | 0.5–1.0 |
| Energía / Seguros | factura, consumo, contrato, cliente | 0.5–1.0 |
| Genérico / Otros | cuenta, portal, usuario, datos | 0.5–1.0 |

📄 **Archivo:** `docs/tokens_por_sector.csv` (~70 filas)  
🧠 **Reglas de uso:**
1. Solo se aplican pesos específicos si el sector es conocido o derivable (`brand_in_path`).  
2. En caso contrario, se usa peso genérico bajo.  
3. Siempre se combina con `trusted_token_context` y `domain_whitelist_score` para evitar FP.  
4. Versionado: `tokens_suspicious_v*.csv`, revisión quincenal.

---

## 🧩 6️⃣ Dependencias internas

| Feature derivada | Componentes base | Tipo |
|-------------------|-----------------|------|
| `domain_complexity` | `domain_length`, `domain_entropy` | Auxiliar |
| `infra_risk` | `is_http`, `tld_risk_weight`, `free_hosting` | Agregada |
| `trusted_token_context` | `trusted_path_token`, `domain_whitelist_score` | Contextual |
| `token_density` | `tokens_por_sector.csv`, `SUSPICIOUS_TOKENS_WEIGHT` | Lingüística |

📎 *Nota:* Ninguna feature base y su derivada coexisten en el modelo → evita doble conteo y mejora estabilidad.

---

## 📊 7️⃣ Evidencia empírica — Drift v1→v2

| Feature | Δ (%) | Interpretación |
|----------|-------|----------------|
| `domain_length` | −44 % | Dominios más cortos y creíbles. |
| `domain_entropy` | −25 % | Menor aleatoriedad, más naturales. |
| `num_params` | +189 % | Rutas con más parámetros dinámicos. |
| `suspicious_path_token` | +33.7 pp | Incremento de rutas de acción. |

📈 *Conclusión:* el phishing español actual usa **URLs limpias y semánticamente engañosas**, lo que valida el rediseño contextual de features.

