Feature: infra_risk — v3 FINAL
Propósito

Medir el riesgo inherente a la infraestructura donde está alojado un dominio, usando señales globalmente estables y no dependientes de ninguna campaña concreta.

🧠 Motivación técnica

Las campañas modernas de phishing orientado a España muestran patrones comunes:

TLDs de riesgo: .live, .xyz, .top, .shop, .icu, .click

Uso persistente de HTTP

Hostings gratuitos o de muy baja reputación

Proveedores masivos genéricos y fáciles de automatizar

Estas señales son invariantes en el tiempo y no dependen de la semántica del dominio ni de la víctima.

infra_risk mide únicamente el riesgo estructural del hosting.

🧱 Definición formal

La feature es la suma de tres señales independientes:

infra_risk = http_weight + tld_risk_weight + free_hosting_weight

1. HTTP penalty
+0.3 si la URL usa http://


Bancos y servicios oficiales no usan HTTP

Kits de phishing sí aparecen con HTTP con frecuencia

2. TLD risk weight

Peso según riesgo del TLD:

.live, .xyz, .top, .shop, .icu, .click → riesgo alto

.com, .net, .org → riesgo bajo

.es, .gob.es, .com.es → riesgo 0

.ru, .cn, .su, .by, .kp → riesgo extremo (peso 3.0)

Todos los valores exactos se definen en features_constantes.py.

Excepción importante:

GLOBAL_NEUTRAL_DOMAINS (Google, Microsoft, Cloudflare, Akamai…)
→ tld_risk_weight = 0
para evitar falsos positivos en proveedores globales.

3. Free hosting / low–reputation hosting
+1.0


Si el host pertenece a proveedores gratuitos clásicos incluidos en
FREE_HOSTING → riesgo elevado.

📊 Comportamiento real

Sobre dataset v2.1 (492 URLs):

Legítimas (label=0)
mean = 0.00
std  = 0.00
max  = 0.00


✔ No penaliza nunca a sitios españoles legítimos
✔ 0 falsos positivos

Phishing (label=1)
mean ≈ 1.22
std  ≈ 1.39
75% ≈ 3.0
max ≈ 3.3


✔ Señal muy informativa
✔ Captura infraestructura maliciosa real
✔ Alta amplitud → buena señal para modelos lineales y árboles

✔ Decisión de diseño

No se incluye:

patrones de campañas (ej. prefixes tipo ingress-)

dominios hackeados .es

proveedores específicos raros

reglas semánticas del dominio

infra_risk se mantiene como feature estructural pura.