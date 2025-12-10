Feature Engineering — Versión v3 (CERRADA)

Objetivo:
La versión v3 define un conjunto de 7 features estructurales diseñadas para separar de forma robusta:

phishing masivo (kits, infra barata, subdominios sintéticos)

phishing técnico moderado

URLs legítimas españolas oficiales

proveedores globales legítimos con rutas técnicas

v3 no aborda phishing profesional ultra-limpio. Eso se cubrirá en v4.

🧱 1. Vector de salida (orden contractual)
[
  domain_complexity,
  domain_whitelist,
  trusted_token_context,
  host_entropy,
  infra_risk,
  brand_in_path,
  brand_match_flag
]

🔢 2. Definición matemática de features
2.1 domain_complexity ∈ [0,1]

Medida derivada de:

nº de tokens del host

entropía Shannon del host

longitud relativa
Cuanto más complejo el dominio → mayor puntaje.

2.2 domain_whitelist ∈ {0,1}

1 si el registered_domain pertenece a tu whitelist española + global fiable.

2.3 trusted_token_context ∈ {-1,0,1}

Evalúa coherencia semántica:

+1 → token legítimo + dominio whitelisted

0 → token neutro

-1 → token legítimo en dominio no-whitelist (señal fuerte de spoofing)

2.4 host_entropy ≥ 0

Entropía Shannon del subdominio.
Detecta subdominios artificiales típicos de kits (3.0–4.5+).

2.5 infra_risk ≥ 0

infra_risk = http_flag + tld_risk_weight + free_hosting_weight
Detecta infraestructura barata, hosting masivo y TLD tóxicos.

2.6 brand_in_path ∈ {0,1}

1 si el PATH contiene tokens de marcas reales españolas en ausencia de dominio oficial.

2.7 brand_match_flag ∈ {0,1}

1 si el registered_domain coincide con la marca oficial reconocida
(banco/entidad española).

📊 3. Resultados EDA (resumen)
✔ signals_on = 4

100% phishing.
0 falsos positivos.

✔ signals_on = 3

Separación perfecta. Legitimos whitelisted vs phishing masivo.

✔ signals_on = 2

Separación moderada gracias a domain_complexity.
Contiene phishing técnico y legítimos técnicos.

✔ signals_on = 1

Zona conflictiva natural:

legítimos internacionales técnicos

phishing profesional limpio

No es un fallo: es un límite estructural del enfoque v3.

✔ No hay features rotas ni inconsistencias.
⚠️ 4. Limitaciones conocidas de v3

No distingue phishing profesional ultra-limpio.

Depende de whitelist para legitimidad.

host_entropy no separa en casos técnicos limpios.

domain_complexity domina en casos ambiguos.

No se procesan acortadores (se excluirán).

No hay análisis semántico (v4 lo incorporará).

📌 5. Estado del extractor

La versión v3 queda oficialmente congelada.
No se añadirán ni modificarán features.
Las mejoras pertenecen a features_v4 (semántica, lexical, homografía).