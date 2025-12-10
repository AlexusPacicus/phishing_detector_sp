1. Objetivo

La versión v3 del módulo de Feature Engineering define un conjunto mínimo, estable y altamente explicable de 7 features, diseñadas para maximizar la robustez, interpretabilidad y generalización en la detección de phishing dirigido a usuarios en España.

El set v3 elimina señales ruidosas, redundantes o dependientes del dataset, y conserva únicamente aquellas que:

capturan propiedades estructurales del dominio,

modelan riesgo real de infraestructura,

incorporan legitimidad y marcas españolas,

y mantienen cero falsos positivos en dominios oficiales.

🧱 2. Vector contractual (orden fijo)

El extractor debe devolver exactamente este vector de 7 elementos, en este orden:

FEATURES_V3 = [
    "domain_complexity",
    "domain_whitelist",
    "trusted_token_context",
    "host_entropy",
    "infra_risk",
    "brand_in_path",
    "brand_match_flag"
]


Este orden es contractual:
se utiliza en el entrenamiento, scoring, despliegue y documentación.

📦 3. Definición breve de las features

A continuación se describe qué mide cada feature y por qué es relevante.
Las fórmulas completas están en los README específicos de cada una.

1) domain_complexity

Tipo: float (0–1)
Qué mide: complejidad estadística del dominio registrado mediante entropía + longitud + penalización de dominios cortos + whitelist dura.
Por qué importa: los dominios de phishing presentan patrones anómalos en estructura y diversidad de caracteres.

2) domain_whitelist

Tipo: {0, 1}
Qué mide: si el dominio pertenece a la whitelist oficial (dominios españoles y proveedores globales legítimos).
Por qué importa: evita falsos positivos y sirve como ancla de legitimidad para TTC.

3) trusted_token_context (TTC v28)

Tipo: {–1, 0, +1}
Qué mide: el contexto estructural del dominio según legitimidad y marca:

+1 → dominio whitelisted

0 → dominio no oficial pero con marca española válida

–1 → resto
Por qué importa: proporciona contexto fiable sin analizar el contenido del path.

4) host_entropy

Tipo: float
Qué mide: entropía de Shannon del subdominio (sin normalizar).
Por qué importa: los kits modernos generan subdominios aleatorios para ocultar hosting barato.

5) infra_risk

Tipo: float
Qué mide: riesgo inherente a la infraestructura del dominio:

penalización HTTP

peso por TLD de riesgo

hosting gratuito / baja reputación
Por qué importa: captura patrones globales estables de phishing.

6) brand_in_path

Tipo: {0, 1}
Qué mide: presencia de una marca española en el path, mediante token exacto, solo si el dominio no es legítimo.
Por qué importa: detecta campañas reales que incrustan la marca en la ruta en vez de en el dominio.

7) brand_match_flag

Tipo: {0, 1}
Qué mide: coincidencia exacta entre el núcleo del dominio y una marca española oficial.
Por qué importa: evita penalizar dominios legítimos que usan .com o .net, y refuerza TTC.

🧬 4. Principios de diseño del set v3

Explicabilidad total: cada feature captura un concepto único y entendible.

No redundancia: ninguna feature replica lo que mide otra.

Cero doble conteo: no se mezclan signals de forma redundante.

Estabilidad temporal: el set no depende de campañas concretas.

Compatibilidad con LR y XGBoost: todas las features funcionan bien tanto lineal como no linealmente.

Tolerancia a falsos positivos: dominio_whitelist y TTC bloquean el ruido.

Escalabilidad: cada feature se puede extender en v4 sin romper v3.

🧪 5. Validación empírica (resumen)
Feature	Legítimas	Phishing	Observación
domain_complexity	bajo	alto	muy discriminativa
domain_whitelist	1	0	cero FPs
TTC_v28	+1/0	–1	separa legitimidad estructural
host_entropy	bajo	moderado-alto	detecta kits
infra_risk	0	alto	separa infraestructura
brand_in_path	0	~20%	buena señal de abuso
brand_match_flag	~0.7	~0.03	sólida