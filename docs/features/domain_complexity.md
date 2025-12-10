domain_complexity_v23 — Especificación FINAL (opción A)
Objetivo

Medir la complejidad real del dominio registrado para detectar phishing moderno, penalizando nombres de dominio demasiado cortos (patrón típico en España) y estableciendo una whitelist dura para garantizar cero falsos positivos en dominios legítimos.

1. Materia prima

Para una URL:

registered_domain: dominio registrado (ej. bbva.es)

core: parte sin TLD (ej. bbva)

whitelist: conjunto de dominios legítimos validados

2. Señales internas
2.1 Longitud del dominio
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
2.2 Entropía del núcleo
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
3. Combinación principal (peso a entropía)
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
4. Penalización explícita a dominios cortos (<10)

Los dominios muy cortos son extremadamente frecuentes en phishing moderno español.

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
:
𝑟
𝑎
𝑤
=
𝑟
𝑎
𝑤
⋅
0.35
si domain_length<10:raw=raw⋅0.35

Es una penalización fuerte y deliberada, alineada con el patrón actual de campañas bancarias y logísticas falsas.

5. Whitelist DURA

Si el dominio está en la whitelist:

𝑟
𝑎
𝑤
=
0
raw=0

Esto garantiza cero falsos positivos en:

bancos españoles reales

logística

energía / seguros

portales oficiales

SaaS global legítimo

6. Reescalado final (no lineal)
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
(
𝑟
𝑎
𝑤
)
0.55
domain_complexity=(raw)
0.55
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
∈
[
0
,
1
]
domain_complexity∈[0,1]

El exponente <1 amplifica diferencias en la zona media sin saturar el extremo alto.

7. Comportamiento esperado
✔ Phishing español moderno (dominios cortos falsos)

0.60 – 1.00

Ejemplos reales:

ing-clientes.app

bbva-seguridad.top

correos-verif.info

✔ Dominios legítimos en whitelist

0.00 exacto

✔ Dominios legítimos no-whitelist pero estables

0.10 – 0.40 típicamente

✔ Hosts comprometidos .es, Google Sites, IPs

≈ 0.00 (correcto, este no es el rol de la feature)