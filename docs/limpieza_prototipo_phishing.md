# Limpieza prototipo phishing

## Resumen
- Total de URLs iniciales: **270** (limpiezas realizadas anteriormente entre los feeds de PhishTank y TweetFeed).  
- Tras revisión manual: **100 URLs válidas** dirigidas a usuarios en España.  
- Descartadas: **170** (LatAm/PT/global, irrelevantes o ruido).  
- Dataset final: CSV con columnas completas (`url`, `motivos`, `campaign`, etc.).  

## Proceso de limpieza

### 1. Carga inicial
- Fuente: combinación de varios feeds (ej. `PhishTank`, `TweetFeed`, `OpenPhish`, otros).  
- Total inicial: **270 URLs**.  
- Mezcla de campañas globales, LatAm y españolas.  

### 2. Criterios de selección
- ✅ **Mantener**:  
  - Campañas en castellano dirigidas a España.  
  - Marcas españolas claras (Correos, DGT, ING, BBVA, Orange, Santander, IONOS…).  
  - Indicadores específicos de España (`.es`, `+34`, símbolo `€`).  
- ❌ **Descartar**:  
  - Bancos/servicios LatAm (Banrural, Cuscatlán, Daviplata, Yape, Banco de Venezuela).  
  - Campañas en portugués (Bradesco, Itaú, Nubank, “fatura”, “pagamento”).  
  - Globales sin foco español.
  - Exceso de campañas low-cost, acortadores y repetición de entidades en lo posible.  

### 3. Revisión manual
- Se analizaron **270 URLs una por una**.  
- Se rellenaron las columnas `motivos` y `campaign`.  
- Descartadas: **170**.  
- Confirmadas: **100 válidas**.  

### 4. Resultados
- CSV final: **100 URLs phishing válidas y completas**.  
- Primer dataset **cerrado y utilizable para el prototipo**.  

## Ejemplos
- **Válidas (España):**  
  - `http://caixacapitalrisc.send2sign.es/login` → campaña CaixaBank.  
  - `https://soporte-netflx.com/` → phishing Netflix en castellano.  

- **Descartadas (LatAm/PT/otros):**  
  - `https://correosdecr.web.app` → Correos Costa Rica, no España.  
  - `https://qrco.de/Dgtes5` → Acortador, sin contexto de campaña.  
  - `http://app-ing.direct-ayuda.com` → Duplicado (http/https).  
  

## Observaciones
- El objetivo de fijar **100 URLs válidas** asegura un dataset inicial robusto para pruebas del modelo  
- Se añadieron URLs de un repositorio de GitHub para mejorar la calidad y variedad del dataset.