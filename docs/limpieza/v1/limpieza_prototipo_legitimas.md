# 📝 Proceso de elección de URLs legítimas

Este documento describe los criterios, pasos y decisiones que se siguieron para seleccionar las **100 URLs legítimas únicas** que forman el dataset final del prototipo.

---

## 📌 Criterios generales

- **Enfoque pedagógico** → con un dataset reducido (100 URLs) se buscó maximizar la diversidad sectorial y de patrones.  
- **Enfoque realista** → se incluyeron sobre todo sectores y entidades que aparecen en campañas reales de phishing en España.  
- **URLs estables** → se descartaron páginas con parámetros dinámicos (`state`, `nonce`, `code_challenge`) para evitar ruido.  
- **Variedad por entidad** → se intentó cubrir home, login, app y seguridad, en lugar de repetir siempre el login.  
- **Control de sesgo** → ING tiene mucho phishing en el dataset, por lo que se incluyeron varias legítimas para hacer contrapeso y evitar que el modelo aprenda un sesgo erróneo.  

---

## 📌 Sectores cubiertos y decisiones

### 1. Banca (44 URLs, 14 entidades)  
- **Grandes bancos:** ING (6), BBVA (5), Santander (4), CaixaBank (3), Sabadell (3).  
- **Bancos medianos:** Abanca (3), Unicaja (4), Ibercaja (3), Kutxabank (3), Bankinter (3).  
- **Otros bancos:** Caja Rural / Ruralvía (2), Banco Mediolanum (1), Openbank (3).  
- **Decisiones clave:**  
  - **ING** se cubrió con 6 legítimas únicas para compensar la gran cantidad de phishing detectado, evitando que el modelo aprenda “todo ING es phishing”.  
  - No se buscó igualar 1:1 el número de legítimas al de phishing en ING, ya que eso habría reducido la representación de otros bancos.  
  - Se reforzaron entidades menos presentes en phishing, como **Openbank, Ibercaja, Kutxabank y Bankinter**, para aportar diversidad.  
  - Banco Galicia se eliminó.  
  - Banco Mediolanum se representó con su portal oficial de banca personal, evitando duplicados de `bmedonline.es`.  

### 2. Logística (7 URLs, 6 entidades)  
- Correos (2), Correos Express (2), DHL (1), SEUR (1), MRW (1), GLS (1).  
- **Decisiones clave:** se añadieron **MRW y GLS** para diversificar y se eliminó un duplicado de DHL.

### 3. Administración pública (5 URLs)  
- DGT (3), AEAT (1), Seguridad Social (1), UnisciMadrid (1).  
- **Decisiones clave:** DGT se mantuvo con 3 legítimas por su relevancia, pese a estar sobrerrepresentada en phishing.

### 4. Telecomunicaciones (6 URLs)  
- Orange (2), Vodafone (1), Movistar (1), Yoigo (1), Digi (1).  
- **Decisiones clave:** Orange se limitó a 2 legítimas, evitando inflar aún más su peso.

### 5. SaaS / Cloud (7 URLs)  
- IONOS (3), Microsoft/Outlook (1), Zoom (1), Dropbox (1), Google Drive (1), WeTransfer (1), Yahoo Mail (1).  
- **Decisiones clave:** IONOS se reforzó porque fue de los más atacados en phishing.

### 6. Streaming / Gaming (7 URLs)  
- Netflix (2), HBO Max (1), Prime Video (1), Roblox (2), Habbo (1), FlixOlé (1).  
- **Decisiones clave:** Netflix limitado a 2 para evitar sobrepeso. FlixOlé incluido como servicio nacional.

### 7. Cripto / Energía (5 URLs)  
- Coinbase (2), Binance (1), WalletConnect (1), Bit2Me (1), BP (1).  
- **Decisiones clave:** Bit2Me como exchange español. BP como energía/pagos.

### 8. Retail / Seguros / Transporte / RRSS (19 URLs)  
- **Retail (7):** Carrefour, Mercadona, El Corte Inglés, PcComponentes, MediaMarkt, Zara, Decathlon.  
- **Seguros (2):** Mapfre, Mutua Madrileña.  
- **Energía (1):** Iberdrola.  
- **Transporte (2):** Renfe, Iberia Plus.  
- **RRSS / Mensajería (2):** Instagram, WhatsApp.  
- **Decisiones clave:** se añadió **Decathlon login** para reforzar retail.  

---

## 📊 Resumen por sector

| Sector                | Nº URLs | % del total |
|------------------------|---------|-------------|
| Banca                 | 44      | 44 %        |
| Logística             | 7       | 7 %         |
| Administración pública | 5       | 5 %         |
| Telecomunicaciones    | 6       | 6 %         |
| SaaS / Cloud          | 7       | 7 %         |
| Streaming / Gaming    | 7       | 7 %         |
| Cripto / Energía      | 5       | 5 %         |
| Retail                | 7       | 7 %         |
| Seguros               | 2       | 2 %         |
| Energía               | 1       | 1 %         |
| Transporte            | 2       | 2 %         |
| Redes Sociales        | 2       | 2 %         |

---

## 📌 Conclusiones

- El dataset final incluye **100 URLs legítimas únicas, sin duplicadas**, con amplia cobertura de sectores y **14 entidades bancarias**.  
- **ING** se cubrió con 6 legítimas para **contrarrestar su gran presencia en phishing**, evitando que el modelo lo clasifique siempre como phishing.  
- No se igualó 1:1 con su número de phishing, para dar espacio a entidades menos representadas y ganar diversidad (Openbank, Ibercaja, Kutxabank, Bankinter…).  
- Se añadieron **MRW y GLS** en logística y **Decathlon** en retail para ampliar la variedad.  
- El balance se diseñó con fines **pedagógicos y explicativos**, no para reflejar con exactitud la distribución real de ataques (donde banca supera el 50 %).  
- En futuros datasets a escala se ajustarán proporciones según threat intel real: banca ~50–60 % y el resto de sectores distribuidos por frecuencia observada.
