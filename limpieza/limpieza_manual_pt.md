# Limpieza manual de URLs de PhishTank

## Resumen
- Total de URLs iniciales: [poner nº inicial del CSV crudo]  
- Tras eliminación de duplicados: [poner nº tras limpieza]  
- Candidatas seleccionadas para revisión manual: **2.694**  
- Válidas (España): [rellenar nº final]  
- Descartadas (LatAm/PT/otros): eliminadas por irrelevancia  

## Proceso de limpieza

### 1. Carga y exploración inicial
- Fuente: `phishtank_01.csv` (feed de PhishTank).  
- Se analizaron duplicados, valores nulos y estructura de columnas.  

### 2. Limpieza automática
- Eliminación de duplicados por `url`.  
- Normalización de dominios y rutas:  
  - `domain_norm`, `path_norm`, `route_norm`.  
- Creación de un campo `url_norm` para trabajar en minúsculas y sin acentos.  
- Detección de **marcas españolas** en la URL mediante expresiones regulares.  
  - Se preparó un listado de marcas relevantes en España:  
    - **Banca**: Santander, BBVA, CaixaBank, ING, Sabadell, Bankinter, Abanca, EVO, Unicaja, Kutxabank, Openbank, etc.  
    - **Telecomunicaciones**: Movistar, Vodafone, Orange, Yoigo, MásMóvil, Digi, Euskaltel, Pepephone.  
    - **Administración pública**: DGT, SEPE, Catastro, Agencia Tributaria, Seguridad Social, INEM.  
    - **E-commerce y supermercados**: El Corte Inglés, Carrefour, MediaMarkt, PcComponentes, Mercadona, Lidl, Aldi, DIA, Alcampo, Eroski, Zara, Mango, Desigual, Tous, etc.  
    - **Energía y seguros**: Iberdrola, Endesa, Naturgy, Repsol, Cepsa, Mapfre, Mutua Madrileña, Línea Directa.  
    - **Otros sectores**: Seat, Renfe, Iberia, FNAC, Casa del Libro, etc.  
- Se generó la columna `marca_es` para identificar URLs candidatas.

### 3. Selección de candidatas
- Se exportaron las URLs que podían tener relación con marcas españolas a:  
  - `phishtank_candidatas_segunda.csv`.  
- Total: **2.694 URLs candidatas**.

### 4. Revisión manual final
- Cada URL fue analizada manualmente con los siguientes criterios:  
  - ✅ Válidas: campañas en castellano dirigidas a España (ej. DGT, Correos, ING, Orange, IONOS, BBVA).  
  - ❌ Descartadas: campañas de LatAm (Banrural, Cuscatlán, Pichincha, Daviplata, Banco de Venezuela…), campañas en portugués (Bradesco, Itaú, Nubank, “faturas”, “pagamento”…), y campañas globales sin relevancia para España.  
- Se completó la columna `ruido_estimado` (0–100) como medida de confianza.  
- Se eliminó todo lo irrelevante para mantener un dataset final **limpio y específico de España**.

## Ejemplos

### Válidas (España)
- `https://qrco.de/MULTAes` → Smishing DGT. Ruido 5%.  
- `https://correos-paqueteria.com/asset.php` → Correos España. Ruido 5%.  
- `https://soporte-netflx.com/` → Netflix en español. Ruido 10%.  
- `https://www.ing-es-movil.com` → ING España. Ruido 5%.  
- `https://ionosesfacturas.rf.gd/` → IONOS facturas falsas. Ruido 10%.  

### Descartadas (LatAm/PT/otros)
- `https://pagoscuscatlan.web.app/` → Banco Cuscatlán (El Salvador). Ruido 95%.  
- `https://bradesco.ibf3-clienteprime.com/` → Banco Bradesco (Brasil). Ruido 95%.  
- `https://yape-seguridad.webcindario.com/` → Yape (Perú). Ruido 95%.  
- `https://banruralbancavirtualgt.biz.site/` → Banrural (Guatemala). Ruido 95%.  

## Observaciones
- El proceso combinó **limpieza automática** (regex + normalización + eliminación de duplicados) con **curación manual exhaustiva**.  
- A diferencia de TweetFeed (donde se usaron heurísticas de puntuación), en PhishTank fue viable revisar manualmente todas las candidatas.  
- Se eliminó todo lo irrelevante para España: el dataset final solo conserva campañas que aportan valor para un prototipo de detección en contexto español.  
