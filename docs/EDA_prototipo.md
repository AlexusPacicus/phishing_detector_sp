# 📊 Análisis Exploratorio de Datos (EDA) – Dataset prototipo

## 1. Introducción
Este documento recoge los hallazgos del análisis exploratorio sobre el **dataset prototipo de 200 URLs balanceadas** (100 legítimas, 100 phishing).  

Objetivos del EDA:  
- Explorar diferencias estructurales entre URLs phishing y legítimas.  
- Identificar patrones relevantes por dominios, TLDs y tokens.  
- Señalar variables candidatas para la fase de **feature engineering**.  

---

## 2. Distribución general
- Balance perfecto: **100 legítimas vs 100 phishing**.  
- Categorías representadas: banca, SaaS, gaming, logística, administración pública, telecomunicaciones, streaming, cripto, retail, seguros y redes sociales.  

👉 Esto garantiza un dataset inicial sin sesgos de clase.  

---

## 3. Análisis estructural de URLs
- **Longitud media de URL**: similares → 44.3 (legítimas) vs 43.5 (phishing).  
- **Longitud media de dominio**: mayor en phishing → 15.4 vs 11.7.  
- **Profundidad media de ruta**: legítimas más profundas → 4.2 vs 3.3.  
- **Nº de parámetros**: phishing ligeramente superior → 0.12 vs 0.04.  
- **Caracteres especiales**: phishing introduce más `%`, `=`, `@`.  

---

## 4. Dominios y TLDs
- **Legítimas**: dominios oficiales (`bbva.es`, `bancosantander.es`, `ing.es`, `ionos.es`, `openbank.es`).  
- **Phishing**: servicios gratuitos (`webcindario.com`, `blogspot.com`, `web.app`, `ead.me`), typosquatting (`ing-es-movil.com`, `direct-ayuda.com`), y dominios sospechosos (`authline-checkappr0v.com.es`).  
- **TLDs**: `.es` domina en legítimas, mientras que phishing diversifica con `.com`, `.app`, `.me`, `.net`, `.xyz`, `.top`.  

---

## 5. Protocolos
- **Legítimas**: 100% usan `https`.  
- **Phishing**: 85% `https`, 15% todavía en `http`.  

👉 Aunque ya no es un factor decisivo (el phishing moderno también usa TLS), la presencia de `http` sigue siendo un **indicador claro de phishing**.  

---

## 6. Tokens en dominios y rutas
- **Dominios legítimos**: centrados en marcas (`bbva`, `santander`, `ing`, `caixabank`, `ionos`, `openbank`).  
- **Dominios phishing**: hostings gratuitos (`webcindario`, `sites`, `ead`), palabras sospechosas (`cliente`, `app`, `authline`), y marcas usadas de forma fraudulenta (`netflix`, `google`, `ing`).  
- **Rutas legítimas**: términos de servicio (`login`, `banca`, `particulares`, `seguridad`, `empresas`).  
- **Rutas phishing**: genéricos y técnicos (`php`, `html`, `index`, `view`, `principal`), codificación (`p%c3%a1gina`), y cadenas aleatorias (`dwd9i@prmk4jyy2v`).  

---

## 7. Entropía de dominio
- **Legítimas**: entropía media ≈ 3.04.  
- **Phishing**: entropía media ≈ 3.28.  

👉 Los dominios phishing muestran más **aleatoriedad**, indicador típico de generación automática o nombres falsos.  

---

## 8. Features candidatas
A partir del EDA, se recomiendan las siguientes variables:  

### 🔹 Estructurales
- `url_length`  
- `domain_length`  
- `path_depth`  
- `num_params`  
- `domain_entropy`  

### 🔹 Caracteres y símbolos
- `contains_@`, `contains_-`, `contains__`, `contains_%`, `contains_=`  

### 🔹 Protocolos y TLDs
- `protocol` (http/https)  
- `tld` → indicador de TLD sospechoso/infrecuente  

### 🔹 Tokens
- **Dominio**: marcas oficiales, hostings gratuitos, typosquatting.  
- **Ruta**: palabras sospechosas (`php`, `html`, `index`, `view`, `cliente`, `inicio`), palabras de confianza (`seguridad`, `banca`, `empresas`, `ayuda`), cadenas codificadas o aleatorias.  

---

## 9. Conclusión
El EDA confirma que existen **diferencias consistentes entre phishing y legítimas**, especialmente en:  
- Longitud/entropía de dominio.  
- Uso de parámetros y símbolos.  
- Tipo de TLD.  
- Tokens en dominios y rutas.  

Estos hallazgos serán la base del próximo paso: **feature engineering**, donde se convertirán en variables numéricas y categóricas para entrenar el primer prototipo de detección de phishing.  
