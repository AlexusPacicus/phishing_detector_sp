# Features v3 — Documento Técnico

**Versión:** 3.0  
**Estado:** CONTRACTUAL  
**Fecha:** Diciembre 2024

---

## 1. Limpieza de whitelist v3

### 1.1 Contexto

La whitelist original contenía dominios que no correspondían al propósito del detector de phishing español:

- Infraestructura global (CDNs, hosting, SaaS)
- Plataformas internacionales sin presencia específica ES
- Contenido adulto o irrelevante para seguridad

Estos dominios distorsionaban `domain_whitelist` y `trusted_token_context`, generando falsos negativos potenciales.

### 1.2 Limpieza aplicada

| Atributo | Valor |
|----------|-------|
| Script | `scripts/clean_whitelist_v3.py` |
| Fecha | Diciembre 2024 |
| Backup | `docs/whitelist_backup_*.csv` |

### 1.3 Dominios eliminados

| Categoría | Dominios | Motivo |
|-----------|----------|--------|
| Infraestructura/SaaS global | vercel.app, vercel.com, render.com, s3.amazonaws.com, cloudfront.net, fastly.net, akamaiedge.net, cloudflare.com, digitalocean.com, cloudinary.com, akamai.com | Hosting neutro usado por phishing |
| Plataformas globales | google.com, google.es, gmail.com, youtube.com, facebook.com, instagram.com, meta.com, microsoft.com, office.com, office365.com, outlook.com, paypal.com, stripe.com, slack.com, zoom.us | No son marcas españolas; phishing los suplanta |
| Desarrollo/DevOps | github.com, gitlab.com, bitbucket.org, atlassian.com, okta.com, auth0.com, oracle.com, salesforce.com, aws.amazon.com | Infraestructura técnica global |
| Ecommerce global | shopify.com, cdn.shopify.com, dropbox.com, dropboxusercontent.com | Plataformas internacionales |
| Contenido adulto | xnxx.es, xvideos.es | Irrelevante para seguridad |
| Medios/lifestyle | vogue.es, glamour.es, revistavanityfair.es, fotogramas.es, bonviveur.es, fragrantica.es, tvguia.es | Sin valor de seguridad |
| Otros | webnode.es, blogspot.com.es, blogs.es, windows.net | Hosting gratuito/neutro |

### 1.4 Resultado

| Métrica | Antes | Después | Δ |
|---------|-------|---------|---|
| Total dominios | ~295 | 245 | -50 |
| Dominios ES reales | ~200 | ~200 | 0 |
| Infraestructura global | ~50 | 0 | -50 |

---

## 2. Efecto en features v3

### 2.1 domain_whitelist

| Métrica | Valor |
|----------|-------|
| Dominios en whitelist | 245 |
| Cobertura legítimas | ~33% activan whitelist=1 |
| Cobertura phishing | 0% (ningún phishing en whitelist) |

**Interpretación:** Whitelist más estricta reduce falsos negativos por hosting neutro.

### 2.2 trusted_token_context

| Valor TTC | Distribución esperada |
|-----------|----------------------|
| +1 (whitelist) | ~33% legítimas |
| 0 (marca en dominio) | ~40% legítimas |
| -1 (resto) | ~27% legítimas, 100% phishing |

**Interpretación:** TTC +1 ahora indica exclusivamente dominios españoles oficiales verificados.

### 2.3 Invariantes preservados

| Invariante | Estado |
|------------|--------|
| Schema whitelist.csv | ✓ Sin cambios (columna `domain`) |
| NaN en features | ✓ 0 NaN |
| Tipos de datos | ✓ Sin cambios |
| Orden FEATURES_V3 | ✓ Inmutable |

---

## 3. Alineación con contrato v3

### 3.1 Verificación de consistencia

| Elemento | MANIFIESTO_V3 | Pipeline actual | Estado |
|----------|---------------|-----------------|--------|
| Whitelist path | `docs/whitelist.csv` | `docs/whitelist.csv` | ✓ Alineado |
| Loader | `load_whitelist_v3()` | `load_whitelist_v3()` | ✓ Alineado |
| Dominios | — | 245 | ✓ Documentado |
| Schema | columna `domain` | columna `domain` | ✓ Alineado |

### 3.2 Impacto en extracción

| Componente | Impacto |
|------------|---------|
| `extract_features_v3()` | Sin cambios de código |
| `initialize_v3()` | Sin cambios de código |
| Metadata JSON | Checksum de whitelist actualizado |

### 3.3 Compatibilidad

| Artefacto | Compatible |
|-----------|------------|
| dataset_v3_features.csv | ✓ Regenerable con whitelist limpia |
| Modelo .joblib v3 | ⚠ Requiere reentrenamiento si existía |
| scoring_v3.py | ✓ Compatible |

---

## 4. Justificación técnica

### 4.1 Por qué eliminar infraestructura global

Los dominios como `github.com`, `cloudflare.com` o `vercel.app` son infraestructura neutra:

- Phishing los usa legítimamente para hosting
- Whitelistearlos genera falsos negativos
- No son "marcas españolas" a proteger

### 4.2 Por qué eliminar plataformas internacionales

Dominios como `google.com`, `paypal.com`, `microsoft.com`:

- Son objetivos frecuentes de phishing (suplantación)
- Whitelistearlos bloquea detección de phishing que los imita
- El detector se enfoca en marcas españolas, no globales

### 4.3 Por qué mantener ~245 dominios

| Criterio | Justificación |
|----------|---------------|
| Dominios .es oficiales | Banca, teleco, logística, administración pública española |
| Dominios .com de marcas ES | bbva.com, santander.com, mapfre.com |
| Exclusión de hosting | Evita falsos negativos por infraestructura neutra |

---

## 5. Trazabilidad

| Archivo | Rol | Estado |
|---------|-----|--------|
| `docs/whitelist.csv` | Whitelist v3 limpia | 245 dominios |
| `docs/whitelist_backup_*.csv` | Backup pre-limpieza | Histórico |
| `scripts/clean_whitelist_v3.py` | Script de limpieza | Ejecutado |
| `scripts/analyze_whitelist_v3.py` | Análisis de whitelist | Referencia |

---

## 6. Checklist de validación

- [x] Whitelist limpia (245 dominios)
- [x] Schema preservado (columna `domain`)
- [x] Sin NaN en features tras re-extracción
- [x] TTC +1 ≈ 33% legítimas
- [x] Contrato v3 alineado con pipeline actual
- [x] Sin cambios de código en extractores
- [x] Backup creado antes de limpieza

---

*Documento técnico de features v3. Alineado con MANIFIESTO_V3.*
