Feature: trusted_token_context_v28 — Versión Final v3
Tipo: int
Valores: +1, 0, -1
Rol: señal contextual de legitimidad estructural del dominio
🎯 Objetivo

Modelar la coherencia estructural del dominio en relación con marcas españolas, sin usar tokens del path ni semántica léxica.
Esta feature NO detecta phishing por sí misma:
modula el comportamiento del modelo combinándose con domain_complexity, infra_risk y host_entropy.

1. Inputs

domain_whitelist → 1 si el dominio es oficial o está en la whitelist extendida (ES + global neutral).

brand_match_flag_v2 → 1 si el dominio contiene una marca española legítima (bbva, santander, caixabank, correos…).

2. Regla exacta (implementación real)
if domain_whitelist == 1:
    TTC = +1
elif brand_match_flag_v2 == 1:
    TTC = 0
else:
    TTC = -1


Esto significa:

✔ +1 → dominio oficial español / infraestructura autorizada

(CaixaBank, BBVA, Santander, Correos, etc.)

✔ 0 → dominio con marca española pero NO oficial

(Ej.: bankinter.com, pccomponentes.com, bbva.com
o incluso dominios ilegítimos que contienen la marca).

Esto es intencionado:
TTC ≠ detector de marca fraudulenta.
Ese rol lo tiene brand_in_path.

✔ –1 → cualquier dominio sin marca ni legitimidad

Es el caso esperado para phishing.

3. Motivación del diseño
✔ Eliminación total de token_flag

La versión v28 elimina el análisis léxico del path.
Evita falsos positivos debidos a login, clientes, acceso, etc., que son comunes en webs legítimas.

✔ Uso exclusivo de señales estructurales

domain_whitelist aporta legitimidad garantizada

brand_match_flag_v2 evita castigos a dominios legítimos con marca

El resto se considera incoherente

Es estable, reproducible y anticontaminación

✔ TTC v28 NO clasifica

TTC se combina con:

domain_complexity

infra_risk

host_entropy

suspicious_path_token

brand_in_path

para reforzar el contexto del dominio, NO para decidir si algo es phishing.

4. Interpretación
Valor	Significado
+1	Dominio oficial / whitelisted. Se espera ver rutas sensibles.
0	Marca española legítima o conocida, pero dominio no oficial.
–1	Dominio desconocido, sin marca, incoherente con usos legítimos.
5. Comportamiento esperado en dataset real

Legítimos: valores cercanos a 0 o +1

Phishing: valores cerca de –1

Diferencia estadística clara entre clases

Falsos positivos ≈ 0 por diseño

6. Estado

FEATURE CERRADA — versión oficial v3

Sin dependencia del path

Sin tokens

Sin ambigüedades

100% coherente con la implementación real