# ⚖️ Sistema de Scoring – Versión 1

**Objetivo:** detectar campañas de phishing orientadas a España dentro de feeds globales mediante un sistema de puntuación basado en reglas lingüísticas, geográficas y de marca.

---

## ⚙️ Reglas y motivaciones

| Grupo | Regla / Indicador | Peso | Justificación |
|-------|-------------------|------|---------------|
| **Geográfico** | `.es`, `+34`, `€` | +2 / +1 | Identifican claramente origen o targeting español. |
| | `.com.es` | +2 | Estructura muy usada en campañas de phishing españolas. |
| **Lingüístico** | Palabras castellanas (`cliente`, `pago`, `factura`, `seguridad`, `envío`, `multa`, `notificación`) | +1 | Detección de idioma español. |
| **Marca nacional** | `bbva`, `santander`, `caixabank`, `ing`, `correos`, `dgt`, `movistar`, `ionos`, etc. | +1 | Marcas objetivo comunes en España. |
| **Semántico / compuesto** | `banking_combo_es`, `institutional_professional_es`, `ecommerce_combo_es` | +2 / +3 | Agrupan tokens por sector (banca, administración, comercio). |
| **Hosting local** | `webcindario`, `rf.gd` | +2 | Hostings gratuitos frecuentes en phishing español. |
| **Fuzzy matching / whitelist** | Coincidencia ≥80 % con dominios `.es` reales (Tranco) | +2 | Confirma contexto nacional. |
| **Marca + token español** | `brand_plus_spanish_token` | +2 | Detecta campañas mixtas (`app-ing.direct-ayuda.com`). |
| **Marca en subdominio** | `brand_in_subdomain` | +2 | Detecta clones (`bbva.es-login.com`, `ing.seguridad.digital`). |
| **Acortadores con tokens españoles** | `shortener_spain` | +2 | URLs cortas con `spain`, `es`, `dgt`, `bbva`, etc. |
| **Marca en TLD global** | `brand_global_tld_boost` | +1 | Recupera campañas españolas en `.com`, `.app`, `.net`. |
| **Penalizaciones** | TLD LATAM (`.co`, `.mx`, `.ar`, `.br`, `.pe`, etc.) | −2 | Filtra campañas latinoamericanas. |
| | Palabras portuguesas (`pagamento`, `fatura`, `acesso`) | −2 | Excluye campañas PT/BR. |

---

## 🔑 Umbral de decisión
- **score_total ≥ 4** → URL orientada a España (detección amplia), estas urls serán usadas para mejorar el scoring.  
- **score_total ≥ 7** → URL candidata a dataset phishing en español (alta confianza).  

---

## ✅ Resultados
- Dataset procesado: 236 URLs.  
- URLs con `score_total ≥ 7`: 69 → revisadas manualmente e incluidas en `inclusión=1`.  

---

## 💡 Justificación global
- Combina **señales lingüísticas y geográficas** priorizando `.es` y castellano.  
- Integra **marcas y subdominios** frecuentes en phishing real.  
- Controla **ruido internacional** (LATAM/PT) con penalizaciones.  
- Mantiene **explicabilidad total**: cada URL guarda las `signals_detected`.  

---

## 🔄 Nota metodológica
Las reglas y pesos se diseñaron a partir del **dataset prototipo** (200 URLs balanceadas).  
Se aplicaron sobre el nuevo feed (Phishing.Database + otros) para seleccionar las primeras URLs.  
En versiones futuras se ajustarán los pesos en base a **falsos positivos/negativos observados**, usando las urls candidadatas entre 4 y 7.  

---

**Versión:** v1 .  
**Estado:** ✅ Cerrado y aplicado a dataset real.  

---

# ⚖️ Sistema de Scoring – Versión 2  
*(Post-curación manual y ampliación del dataset)*

**Objetivo:**  
Refinar la detección de campañas de phishing orientadas a España aplicando nuevas reglas lingüísticas y de infraestructura, basadas en la validación manual de 468 URLs (209 clasificadas con inclusión=1).

---

## 🔁 Principales mejoras frente a la versión 1

| Tipo | Mejora | Descripción |
|------|---------|-------------|
| **Infraestructura** | Detección de *free hosting* | Se añaden patrones `easywp`, `replit`, `web.app`, `tempsite.link` con pesos positivos (+2). |
| **Comprometidos** | Identificación automática de dominios `.es` legítimos infectados | Se crea categoría `comprometida_es` (no para entrenamiento, solo análisis). |
| **Lingüístico** | Nuevos tokens de logística | `paquete`, `aduanas`, `envio`, `recibir`, `pago` (+2). |
| **Financiero** | Detección de kits 3D Secure | Tokens `verificacion`, `3d`, `no-back-button` (+3). |
| **Penalizaciones** | Campañas LATAM | `banreservas`, `bancoestado`, `banrural`, `daviplata`, `itau`, `bradesco` (−3). |
| **Falsos positivos** | Filtrado `.es` técnico | Penaliza `/wp-`, `/css/`, `/plugins/`, `/vendor/phpunit` (−2). |

---

## 🧱 Categorías nuevas de infraestructura

| Categoría | Descripción | Ejemplo |
|------------|-------------|----------|
| `easywp_es` | Hosting gratuito EasyWP con contenido en español. | `ingress-baronn.ewp.live` |
| `free_hosting_es` | Servicios gratuitos (`replit.app`, `web.app`, `rf.gd`) usados en campañas españolas. | `anularpagosbc.replit.app` |
| `comprometida_es` | Web legítima `.org`, `.dev`, `.com` con rutas fraudulentas. | `amgmarketing.org/correos/` |
| `kit_3dsecure_es` | Plantillas genéricas de verificación bancaria en español. | `/verificacion-user/.../3d/no-back-button` |
| `logistica_sin_marca` | Campañas Correos o SEUR sin logo visible, pero tokens (`paquete`, `aduanas`, `pago`). | `pagomente`, `recibir_paquete.php` |

---

## 🔑 Umbrales actualizados

| Rango | Interpretación | Uso |
|--------|----------------|-----|
| `score ≥ 12` | Alta confianza (campañas confirmadas de phishing en España). | Ampliación del dataset y reentrenamiento. |
| `7 ≤ score < 12` | Confianza media. | Revisión manual en próximas tandas. |
| `4 ≤ score < 7` | Potencialmente útiles. | Para mejorar reglas y ajustar pesos. |
| `< 4` | Ruido o no orientado a España. | Excluido. |

---

## 🧠 Lecciones aprendidas del v2

- **Falsos positivos corregidos:** campañas LATAM con tokens en español.  
- **Nuevos patrones detectados:** kits 3D Secure y hostings EasyWP.  
- **Ruido controlado:** dominios `.es` con contenido técnico ya filtrados.  
- **Documentación estructurada:** 209 URLs curadas manualmente (sectores banca y logística dominantes).  

---

## 🚀 Plan para versión 3

1. Reentrenar el modelo con `primer_phishingrepo.csv` (URLs inclusión=1).  
2. Analizar los logs de inferencia y scoring → ajustar pesos.  
3. Incorporar features nuevas:  
   - `infraestructura_score` (ponderación por tipo de host).  
   - `semantic_tokens_weight` (tokens lingüísticos de sector).  
   - `host_entropy` (detección de subdominios aleatorios).  
4. Documentar reglas emergentes en `scoring_v3.md`.

---

**Versión:** v2.0  
**Estado:** ✅ Cerrado y listo para reentrenamiento  
**Responsable:** Alexis Zapico Fernández  
**Fecha:** 2025-10-15  
---

## 🔍 Búsqueda semántica y detección de orientación española *(Fase 3 – pendiente de implementación)*

Como parte de la futura integración con **PostgreSQL + pgvector**, el proyecto incorporará una capa de **búsqueda vectorial semántica** para mejorar la detección de campañas orientadas a España.

### 🎯 Objetivo
Identificar automáticamente si una URL nueva **“se parece”** a campañas españolas previas, usando **similitud del coseno sobre embeddings multilingües**.  
Esto permitirá:
- Reforzar el **scoring heurístico** con señales semánticas.  
- Detectar variantes de campañas o clones que el sistema de reglas no capture.  
- Reducir la necesidad de reglas lingüísticas manuales.  

### 🧠 Descripción técnica
1. **Generación de embeddings**
   - Se empleará un modelo multilingüe ligero (`paraphrase-multilingual-MiniLM-L12-v2`) o embeddings de subpalabras (`fastText-es`).
   - Cada URL confirmada como española se vectoriza y se almacena en PostgreSQL con `pgvector`.

2. **Búsqueda por similitud del coseno**
   - Para cada nueva URL del feed global:
     1. Se genera su embedding.
     2. Se calcula la **similitud del coseno** con las URLs españolas ya registradas.
     3. Si `sim ≥ 0.75`, se etiqueta como *probablemente orientada a España*.
     4. Se puede sumar un boost en el `score_total` (`+3`), con señal: `semantic_similarity_es`.

3. **Uso previsto**
   - Mejora automática de la clasificación lingüística.  
   - Clustering de campañas españolas similares.  
   - Posible reemplazo parcial del scoring lingüístico manual en futuras versiones.

4. **Ejemplo SQL (pgvector)**
   ```sql
   SELECT url, score_total
   FROM urls_clean
   ORDER BY embedding <-> '[vector_de_la_nueva_url]'
   LIMIT 5;
