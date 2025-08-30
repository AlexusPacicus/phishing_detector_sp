# Limpieza de URLs de TweetFeed

## Resumen
- Total de URLs iniciales: ~39.279  
- Tras aplicar heurísticas de puntuación (`score_total >= 2`): 2.080 candidatas  
- Revisadas manualmente: un subconjunto representativo  
- Válidas confirmadas (España): 13  
- Descartadas: miles de URLs LatAm/PT/Global eliminadas por irrelevancia

## Proceso de limpieza

### 1. Carga inicial
- Fuente: feed de TweetFeed (~39k URLs).  
- Se detectó que el volumen hacía inviable una revisión manual completa.  

### 2. Filtrado automático por heurísticas
Se diseñó un sistema de puntuación para priorizar URLs potencialmente dirigidas a España.  
Las reglas incluyeron:

- **Señales positivas** (suman puntos):  
  - Palabras clave en castellano: `multa`, `pago`, `verificación`, `cliente`, `acceso`, `seguridad`.  
  - Indicadores de España: `.es`, `+34`, símbolo `€`.  
  - Marcas españolas: Correos, DGT, ING, BBVA, Santander, Orange, Movistar, Yoigo, IONOS, etc.

- **Señales negativas** (restan puntos):  
  - TLDs asociados a otros países: `.com.br`, `.co.ua`, `.gt`, `.cr`, `.pe`.  
  - Bancos/servicios LatAm o PT/BR: Banrural, Cuscatlán, Pichincha, Itaú, Bradesco, BHD, Yape.  
  - Keywords en portugués: `pagamento`, `fatura`, `acesso cliente`.

- Se aplicó un **umbral de corte**: `score_total >= 2`.

### 3. Selección de candidatas
- Resultado del filtrado: **2.080 URLs candidatas**.  
- Estas URLs se consideraron lo suficientemente relevantes para revisión manual parcial.  

### 4. Validación manual
- Se revisó un subconjunto representativo de las 2.080.  
- Se confirmaron **13 URLs** como phishing dirigido a usuarios en España.  
- Ejemplos confirmados:  
  - `https://pago-master.digital/Confirmación de Pago.html` → scam financiero en castellano.  
  - `https://orangeinfos.godaddysites.com/` → phishing Orange España.  
  - `https://orangexexchange.live/` → phishing Orange.  

- Se eliminaron datasets antiguos que contenían URLs no válidas (`tweetfeed_es.csv`).  
- Se construyó un nuevo CSV únicamente con las URLs revisadas y confirmadas.  

## Observaciones
- A diferencia de PhishTank (donde la revisión manual fue completa), en TweetFeed fue necesario un **pipeline híbrido**:  
  - **Automático**: heurísticas de puntuación para reducir volumen.  
  - **Manual**: revisión de un subconjunto reducido para asegurar la calidad.  
- Este enfoque permitió obtener un conjunto de URLs en castellano, con campañas claras para España, sin necesidad de revisar las ~39k URLs iniciales.  
- La documentación de criterios (`criterios_limpieza.md`) asegura reproducibilidad para futuras ejecuciones del filtrado.  
