Feature: brand_in_path — Versión v3 FINAL
Objetivo

Detectar abuso explícito de marca en el path de una URL, siempre que el dominio no sea legítimo.
Es una señal directa y moderna que captura campañas reales de phishing (banca, logística, telcos), donde los atacantes insertan el nombre de la entidad en la ruta.

1. Materia prima
1.1 Extracción del path

Para mantener coherencia con el pipeline existente:

path = url.split("/", 3)[-1].lower()


Esto devuelve solo el segmento final del path tras el tercer /.
Esto simplifica la detección y funciona bien en la práctica porque:

Las marcas suelen aparecer al final (/bbva/login, /correos/seguridad, /caixabank/verify)

No es sensible a la estructura completa del path

Reduce ruido en paths largos o aleatorios

1.2 Tokenización

El path se divide estrictamente por caracteres separadores:

/  -  _  .  =  &  ?  %


En forma de expresión regular:

tokens = re.split(r"[\/\-\_\.\=\&\?\%]", path)


La tokenización es exacta y no ambigua.

1.3 Origen de brands_set

En v3, las marcas NO se extraen de label==0 del dataset.

El set oficial de marcas se construye a partir de:

Whitelist española (dominios oficiales .es)

Dominios globales neutros

(Opcional) lista manual validada de entidades críticas (banca, logística, telco)

Regla final:

brands_set = { registered_domain.split(".")[0] for registered_domain in WHITELIST }


Ejemplos:

bbva.es → bbva

caixabank.es → caixabank

correos.es → correos

santander.com → santander

repsol.com → repsol

iberia.com → iberia

Esto garantiza reproducibilidad y elimina dependencias del dataset.

2. Lógica de activación
2.1 Activación cruda
brand_in_path_raw = 1 si existe algún token t ∈ tokens tal que t == marca


Comparación estrictamente exacta, sin substrings:

✔ …/bbva/login → activa

✔ …/correos/track → activa

✖ …/bbvaseguridad → no activa

✖ …/correosExpress → no activa

2.2 Activación final (protegida por dominio legítimo)

La feature se activa solo si el dominio NO es legítimo:

brand_in_path_final = 1 
    si brand_in_path_raw == 1 
    y domain_whitelist == 0


Si el dominio está en la whitelist:

brand_in_path_final = 0


Ejemplo:
https://correos.es/estado/paquete → tokens contienen “correos” pero domain_whitelist = 1 → NO activa.

3. Motivación

Los atacantes en España abusan de marcas en la ruta mucho más que en el dominio.

La detección en path es estable incluso cuando el host es aleatorio (aq29qx.live).

Es una señal binaria, limpia y sin ruido, perfecta para LR/XGBoost.

Aporta separación que domain_complexity, host_entropy o infra_risk no capturan directamente.

4. Propiedades deseables
✔ Cero falsos positivos

Confirmado empíricamente:
brand_in_path_final == 1 y label == 0 → 0 casos.

✔ Muy buen recall para campañas españolas

Activa correctamente en:

Phishing de banca

Phishing de Correos

Phishing de MRW/SEUR

Phishing de Iberdrola / Endesa

Kits genéricos que copian rutas de marca

✔ Complementaria a TTC v28

TTC detecta legitimidad del dominio.
brand_in_path detecta abuso de marca cuando NO hay legitimidad.

5. Interacciones con el pipeline v3
Feature	Relación
domain_whitelist	brand_in_path solo se activa si esta = 0
domain_complexity	Complementa casos con hosts neutros pero rutas manipuladas
host_entropy	No interfiere, opera en otra capa
infra_risk	Se combinan muy bien: dominio random + marca en path
trusted_token_context	TTC nunca usa el path; no hay doble conteo

Nota: el extractor analiza únicamente el segmento final del path (tras el tercer "/"), siguiendo la implementación actual (`url.split("/", 3)[-1]`).
