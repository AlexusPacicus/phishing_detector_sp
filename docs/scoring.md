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

**Versión:** v1 (v2.6 estable).  
**Estado:** ✅ Cerrado y aplicado a dataset real.  
