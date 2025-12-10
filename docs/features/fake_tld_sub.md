🧩 Feature eliminada: fake_tld_in_subdomain_or_path
Estado: Eliminada en v2.x
Motivo: Falta total de discriminación y obsolescencia táctica
🧠 1. Descripción original

La feature fake_tld_in_subdomain_or_path estaba diseñada para detectar intentos clásicos de suplantación mediante falsificación del TLD en:

subdominios

rutas

parámetros

Ejemplos que esta técnica intentaba capturar:

bbva.es-login.com
caixa.com.es-verificacion.net
santander.net.es-seguridad.info


Este tipo de manipulación era común en campañas antiguas.

🧪 2. Análisis empírico en dataset v2.1 (492 URLs)
Resultados:
Legítimos:
mean = 0.217
std  = 0.413

Phishing:
mean = 0.250
std  = 0.434


Interpretación:

La activación de la feature es prácticamente idéntica en ambas clases.

No existe separación estadística entre legítimos y phishing.

No contribuye al modelo ni aporta señal relevante.

🟥 3. Diagnóstico: técnica obsoleta

El análisis de campañas modernas orientadas a España muestra:

Los atacantes ya no intentan falsificar TLDs.

Prefieren infraestructura neutral:

builderall

cprapid

easywp

codeanyapp

cloudways

O URLs con subdominios aleatorios, no TLD falsos.

Los falsos positivos aumentan y los verdaderos positivos caen casi a cero.

Por tanto, la feature no refleja el comportamiento real de las amenazas actuales.

🧨 4. Riesgos de mantener esta feature

Introducir ruido innecesario.

Reducir la interpretabilidad.

Posible sobreajuste a patrones irrelevantes.

Ningún beneficio detectable en recall o precisión.

Mantenerla empeoraría el modelo.

🟩 5. Decisión final

La feature se elimina por completo del extractor v2.x.

No se realiza reemplazo directo, ya que otros módulos del pipeline capturan mejor los patrones modernos:

domain_complexity_v23

host_entropy

trusted_token_context_v28

brand_match_flag_v2

infra_risk (versión estable)

📌 6. Notas para futuro desarrollo

Si se detectan campañas que reutilicen técnicas de falsificación de TLDs, podría evaluarse la reintroducción de una versión modernizada basada en:

coincidencias estructurales

distancia léxica

normalización de dominios

Por ahora, esta señal no es útil en el ecosistema actual.