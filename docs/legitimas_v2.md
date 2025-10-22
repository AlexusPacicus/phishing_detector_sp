




Sector	Nº URLs	% aprox
🏦 Banca	59	39.3%
📦 Logística	36	24.0%
☁️ SaaS / Cloud / Plataformas	10	6.7%
📱 Telecomunicaciones	10	6.7%
💳 Cripto / Fintech	10	6.7%
🔌 Energía / Seguros	10	6.7%
🏛️ Administración pública	5	3.3%
🛒 Retail / e-commerce / Streaming	10	6.7%
⚙️ Genérico / Otros (hard negatives, integraciones)	10	6.7%
Total	150	100%

| Entidad                            | Nº URLs | % dentro del sector | Notas                                                                                              |
| :--------------------------------- | ------: | ------------------: | :------------------------------------------------------------------------------------------------- |
| Santander                          |       8 |               13.6% | Muy representado en phishing; incluir rutas `/ayuda`, `/seguridad`, `/tarjetas`, no solo `/login`. |
| BBVA                               |       7 |               11.9% | Variedad: `/login`, `/banca-digital`, `/seguridad`, `/particulares`.                               |
| CaixaBank                          |       6 |               10.2% | Importante incluir `/areaclientes`, `/empresas`, `/seguridad`.                                     |
| ING                                |       5 |                8.5% | Rutas `/app`, `/clientes`, `/faq`.                                                                 |
| Sabadell                           |       5 |                8.5% | `/acceso`, `/personas`, `/banca-online`.                                                           |
| Bankinter                          |       4 |                6.8% | `/banca-internet`, `/empresas`, `/contacto`.                                                       |
| Openbank                           |       4 |                6.8% | `/clientes`, `/productos`, `/faq`.                                                                 |
| Abanca                             |       3 |                5.1% | `/clientes`, `/banca-movil`.                                                                       |
| Unicaja                            |       3 |                5.1% | `/personas`, `/canales`, `/banca-digital`.                                                         |
| Kutxabank                          |       3 |                5.1% | `/personas`, `/banca-online`, `/seguridad`.                                                        |
| EVO Banco                          |       2 |                3.4% | `/login`, `/ayuda`.                                                                                |
| Cajamar                            |       2 |                3.4% | `/banca`, `/clientes`.                                                                             |
| Cetelem / Wizink (crédito consumo) |       2 |                3.4% | Complemento financiero (útiles para señales fintech).                                              |
| **Total**                          |  **59** |            **100%** | —                                                                                                  |
🎯 Reglas para este sector
Máx 8 URLs por entidad, mín 3 tipos de ruta (login, operativa, ayuda/seguridad).
Evita rutas duplicadas entre entidades (/login, /acceso repetidos).
Añade 3–5 hard negatives (subdominios raros o integraciones, p. ej. login.santander.openbank.es o secure.bbva.azureedge.net).
Incluye al menos 1 URL con dominio internacional por cada gran banco (ej. santander.com, bbva.com) para enriquecer variabilidad TLD.

🧩 Criterio documentable (añadirás a docs/legitimas_v2_calidad.md)
Regla: “En caso de entidades bancarias inactivas o absorbidas, sus cupos se reasignan equitativamente entre bancos activos del mismo grupo.”
Ejemplos de aplicación:
Si EVO Banco o Unicaja no presentan rutas operativas diferenciadas, sus 2–3 URLs se redistribuyen hacia Santander, BBVA o CaixaBank.
Si Cajamar o Abanca comparten infraestructura con otra entidad, se considera un solo grupo para el conteo.

📦 Sector Logística — Distribución final (36 URLs)
Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Correos	22	61.1 %	Entidad central y más atacada. Incluir variedad de rutas: /seguimiento, /envios, /recogida, /avisos, /cita-previa, /ayuda, /login. Añadir 2 hard negatives con subdominios o query params (p. ej. clientes.correos.es, citaprevia.correos.es).
SEUR	2	5.6 %	/seguimiento, /clientes.
MRW	2	5.6 %	/seguimiento, /contacto.
NACEX	3	8.3 %	/seguimiento, /faq, /delegaciones.
GLS España	2	5.6 %	/tracking, /envios.
DHL España	2	5.6 %	/tracking, /ayuda.
UPS España	2	5.6 %	/track, /centros.
FedEx / Amazon Logistics / integraciones	1	2.8 %	Casos híbridos (lockers, devoluciones, integraciones API).
Total	36	100 %	—
Criterios adicionales:
Correos cubre más del 60 % del sector, reflejando su peso real en el phishing v2.
Cada entidad debe tener mínimo 3 tipos de ruta distintos.
Rutas repetitivas /tracking deben variarse (/estado-envio, /consulta-envio, etc.).
Si alguna entidad carece de suficientes URLs activas, sus cupos se redistribuyen hacia Correos o SEUR, manteniendo el total en 36.


☁️ Sector SaaS / Cloud / Plataformas — Distribución final (10 URLs)
Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Microsoft (365 / Azure)	3	30 %	Incluir rutas /login, /account, /security, /status, /support. Cubrir entorno Office 365 y Azure Portal.
Google Workspace	2	20 %	/login, /admin, /security, /status. Añadir una ruta docs (p. ej. /support).
IONOS / OVH / SiteGround	2	20 %	Hosting y correo empresarial. Rutas /login, /customer, /faq, /status.
GitHub / GitLab	2	20 %	/login, /account, /settings, /status, /docs. Muy útiles para features semánticas (tech tokens).
Stripe / Redsys (Pasarelas de pago SaaS)	1	10 %	/dashboard, /billing, /docs. Complementa con 1–2 hard negatives si hay integraciones externas.
Total	10	100 %	—
Criterios adicionales:
Variedad de rutas: cada entidad debe incluir al menos /login, una página técnica (/status, /docs) y una de ayuda (/support, /faq).
Añadir 2 hard negatives (ej. subdominios de autenticación externa o URLs legítimas con param token de API).
Si una entidad no dispone de rutas públicas suficientes, reasignar sus cupos a Microsoft o Google, manteniendo el total de 10.


📱 Sector Telecomunicaciones — Distribución final (10 URLs)
Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Movistar (Telefónica)	4	40 %	Principal operador nacional. Incluir /mi-movistar, /facturas, /ayuda, /cobertura, /clientes. Añadir 1 hard negative (subdominio tipo id.movistar.es o integración).
Vodafone España	2	20 %	/mi-vodafone, /login, /soporte, /facturas.
Orange España	2	20 %	/mi-orange, /clientes, /ayuda, /facturas.
MásMóvil / Digi / Pepephone (grupo alternativo)	2	20 %	/area-cliente, /soporte, /portabilidad, /faq. Priorizar Digi y Pepephone por diversidad de infraestructura.
Total	10	100 %	—
Criterios adicionales:
Cada operador debe tener al menos tres tipos de ruta distintos (/login o /area-cliente, /facturas, /ayuda).
Añadir 1–2 hard negatives: páginas legítimas con tokens o integraciones externas (id.movistar.es, auth.vodafone.es).
Evitar redundancias de /mi-<marca> — busca rutas funcionales distintas (/facturas, /cobertura, /incidencias).
Si una marca carece de páginas activas o abiertas (p. ej. portales totalmente cerrados), redistribuir a Movistar o Vodafone.

💳 Sector Cripto / Fintech — Distribución final (10 URLs)
Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Binance	4	40 %	/login, /security, /wallet, /support, /es/docs.
Coinbase	3	30 %	/login, /learn, /security, /status.
Kraken	2	20 %	/login, /help, /security.
Bit2Me (España)	1	10 %	/login, /academy, /contacto.
Total	10	100 %	—
Criterios:
Incluir rutas públicas y de soporte, no solo login.
Añadir 1–2 hard negatives (páginas legítimas de APIs o docs con ?token= o redirect).
Si alguna no tiene rutas accesibles, reasignar a Binance o Coinbase.
🔌 Sector Energía / Seguros — Distribución final (10 URLs)
Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Iberdrola	3	30 %	/clientes, /facturas, /incidencias, /ayuda.
Endesa	3	30 %	/area-cliente, /facturas, /tarifas, /sostenibilidad.
Mapfre	2	20 %	/clientes, /siniestros, /seguros.
Línea Directa / Mutua Madrileña	2	20 %	/area-cliente, /contacto, /particulares.
Total	10	100 %	—
Criterios:
Enfocar en rutas /facturas, /area-cliente, /siniestros, /ayuda.
Añadir 1 hard negative (por ejemplo, subdominios de portales antiguos).
Si una aseguradora no tiene portales abiertos, reasignar a Iberdrola o Endesa.
🏛️ Sector Administración pública — Distribución final (5 URLs)
Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Agencia Tributaria (AEAT)	2	40 %	/sede, /tramites, /notificaciones.
Seguridad Social (TuSS / INSS)	2	40 %	/sede-electronica, /cita-previa, /informes.
Dirección General de Tráfico (DGT)	1	20 %	/sede-electronica, /tramites, /cita-previa.
Total	5	100 %	—
Criterios:
Enfocar en rutas /sede, /cita-previa, /notificaciones, /tramites.
No usar mirrors autonómicos.
Si alguna URL deja de ser accesible, redistribuir a AEAT o Seguridad Social.
🛒 Sector Retail / e-commerce / Streaming — Distribución final (10 URLs)
Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Amazon España	3	30 %	/login, /pedido, /devoluciones, /ayuda.
El Corte Inglés	2	20 %	/clientes, /pedido, /ayuda.
Carrefour España	2	20 %	/login, /compra, /ayuda.
PcComponentes / MediaMarkt	2	20 %	/checkout, /factura, /soporte.
Netflix (España)	1	10 %	/es/login, /account, /help.
Total	10	100 %	—
Criterios:
Cubrir variedad de rutas (/pedido, /ayuda, /checkout, /facturas).
1–2 hard negatives: URLs legítimas con tracking o IDs largos.
Evitar repetir solo /login; buscar rutas funcionales.
⚙️ Sector Genérico / Otros — Distribución final (10 URLs)
Tipo / Entidad	Nº URLs	% del sector	Descripción / rutas recomendadas
Pasarelas de pago (Redsys, PayPal, Stripe)	3	30 %	/tpv, /pago, /return, /callback, /docs.
Servicios mixtos / APIs públicas (AWS, Cloudflare, Azure Status)	3	30 %	/status, /api, /help, /incident.
Portales de identidad (OAuth, Auth0, Okta)	2	20 %	/authorize, /login, /callback.
Redes sociales / integraciones (LinkedIn, Twitter)	2	20 %	/login, /help, /security.
Total	10	100 %	—
Criterios:
Este bloque sirve como “zona neutra” y hard negatives globales.
Priorizar URLs legítimas pero ambiguas (autenticación, callbacks, APIs).
Si alguna no se consigue, redistribuir dentro del mismo grupo funcional.