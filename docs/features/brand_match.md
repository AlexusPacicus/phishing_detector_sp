# Feature: brand_match_flag — Especificación v3 FINAL

**Estado:** CERRADO  
**Posición en vector:** 7  
**Dependencia crítica:** `constants["BRANDS_FROM_DOMAINS_ES"]`

---

## 1. Definición

Indica si el núcleo del dominio (`core`) coincide exactamente con una marca española conocida.

| Atributo | Valor |
|----------|-------|
| Tipo | int |
| Valores | {0, 1} |

---

## 2. Fuente de verdad de marcas españolas

### 2.1 Origen

Las marcas se derivan **exclusivamente** de `docs/dominios_espanyoles.csv`.

**NO se derivan de:**
- Whitelist
- Dataset de entrenamiento
- Listas manuales

### 2.2 Construcción de `brands_set`

```python
brands_set = constants["BRANDS_FROM_DOMAINS_ES"]
```

### 2.3 Requisito de inicialización

```python
load_brands_from_domains_es(constants)
```

Debe ejecutarse **antes** de cualquier llamada a `extract_features_v3()`.

---

## 3. Algoritmo

### 3.1 Extracción del núcleo

```python
import tldextract

ext = tldextract.extract(url)
core = ext.domain.lower()
```

El `core` es el núcleo del dominio sin TLD ni subdominio.

### 3.2 Comparación

```python
brand_match_flag = int(core in brands_set)
```

---

## 4. Ejemplos

| URL | Core | En brands_set | Resultado |
|-----|------|---------------|-----------|
| `https://santander.es/particulares` | santander | ✓ | 1 |
| `https://bbva.com/login` | bbva | ✓ | 1 |
| `https://bbva-seguridad.live/verify` | bbva-seguridad | ✗ | 0 |
| `https://sites.google.com/phishing` | google | ✓ | 1 |
| `https://random-host.xyz/bbva` | random-host | ✗ | 0 |

---

## 5. Rol en trusted_token_context (TTC)

`brand_match_flag` alimenta la lógica de TTC:

| Condición | TTC |
|-----------|-----|
| `domain_whitelist == 1` | +1 |
| `domain_whitelist == 0` AND `brand_match_flag == 1` | 0 |
| resto | -1 |

**Justificación de TTC = 0:**  
Cuando el dominio NO está en whitelist pero SÍ coincide con una marca española del CSV, se asigna contexto neutro (0). Esto evita penalizar dominios legítimos que usan TLDs globales (.com, .net) y no están en la whitelist oficial.

---

## 6. Propiedades

| Propiedad | Valor |
|-----------|-------|
| Legítimas (media) | ~0.73 |
| Phishing (media) | ~0.04 |
| Falsos positivos críticos | 0 |

### 6.1 Casos donde phishing activa (aceptable)

- Google Sites (`sites.google.com`)
- GitHub Pages (`*.github.io`)
- Blogspot (`*.blogspot.com`)
- Dominios .es comprometidos

Ninguno representa un falso positivo real; son infraestructura neutra.

---

## 7. Relación con otras features

| Feature | Relación |
|---------|----------|
| domain_whitelist | brand_match_flag complementa para dominios .com/.net legítimos |
| trusted_token_context | brand_match_flag determina TTC = 0 |
| brand_in_path | Sin solapamiento; brand_match_flag analiza dominio, brand_in_path analiza path |

---

## 8. Diferencia con whitelist

| Aspecto | whitelist | brands_set (CSV) |
|---------|-----------|------------------|
| Fuente | `docs/whitelist.csv` | `docs/dominios_espanyoles.csv` |
| Contenido | Dominios oficiales verificados | Dominios .es por ranking Tranco |
| Uso | domain_whitelist, TTC +1 | brand_match_flag, brand_in_path, TTC 0 |
| Tamaño | ~300 dominios | ~200 dominios |

---

*Feature contractual del vector v3.*
