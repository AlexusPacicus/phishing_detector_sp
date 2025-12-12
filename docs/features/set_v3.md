🧩 DEFINICIÓN TÉCNICA OFICIAL — FEATURE SET v3
1️⃣ domain_complexity

Tipo: float
Rango esperado: 0.0 – 1.0

Definición

Mide la complejidad estructural del dominio registrado, penalizando dominios cortos y respetando dominios oficiales.

Procedimiento

Extraer registered_domain y core (núcleo sin TLD ni subdominio).

Calcular:

𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
_
𝑙
𝑒
𝑛
𝑔
𝑡
ℎ
=
𝑙
𝑒
𝑛
(
𝑟
𝑒
𝑔
𝑖
𝑠
𝑡
𝑒
𝑟
𝑒
𝑑
_
𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
)
domain_length=len(registered_domain)
𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
_
𝑒
𝑛
𝑡
𝑟
𝑜
𝑝
𝑦
=
𝐻
(
𝑐
𝑜
𝑟
𝑒
)
domain_entropy=H(core)

Normalizar rangos:

𝑛
𝑜
𝑟
𝑚
_
𝑙
𝑒
𝑛
=
min
⁡
(
𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
_
𝑙
𝑒
𝑛
𝑔
𝑡
ℎ
/
18
,
 
1
)
norm_len=min(domain_length/18, 1)
𝑛
𝑜
𝑟
𝑚
_
𝑒
𝑛
𝑡
𝑟
𝑜
𝑝
𝑦
=
min
⁡
(
𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
_
𝑒
𝑛
𝑡
𝑟
𝑜
𝑝
𝑦
/
3.8
,
 
1
)
norm_entropy=min(domain_entropy/3.8, 1)

Combinar:

𝑟
𝑎
𝑤
=
0.78
⋅
𝑛
𝑜
𝑟
𝑚
_
𝑒
𝑛
𝑡
𝑟
𝑜
𝑝
𝑦
+
0.22
⋅
𝑛
𝑜
𝑟
𝑚
_
𝑙
𝑒
𝑛
raw=0.78⋅norm_entropy+0.22⋅norm_len

Penalizar dominios cortos:

𝑟
𝑎
𝑤
=
0.35
⋅
𝑟
𝑎
𝑤
si 
𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
_
𝑙
𝑒
𝑛
𝑔
𝑡
ℎ
<
10
raw=0.35⋅rawsi domain_length<10

Si el dominio está en la whitelist española:

𝑟
𝑎
𝑤
=
0.0
raw=0.0

Reescalado final:

𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
_
𝑐
𝑜
𝑚
𝑝
𝑙
𝑒
𝑥
𝑖
𝑡
𝑦
=
𝑟
𝑎
𝑤
0.55
domain_complexity=raw
0.55
2️⃣ domain_whitelist

Tipo: int
Valores: {0, 1}

Definición

Indica si el dominio pertenece a una lista oficial de dominios españoles legítimos (o globales neutrales autorizados).

𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
_
𝑤
ℎ
𝑖
𝑡
𝑒
𝑙
𝑖
𝑠
𝑡
=
{
1
	
si registered_domain ∈ WHITELIST


0
	
en otro caso
domain_whitelist={
1
0
	​

si registered_domain ∈ WHITELIST
en otro caso
	​

Notas

Es una señal estructural de legitimidad.

Base para trusted_token_context y domain_complexity.

3️⃣ trusted_token_context (v28)

Tipo: int
Valores: {-1, 0, +1}

Definición

Contextualiza la confiabilidad del dominio combinando whitelist y coincidencias de marca del CSV.

Regla exacta
 
```
trusted_token_context =
    +1  si domain_whitelist == 1
     0  si domain_whitelist == 0 AND core ∈ brands_set
    -1  en otro caso
```

Fuentes de verdad

| Valor | Fuente | Condición |
|-------|--------|-----------|
| +1 | `docs/whitelist.csv` | Dominio oficial verificado |
| 0 | `docs/dominios_espanyoles.csv` | Marca española detectada (no oficial) |
| -1 | — | Sin señal de legitimidad |

Justificación de TTC = 0

Cuando el dominio NO está en whitelist pero SÍ coincide con una marca del CSV (`brands_set`), se asigna contexto neutro. Esto evita penalizar dominios legítimos con TLDs globales (.com, .net) que no están en whitelist oficial.

Importante

- No depende del PATH.
- `brands_set` proviene de `dominios_espanyoles.csv`, NO de whitelist.
- Limpia, estable y anti-FP.

4️⃣ host_entropy

Tipo: float
Rango: 0.0 – 3.0 aprox.

Definición

Entropía del subdominio limpio, útil para detectar subdominios aleatorios típicos de infraestructura de phishing moderna.

Procedimiento

Extraer subdomain.

Limpiar puntos:

𝑠
=
𝑠
𝑢
𝑏
𝑑
𝑜
𝑚
𝑎
𝑖
𝑛
.
𝑟
𝑒
𝑝
𝑙
𝑎
𝑐
𝑒
(
"
.
"
,
"
"
)
s=subdomain.replace(".","")

Si no hay subdominio → host_entropy = 0.

Si existe:

ℎ
𝑜
𝑠
𝑡
_
𝑒
𝑛
𝑡
𝑟
𝑜
𝑝
𝑦
=
𝐻
(
𝑠
)
host_entropy=H(s)
Notas

subdomain_missing_flag existe, pero es interna, no feature final.

5️⃣ infra_risk

Tipo: float
Rango típico: 0 – 5

Definición

Riesgo agregado asociado a la infraestructura técnica usada por la URL.

Fórmula
𝑖
𝑛
𝑓
𝑟
𝑎
_
𝑟
𝑖
𝑠
𝑘
=
0.3
⋅
𝑖
𝑠
_
ℎ
𝑡
𝑡
𝑝
+
𝑡
𝑙
𝑑
_
𝑟
𝑖
𝑠
𝑘
_
𝑤
𝑒
𝑖
𝑔
ℎ
𝑡
+
𝑓
𝑟
𝑒
𝑒
_
ℎ
𝑜
𝑠
𝑡
𝑖
𝑛
𝑔
infra_risk=0.3⋅is_http+tld_risk_weight+free_hosting

Donde:

is_http = 1 si la URL usa HTTP plano.

tld_risk_weight proviene del diccionario de TLDs de riesgo.

free_hosting = 1 si aparece un patrón de hosting gratuito o abusado.

Características

0 FPs confirmados.

Señal fuerte en phishing .live, .app, .top, .shop, .xyz.

---

## Fuente de verdad de marcas españolas

### Origen exclusivo

Las marcas españolas para `brand_in_path`, `brand_match_flag` y `trusted_token_context (0)` se derivan **exclusivamente** de:

```
docs/dominios_espanyoles.csv
```

**NO se derivan de whitelist.**

### Construcción de brands_set

```python
brands_set = constants["BRANDS_FROM_DOMAINS_ES"]
```

### Requisito de inicialización

```python
load_brands_from_domains_es(constants)
```

Debe ejecutarse **antes** de cualquier llamada a `extract_features_v3()`.

### Diferencia whitelist vs brands_set

| Aspecto | whitelist | brands_set (CSV) |
|---------|-----------|------------------|
| Fuente | `docs/whitelist.csv` | `docs/dominios_espanyoles.csv` |
| Uso | domain_whitelist, TTC +1, domain_complexity bypass | brand_match_flag, brand_in_path, TTC 0 |

---

6️⃣ brand_in_path

Tipo: int
Valores: {0, 1}

Definición

Detecta si el último segmento del path contiene una marca española conocida.

Fuente de marcas

`brands_set` derivado de `docs/dominios_espanyoles.csv` via `constants["BRANDS_FROM_DOMAINS_ES"]`.

Reglas

- Tomar `last_segment = url.split("/", 3)[-1].lower()`.
- Tokenizar según el regex exacto: `[\/\-\_\.\=\&\?\%]`.
- Comparar tokens con `brands_set`.
- Solo activar si `domain_whitelist == 0`.

Salida

- 1 si se detecta una marca válida en el path.
- 0 en caso contrario.

---

7️⃣ brand_match_flag

Tipo: int
Valores: {0, 1}

Definición

Indica si el núcleo del dominio coincide con una marca española conocida.

Fuente de marcas

`brands_set` derivado de `docs/dominios_espanyoles.csv` via `constants["BRANDS_FROM_DOMAINS_ES"]`.

Construcción

```python
brands_set = constants["BRANDS_FROM_DOMAINS_ES"]
```

Regla

```python
brand_match_flag = int(core in brands_set)
```

Salida

- 1 si el dominio coincide con una marca del CSV.
- 0 si no coincide.

Rol en TTC

`brand_match_flag == 1` con `domain_whitelist == 0` → TTC = 0 (contexto neutro).

---

## Vector contractual FINAL v3

```python
FEATURES_V3 = [
    "domain_complexity",
    "domain_whitelist",
    "trusted_token_context",
    "host_entropy",
    "infra_risk",
    "brand_in_path",
    "brand_match_flag"
]
```

## Contrato de inicialización

```python
from features.features_constantes import constants, load_brands_from_domains_es

# OBLIGATORIO antes de extract_features_v3()
load_brands_from_domains_es(constants)
```