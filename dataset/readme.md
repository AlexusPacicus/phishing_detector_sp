# 📑 Unificación del dataset final (phishing vs legítimas)

## 1. Fuentes de datos
- **Legítimas** → `legitimas_final.csv` (100 URLs válidas, curadas y categorizadas).  
- **Phishing** → `phishing_final.csv` (100 URLs válidas, curadas y categorizadas).  

Ambos ficheros provenían de procesos de limpieza manual documentados previamente:  
- Limpieza de PhishTank  
- Limpieza de TweetFeed  
- Limpieza prototipo phishing

## 2. Proceso de unificación
1. Se identificaron las columnas en común:  
   - `url`, `label`, `categoria`, `matched_target`.  
2. Se detectaron diferencias:  
   - `notas` → presente en legítimas.  
   - `motivos` → presente en phishing.  
   - `campaign` → presente solo en phishing.  
3. Se decidió unificar `motivos` y `notas` en una única columna llamada **`notas`**.  
4. El esquema final definido fue:  
   - `url`  
   - `label` (0 = legítima, 1 = phishing)  
   - `categoria`  
   - `matched_target`  
   - `notas`  
   - `campaign`  
5. Se normalizó la categoría `rrss` → `redes sociales` para mantener consistencia.

## 3. Resultados
- **Total final**: 200 URLs.  
  - 100 legítimas (label = 0).  
  - 100 phishing (label = 1).  
- Todas las columnas alineadas y sin pérdida de información.  
- En legítimas, las columnas `campaign` quedan vacías.  
- En phishing, las columnas `notas` incluyen la justificación de inclusión.  

## 4. Exploración del dataset

### Balance de clases
- **Legítimas (0)**: 100  
- **Phishing (1)**: 100  

Dataset perfectamente balanceado.

### Distribución por categorías  
(*se unificaron las etiquetas `rrss` y `redes sociales` bajo `redes sociales` para evitar duplicados*)  

| Categoría            | Legítimas | Phishing |
|----------------------|-----------|----------|
| Banca                | 37        | 37       |
| Cripto               | 5         | 5        |
| Energía              | 1         | 1        |
| Gaming               | 3         | 3        |
| Genérico             | 18        | 18       |
| Logística            | 7         | 7        |
| Público              | 7         | 7        |
| Redes sociales       | 1         | 1        |
| SaaS                 | 9         | 9        |
| Streaming            | 5         | 5        |
| Telecomunicaciones   | 7         | 7        |


### Ejemplos
- **Legítima**:  
  - `https://www.caixabank.es/particular/banca-digital.html`  
  - `https://zoom.us/es/join`  
- **Phishing**:  
  - `http://caixacapitalrisc.send2sign.es/login` → campaña CaixaBank.  
  - `https://soporte-netflx.com/` → phishing Netflix en castellano.  

## 5. Observaciones
- Este dataset ya está **listo para entrenar un prototipo de detección de phishing**.  
- Mantiene balance (50/50) para evitar sesgos iniciales.  
- La estructura permite futuras expansiones:  
  - Añadir más URLs legítimas/phishing.  
  - Incorporar nuevas categorías o campañas.  
  - Usar `notas` como campo de explicación para auditorías manuales.  

## 6. Conclusión
Este dataset final de 200 URLs, bien balanceado y documentado, constituye la **base oficial para el prototipo de detección de phishing en España**.  
