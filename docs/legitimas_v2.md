🛡️ Inclusión de URLs legítimas – Dataset v2
Fecha: 23/10/2025
Responsable: Alexis Zapico Fernández
Versión: legitimas_v2_final.csv (150 URLs)
1. 🎯 Objetivo
Construir un nuevo conjunto de 150 URLs legítimas verificadas que representen diversos sectores económicos, para:
Usarlo como contrapeso semántico en la validación del modelo (eval_set_inclusion1.csv).
Mejorar la robustez del sistema frente a falsos positivos.
Reflejar la diversidad real de servicios usados en España.
2. 📂 Fuentes y metodología
Las URLs fueron obtenidas mediante búsqueda manual controlada, aplicando los siguientes criterios generales:
Criterio	Valor
is_https	1
free_hosting	0
confidence	≥90
domain	Oficial y activo (verificado manualmente)
deduplicado	No repetida frente a legitimas_final.csv del prototipo
Cada URL se anotó con:
sector
entidad
tipo de ruta (route_type)
origen (source = manual)
nivel de confianza (confidence)
fecha de recolección (timestamp)
3. 📊 Distribución sectorial
Sector	Nº URLs	% aprox
🏦 Banca	59	39.3%
📦 Logística	36	24.0%
☁️ SaaS / Cloud / Plataformas	10	6.7%
📱 Telecomunicaciones	10	6.7%
💳 Cripto / Fintech	10	6.7%
🔌 Energía / Seguros	10	6.7%
🏛️ Administración pública	5	3.3%
🛒 Retail / e-commerce	10	6.7%
⚙️ Genérico / Otros	10	6.7%
TOTAL	150	100%
Cada bloque sectorial se documenta en su sección correspondiente, con entidades, rutas representadas y criterios adicionales.
4. 🧩 Criterios específicos por sector
Por ejemplo:
Banca: máx 8 URLs por entidad; mín 3 tipos de ruta (/login, /ayuda, /empresas...); añadir al menos un dominio internacional por gran banco.
Logística: Correos = 60% del sector; evitar duplicados tipo /seguimiento; añadir integraciones API como hard negatives.
SaaS: cubrir login, admin, status, support. Incluir pasarelas tipo Stripe y Redsys como casos ambiguos.
(y así con cada bloque... ya lo tienes detallado en el documento base)
5. ✅ Verificación manual
Todas las URLs fueron accedidas manualmente el 22 de octubre de 2025, comprobando que devuelven 200 OK o redirección válida (302 → 200).
Se priorizaron rutas activas, semánticas, con contexto claro.
Se evitó cualquier tipo de contenido genérico o redireccionado fuera de España.
6. 🧠 Observaciones semánticas
Las URLs seleccionadas refuerzan tokens positivos como:
clientes, empresas, banca, sede, tramites, ayuda, area-cliente, status, dashboard, factura, pedido, etc.
Se incluyeron varios hard negatives legítimos:
URLs con parámetros (orderID=..., ?token=...)
Subdominios o integraciones (auth0, login.microsoftonline.com, etc.)
Rutas de documentación o APIs (/docs, /api/status, etc.)
Esto refuerza las señales trusted_path_token y entrena al modelo a no penalizar por estructuras legítimas complejas.
7. 🔍 Validación contra prototipo
Se comprobó que ninguna URL esté duplicada con el dataset original legitimas_prototipo.csv.
8. 📁 Entregables
data/processed/legitimas/legitimas_v2_final.csv
Documentación completa por sector en docs/legitimas_v2.md
Este README: docs/README_inclusion_legitimas_v2.md
9. 🔮 Próximos pasos
Usar este conjunto en la validación eval_set_inclusion1.csv junto a phishing_v2_150.csv.
Analizar falsos positivos por sector.
Ajustar scoring semántico si se detectan patrones comunes de error.
Publicar post resumen en LinkedIn con ejemplos y visualizaciones.
