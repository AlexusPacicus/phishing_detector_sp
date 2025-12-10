# 🧠 Análisis de errores y features – Inclusión v2 (FN / FP)

**Fecha:** 28/10/2025  
**Responsable:** Alexis Zapico Fernández  
**Modelo:** `logreg_phishing_final.joblib` (v1 – prototipo)  
**Dataset:** `eval_set_inclusion_v2.csv` (150 phishing / 150 legítimas)

---

## 1️⃣ Contexto general

Este análisis consolida los resultados obtenidos durante la validación del modelo del prototipo (v1) sobre el conjunto de datos **Inclusion v2**.  
El objetivo es **entender los patrones de error del modelo** (falsos negativos y falsos positivos) y analizar **las features reales** empleadas en las predicciones, con el fin de rediseñar el módulo `features_v2.py` y preparar el reentrenamiento.

---

## 2️⃣ Distribución de errores

| Tipo | Cantidad | % sobre total (300) |
|------|-----------|--------------------:|
| Falsos negativos (FN) | 25 | 8.3 % |
| Falsos positivos (FP) | 19 | 6.3 % |
| Aciertos (TP + TN) | 256 | 85.3 % |

> Los falsos negativos representan principalmente campañas en **hosting .live** o kits genéricos no vistos en el entrenamiento,  
> mientras que los falsos positivos provienen de **portales legítimos con rutas sensibles** (`/login`, `/clientes`, `/portal`).

---

## 3️⃣ Análisis sectorial

### 🟥 Falsos negativos
| Sector | % | Entidades principales |
|:-------|--:|:----------------------|
| **Genérico / Otros** | 44 % | Sitios sin marca evidente o kits genéricos (.live) |
| **Banca** | 32 % | Santander, BBVA, CaixaBank |
| **Logística** | 24 % | Correos España, SEUR |

**Conclusión:**  
El modelo pierde recall en **campañas genéricas** y **kits bancarios o logísticos modernos** no presentes en el prototipo.

---

### 🟦 Falsos positivos
| Sector | % | Entidades afectadas |
|:-------|--:|:--------------------|
| **Banca** | 22 % | `/login`, `/clientes`, `/seguridad` |
| **SaaS / Cloud / Plataformas** | 22 % | Auth0, Stripe, Microsoft |
| **Administración Pública** | 22 % | `sede.gob.es`, Seguridad Social |
| **Cripto / Fintech** | 17 % | Binance, Coinbase |
| Otros | 17 % | Logística, energía |

**Conclusión:**  
El modelo penaliza tokens legítimos (“login”, “portal”, “clientes”) sin verificar si el dominio pertenece a una fuente oficial.

---

## 4️⃣ Análisis por TLD

| TLD | Tipo de error | Observaciones |
|------|----------------|----------------|
| **.live** | 80 % de los FN | Hosting EasyWP / Namecheap. Patrón nuevo no visto en el prototipo. |
| **.com** | 15 % FN / 66 % FP | Dominios globales (`paypal.com`, `stripe.com`) confundidos por tokens. |
| **.es** | 5 % FN / 33 % FP | Portales legítimos del Estado y banca confundidos por rutas complejas. |

**Conclusión:**  
Existe un **drift de infraestructura**, con nuevos TLDs (`.live`, `.app`, `.shop`) y un modelo incapaz de reconocerlos como sospechosos.

---

## 5️⃣ Tokens más comunes

### 🟥 Falsos negativos
```
login.php, clients, acceso, correos, recibir_paquete.php, pagoconyfirmacion, pagomente_spain
```
➡️ *Patrones clásicos pero mal generalizados. El modelo ya no reacciona ante kits PHP o tokens mixtos español/inglés.*

### 🟦 Falsos positivos
```
sede, portal, particulares, home, faqs, atencioclient
```
➡️ *Tokens legítimos confundidos con señales de phishing por falta de contexto semántico.*

---

## 6️⃣ Análisis de features

### 📈 Comparativa de medias por tipo de error

| Feature | FN | FP | OK | Interpretación |
|----------|----|----|----|----------------|
| **domain_length** | 4.2 | 10.8 | 7.0 | FN usan dominios muy cortos (kits `.live`); el modelo no penaliza suficiente. |
| **domain_entropy** | 1.85 | 2.96 | 2.30 | FN tienen baja entropía (nombres simples); el modelo los considera legítimos. |
| **protocol** | 1.0 | 1.0 | 0.87 | HTTPS está presente en casi todos los FN; el modelo no lo trata como factor neutro. |
| **trusted_path_token** | 0.68 | 0.00 | 0.16 | Tokens de confianza (`clientes`, `banca`, `login`) en phishing engañan al modelo. |
| **suspicious_path_token** | 0.64 | 0.22 | 0.49 | Señal útil, pero con peso insuficiente. |
| **num_params** | 0.20 | 0.17 | 0.16 | Diferencias mínimas; aporta poco valor. |
| **contains_equal / contains_percent** | 0.00 | 0.11 / 0.00 | 0.06 / 0.04 | Sin correlación clara; prescindibles. |
| **prob_phish** | 0.23 | 0.61 | 0.45 | Correcta separación de confianza; FN muy infraponderados. |

---

### 🔴 Falsos negativos (phishing no detectado)
- **Dominios cortos y simples** (`domain_length` bajo, `entropy` baja).  
- **Tokens de confianza en rutas** (`clientes`, `banca`, `login`) generan sesgo hacia “legítimo”.  
- **HTTPS presente en todos los FN**, el modelo lo interpreta como señal de legitimidad.  
- **Conclusión:** el modelo **no entiende el contexto**: detecta las palabras, pero no si el dominio es fiable.

### 🔵 Falsos positivos (legítimas mal clasificadas)
- **Dominios largos y con alta entropía**, penalizados por parecer ofuscados.  
- **Estructuras complejas o rutas con parámetros** (`sede`, `portal`, `particulares`) penalizadas erróneamente.  
- **Conclusión:** el modelo **sobrerreacciona ante la complejidad estructural** y no reconoce dominios oficiales.

---

## 7️⃣ Diagnóstico técnico por feature

| Feature | Estado actual | Recomendación |
|----------|----------------|----------------|
| **domain_length** | Discriminativa pero invertida | Reforzar peso negativo (dominios cortos → phishing). |
| **domain_entropy** | Correlacionada con error | Añadir `domain_complexity = domain_entropy * domain_length`. |
| **protocol** | Saturada (casi siempre 1) | Eliminar o combinar con `tld_risk_weight`. |
| **trusted_path_token** | Alta en FN | Crear `trusted_path_penalty`: solo penaliza si dominio no es oficial. |
| **suspicious_path_token** | Útil pero infrautilizada | Aumentar peso o interacción con `tld_risk_weight`. |
| **num_params / contains_equal / contains_percent** | Débil | Eliminar del feature set. |

---

## 8️⃣ Implicaciones y próximos pasos

1. **Añadir nuevas features**
   - `domain_complexity` → relación longitud × entropía.  
   - `tld_risk_weight` → ponderar `.live`, `.app`, `.shop`, etc.  
   - `trusted_path_penalty` → contextualizar tokens de confianza.  
   - `host_entropy` → detectar subdominios aleatorios (`secure-login.ewp.live`).

2. **Eliminar features obsoletas**
   - `protocol`, `contains_equal`, `contains_percent`, `num_params`.

3. **Ajustar pesos y umbral**
   - Aumentar peso de `suspicious_path_token`.  
   - Elevar umbral de decisión: **0.425 → 0.50**.

4. **Incluir whitelisting semántico**
   - Feature `domain_whitelist_score` → 1 si pertenece a entidades oficiales (bancos, SaaS, administración).

---

## 9️⃣ Conclusión

El modelo del prototipo mantiene un rendimiento sólido, pero **pierde sensibilidad ante nuevas infraestructuras y rutas mixtas**.  
Los falsos negativos se concentran en **kits genéricos (.live)** y los falsos positivos en **portales oficiales sin contexto semántico**.  
La revisión de `features_v2.py` debe centrarse en **añadir contexto de dominio y riesgo por TLD**, eliminando señales estructurales redundantes.

> 🔁 Resultado esperado tras el rediseño: reducción de falsos negativos en campañas `.live` y mejora de recall sin aumento de falsos positivos.
