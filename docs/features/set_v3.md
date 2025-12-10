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

Contextualiza la confiabilidad del dominio combinando la whitelist y coincidencias de marca.

Regla exacta
𝑡
𝑟
𝑢
𝑠
𝑡
𝑒
𝑑
_
𝑡
𝑜
𝑘
𝑒
𝑛
_
𝑐
𝑜
𝑛
𝑡
𝑒
𝑥
𝑡
=
{
+
1
	
si 
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
1


0
	
si 
𝑏
𝑟
𝑎
𝑛
𝑑
_
𝑚
𝑎
𝑡
𝑐
ℎ
=
1


−
1
	
en otro caso
trusted_token_context=
⎩
⎨
⎧
	​

+1
0
−1
	​

si domain_whitelist=1
si brand_match=1
en otro caso
	​

Importante

No depende del PATH.

Limpia, estable y anti-FP.

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

6️⃣ suspicious_path_token

Tipo: int
Valores: {0, 1}

Definición

Indica si el PATH contiene tokens léxicos de phishing robustos definidos en tu diccionario actual.

Ejemplos:
verificar, confirmar, pago, paquete, envio, 3dsecure, sms, etc.

Regla
𝑠
𝑢
𝑠
𝑝
𝑖
𝑐
𝑖
𝑜
𝑢
𝑠
_
𝑝
𝑎
𝑡
ℎ
_
𝑡
𝑜
𝑘
𝑒
𝑛
=
{
1
	
si existe alg
u
ˊ
n token sospechoso en el PATH


0
	
si no
suspicious_path_token={
1
0
	​

si existe alg
u
ˊ
n token sospechoso en el PATH
si no
	​

7️⃣ brand_in_path

Tipo: int
Valores: {0, 1}

Definición

Detecta abuso explícito de marca en el PATH cuando la URL no es legítima.

Procedimiento

Tokenizar PATH por separadores duros (-, _, /, %20, .).

Comparar tokens con la lista de marcas españolas.

Activar solo si domain_whitelist == 0.

Regla
𝑏
𝑟
𝑎
𝑛
𝑑
_
𝑖
𝑛
_
𝑝
𝑎
𝑡
ℎ
=
{
1
	
si marca_espa
n
˜
ola_tokenizada ∈ PATH y domain_whitelist=0


0
	
en otro caso
brand_in_path={
1
0
	​

si marca_espa
n
˜
ola_tokenizada ∈ PATH y domain_whitelist=0
en otro caso
	​

Notas

Cero falsos positivos confirmados.

Extremadamente útil en logística y banca españolas.