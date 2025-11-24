

#  Features v2 — Ingeniería de características

**Versión:** v2   
**Constantes:** `features_constantes.py`  
**Whitelist:** `docs/dominios_espanyoles.csv`  
**Tokens sectoriales:** `docs/tokens_por_sector.csv`


# 1. Objetivo

La versión v2 del módulo de Feature Engineering redefine las señales utilizadas para detectar phishing orientado a usuarios en España.

Este rediseño surge tras analizar +500 URLs reales (phishing y legítimas) procedentes de campañas modernas. El EDA revló un cambio claro respecto al prototipo:

- Dominios más cortos y limpios.
- Rutas más profundas y con más parámetros.
- Tokens de acción en castellano.
- Desaparición de hostings gratuitos clásicos.
- Aumento de TLDs de riesgo (.live, .app, .shop).
v2 reduce el feature set a solo 9 señales finales, todas agregadas y libres de doble conteo, optimizadas para el modelo v2

La versión v1 no capturaba estos patrones, lo que generaba falsos negativos en campañas recientes y falsos positivos en portales oficiales.

El objetivo de v2 es construir un conjunto de features compacto, explicable y alineado con el phishing moderno, que:

- Priorice la semántica española real.
- Combine legitimidad de dominio + riesgo de infraestructura moderna.
- Elimine señales débiles o redundantes.
- Maximice el recall sin disparar falsos positivos.

v2 reduce el feature set a solo 9 señales finales, todas agregadas, coherentes entre sí y libres de doble conteo, optimizadas para el modelo v2.

# 2. Principios de diseño

El diseño de Features v2 se basa en tres principios fundamentales que garantizan un feature set compacto, explicable y adaptado al phishing moderno:
- Solo features finales agregadas:
Se eliminan señales internas, derivadas o redundantes.
Cada feature representa una señal única.
- Semántica española base:
El phishing actual en España se caracteriza por rutas con tokens de acción en castellano (verificar, recibir, paquete, pago, sms).
El sistema prioriza estas señales reales frente a heurísticas estructurales antiguas (protocol, símbolos, %, =).
- Riesgo por infraestructura moderna:
Las campañas actuales utilizan TLDs “limpios” (.live, .app, .shop) y subdominios generados en hostings temporales.
v2 integra legitimidad (domain_whitelist_score) con riesgo (infra_risk) en una sola capa coherente.

# 3. Feature set final (9 señales)
Estas son las 9 features finales de la versión v2.
No hay señales internas, duplicadas ni componentes intermedios.

A) Complejidad y estructura de dominio

1. domain_complexity
Tipo: Métrica estructural agregada
Para qué sirve: Detecta dominios demasiado simples o manipulados.
Qué problema resuelve: Los kits modernos usan dominios cortos y “limpios” que engañan a reglas basadas en longitud bruta.
Claves: Combina longitud + entropía → una señal más estable.
$$
domain_complexity = domain_length \cdot domain_entropy
$$

 2. host_entropy
Tipo: Métrica estructural
Para qué sirve: Detecta subdominios generados automáticamente.
Qué problema resuelve: Muchos ataques usan hostings temporales (web.app, repl.co, tempsite.link) con subdominios aleatorios.

B) Legitimidad de dominio
3. domain_whitelist_score
Tipo: Señal binaria de legitimidad
Para qué sirve: Distingue dominios oficiales españoles (banca, SaaS, administración).
Qué problema resuelve: Reduce falsos positivos en rutas sensibles (/login, /clientes).
Valores:
1 → dominio pertenece a entidad oficial
0 → resto

C) Semántica española (tokens reales)
4. suspicious_path_token
Tipo: Señal semántica
Para qué sirve: Detecta tokens usados en campañas reales: verificar, pago, recibir, paquete, sms, aduanas, etc.
Qué problema resuelve: El phishing moderno se apoya más en semántica que en ofuscación.

5. token_density
Tipo: Señal semántica avanzada
Para qué sirve: Cuantifica la densidad de tokens sospechosos según:
 - ruta
 - profundidad
 - pesos sectoriales
Qué problema resuelve: Evita que un único token aislado genere ruido y da más peso a rutas coherentes con campañas reales.
### Fórmula
$$
token\_density = \frac{\sum pesos}{total\_tokens} \cdot \frac{path\_depth}{path\_depth + 2}
$$

6. trusted_token_context
Tipo: Señal contextual
Para qué sirve: Distingue tokens legítimos en dominios legítimos VS tokens legítimos en dominios falsos.
Qué problema resuelve: Falsos positivos en rutas oficiales y falsos negativos en clones bancarios.

D) Infraestructura y riesgo

7.infra_risk
Tipo: Señal agregada de infraestructura
Para qué sirve: agrupa en una única señal el riesgo asociado al protocolo, el TLD y la infraestructura de despliegue.
Captura patrones modernos del phishing español (TLDs baratos, dominios limpios, hostings temporales) y evita el doble conteo que existía en v1.

8.fake_tld_in_subdomain_or_path

Tipo: Señal sintáctica
Para qué sirve: Detecta imitaciones visuales de TLD en subdominios o rutas.
Ejemplos:
bbva.es-login.com
https://secure-site.net/correos.es/paquete
Qué problema resuelve: Señal binaria que identifica engaños de TLDs legítimos.

📏 E) Complejidad de ruta
9.param_count_boost

Tipo: Señal estructural
Para qué sirve: mide el número de parámetros en la URL.
Qué problema resuelve: El phishing moderno usa más parámetros, tratando de imitar procesos reales. 

# 4. Arquitectura interna del feature set

 ## 4.1 Señales internas (solo para cálculo)
Estas señales sirven como materia prima:

- domain_length
- domain_entropy
- host_entropy
- is_http
- free_hosting
- tld_risk_weight
- trusted_path_token
- trusted_path_penalty
- total_tokens
- path_depth
Ninguna aparece en el output final del modelo.

## 4.2 Señales finales (exportadas al modelo)
Cada una se deriva de ciertas internas:

| Feature final                       | Construida a partir de                         | Tipo de transformación          |
|-------------------------------------|------------------------------------------------|----------------------------------|
| `domain_complexity`                | `domain_length`, `domain_entropy`              | Agregación (complejidad)        |
| `host_entropy`                     | `host_entropy`                                 | Medición directa                 |
| `domain_whitelist_score`           | dominio ∈ whitelist                            | Validación                        |
| `suspicious_path_token`            | tokens sospechosos                             | Búsqueda directa                 |
| `token_density`                    | `total_tokens`, `path_depth`, pesos sectoriales| Normalización + ponderación       |
| `trusted_token_context`            | `trusted_path_token − trusted_path_penalty`    | Contexto                          |
| `infra_risk`                       | `is_http`, `tld_risk_weight`, `free_hosting`   | Agregación de infraestructura    |
| `fake_tld_in_subdomain_or_path`    | patrones de TLD falsos                         | Función indicadora                |
| `param_count_boost`                | Conteo de parámetros (`parse_qs`)              | Medición directa                  |

## 4.3. Conclusiones del diseño interno
El diseño interno del feature set v2 garantiza:

Ausencia de doble conteo:
cada señal interna alimenta únicamente una feature final.

Modularidad:
señales básicas (longitud, entropía, tokens, TLD, infraestructura) se combinan en features agregadas más estables.

Explicabilidad:
las 9 features finales responden a preguntas claras del análisis de phishing moderno en España.

Robustez:
la infraestructura se centraliza en infra_risk,
la semántica en token_density y suspicious_path_token,
la legitimidad en domain_whitelist_score,
y el contexto en trusted_token_context.

# 5. Motivación basada en datos (drift cuantitativo)
El EDA comparativo entre el prototipo v1 (200 URLs) y el dataset de inclusión v2 (300 URLs) reveló un cambio estructural y semántico claro en las campañas dirigidas a España.

Estos cambios justifican el rediseño del feature set.

## Cambios confirmados en el phishing real

| Señal                  | Variación | Implicación para el modelo                                                                 |
|------------------------|-----------|---------------------------------------------------------------------------------------------|
| **domain_length**      | −44 %     | Los dominios phishing modernos son **más cortos**, lo que invalida reglas antiguas basadas en longitud. |
| **domain_entropy**     | −25 %     | Menos aleatoriedad → dominios más “limpios”, más parecidos a los legítimos.                |
| **num_params**         | +189 %    | Aumento fuerte de callbacks, tokens y flujos dinámicos → clave para `param_count_boost`.    |
| **suspicious_path_token** | +33.7 pp | Aumento importante de tokens de acción en castellano → refuerza `suspicious_path_token` y `token_density`. |

# 6. Ejemplos prácticos del comportamiento del feature set

Ejemplo 1 — URL legítima (banca)
https://www.bbva.es/personas/area-cliente/login
- domain_whitelist_score = 1 (dominio oficial)
- trusted_token_context = +1
- token_density = baja
- infra_risk = bajo
- param_count_boost = 0
**Resultado**: URL legítima; no presenta señales de ataque.

Ejemplo 2 — Phishing “limpio” con TLD moderno
https://bbva-seguridad.live/login
- domain_whitelist_score = 0
- trusted_token_context = -1 (token legítimo en dominio falso)
- infra_risk = alto (.live)
- token_density = media

 **Resultado**: Phishing moderno utilizando TLD limpio y tokens bancarios.

Ejemplo 3 — Phishing avanzado (logística)
https://correos-validar.app/paquete/confirmar/envio?token=99d3
- suspicious_path_token = 1
- token_density = alta (ruta profunda + varios tokens)
- infra_risk = alto (.app)
- param_count_boost = 1–3
**Resultado**: Campaña realista de logística con tokens en castellano y ruta profunda.

7. Limitaciones conocidas de v2
A pesar de mejorar la precisión y reducir falsos positivos, el diseño v2 presenta varias limitaciones importantes:

 - Cobertura sectorial desigual
Los sectores SaaS, energía, retail y cripto están infrarrepresentados en el dataset actual.
Esto reduce la sensibilidad del modelo en targets menos frecuentes.

- Dependencia del diccionario sectorial
token_density utiliza tokens_por_sector.csv.
Si el diccionario no se actualiza con nuevas campañas, la feature puede quedar desfasada.

- Infraestructura parcialmente modelada
infra_risk cubre TLD y hosting, pero no detecta:
hosts comprometidos
paneles de phishing reconocibles
redirecciones o comportamiento dinámico

4️⃣ Dependencia de la whitelist
trusted_token_context requiere una whitelist española completa.
Si falta una entidad (nuevo banco, nuevo SaaS), pueden aparecer falsos positivos.

5️⃣ Sin señales profundas (embeddings)
v2 trabaja solo con la URL estática.
La semántica profunda (embeddings de texto, pgvector) llegará en v3 para cubrir casos ambiguos.

8. Conclusión final
El feature set v2 representa una evolución clara respecto al prototipo: pasa de señales técnicas poco fiables a un conjunto compacto de 9 features agregadas, explicables y alineadas con el phishing moderno en España.
El rediseño se sustenta en datos reales y en la necesidad de:
- priorizar tokens en castellano,

- modelar infraestructura actual (TLDs modernos, hostings temporales),

- incorporar contexto real de legitimidad,

- eliminar señales débiles y redundantes,

