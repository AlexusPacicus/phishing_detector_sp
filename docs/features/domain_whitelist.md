Feature: domain_whitelist (v3)
Objetivo

Identificar dominios oficiales y legítimos para garantizar cero falsos positivos, proporcionando una señal estructural de legitimidad que se utiliza en:

domain_complexity (anulación completa del riesgo)

trusted_token_context (+1 si el dominio es oficial)

reglas de scoring de nivel superior

1. Entrada

Se extrae el dominio registrado con tldextract:

registered_domain = ext.domain.lower() + "." + ext.suffix.lower()

2. Lógica
Comparación estricta:
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


Sin substrings, sin tokens parciales, sin variantes.
Ejemplo:

URL	registered_domain	En whitelist	domain_whitelist
https://bbva.es/login
	bbva.es	✔	1
https://bbva.es-login.com
	es-login.com	✖	0
3. Contenido de la whitelist (v3)

La whitelist incluye:

🇪🇸 Dominios españoles oficiales

Banca

Logística (Correos, SEUR…)

Energía / Seguros

Telecomunicaciones

Retail

Administración pública

🌍 Dominios globales neutrales

Usados masivamente en España y no asociados a phishing:

google.com

microsoft.com

bing.com

akamaihd.net

wixsite.com

cloudfront.net

github.io

etc.

(Estos aparecen en global_neutral_domains.csv.)

4. Interacciones con otras features
✔ domain_complexity

Si domain_whitelist == 1, entonces:

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
0
domain_complexity=0
✔ trusted_token_context (v28)
trusted\_token\_context = +1 \text{ si domain_whitelist = 1}
✔ brand_in_path

Solo se activa si domain_whitelist == 0.

5. Motivación

El 90% de falsos positivos en modelos sin whitelist proviene de bancos, logística o SaaS legítimos.

El registro español (.es) está muy controlado.

Evita que tokens sensibles ("clientes", "login", "seguridad") produzcan falsos positivos cuando el dominio es oficial.

Reduce ruido en dominio_complexity y host_entropy.