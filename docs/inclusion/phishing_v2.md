
# 🧩 Análisis de Calidad – Dataset `phishing_v2_inclusion1_notas_normalized`

## 1️⃣ Resumen estructural
- **Total de URLs:** 209  
- **Duplicados:** 0 ✅  
- **Nulos:** 0 ✅  
- **Columnas principales:** `url`, `sector`, `entidad`, `ruido_estimado`, `notas`, `confianza_est`, `score_total_v2`  
- **Rango de ruido:** 10–50  
- **Media de ruido:** **10.8 ± 5.5**  
  > 75 % de las URLs tienen ruido ≤ 10 → dataset *extremadamente limpio*.

---

## 2️⃣ Distribución sectorial

| Sector | Nº URLs | % |
|---------|----------|---|
| Banca | 113 | 54.1 % |
| Logística | 67 | 32.1 % |
| Genérico | 28 | 13.4 % |
| Público | 1 | 0.5 % |

➡️ **Conclusión:**  
Dominio claro de banca y logística (86 % del total).  
Otros sectores (SaaS, público, retail…) están casi ausentes → esto afectará a la generalización del modelo si no se amplía luego.

---

## 3️⃣ Entidades más frecuentes

| Entidad | Nº URLs |
|----------|----------|
| Correos | 58 |
| Santander | 50 |
| Genérico | 43 |
| CaixaBank | 25 |
| BBVA | 14 |
| ING | 10 |
| Bankinter | 3 |
| Bankia | 2 |
| Seur | 2 |
| Amazon | 1 |
| DGT | 1 |

➡️ **Sesgo fuerte hacia Santander, Correos y CaixaBank.**  
Lógico en esta fase inicial, pero conviene añadir campañas de SaaS, cripto, energía o seguros.

---

## 4️⃣ Estadísticas del ruido

| Percentil | Ruido (%) |
|------------|------------|
| Mínimo | 10 |
| 25% | 10 |
| 50% | 10 |
| 75% | 10 |
| Máximo | 50 |

➡️ Desviación estándar baja (5.5), bloque homogéneo y de alta confianza.  
Casos con ruido ≈ 50 → útiles para validación.

---

## 5️⃣ Tokens más frecuentes en notas

| Palabra | Frecuencia |
|----------|-------------|
| ing | 148 |
| login | 138 |
| banca | 115 |
| correos | 112 |
| paquete | 87 |
| santander | 83 |
| generico | 69 |
| logistica | 64 |
| smishing | 45 |
| pago | 42 |
| verificación | 30 |
| caixabank | 38 |
| bbva | 28 |
| recibir | 21 |
| banco | 20 |

➡️ Notas bien estandarizadas (`|` y `;`), con pequeñas inconsistencias:  
- mezcla `Verificación` / `verificación`;  
- “Generico” con mayúscula;  
- concatenaciones sin espacio tras `|`.

---

## 6️⃣ Ejemplos representativos

### 🟢 Bajo ruido (10 %)
- `000o8dc.wcomhost.com/...santanderbanco.es...` → **Santander, login, score=14**  
- `0c4d4e6.wcomhost.com/banco-santander/...` → **Santander, verificación, score=16**  
- `122.114.173.242:30/bancosantander.es/...` → **Santander, login, score=12**  
- `alertanotificacionesdinamicos.com/...` → **Genérico, verificación, score=14**  

### 🟠 Ruido medio (≈ 50 %)
- `grupobankintere.com/...` → Bankinter, dominio no español.  
- `appverify.clotingbasicsotre.cloud/...3d/no-back-button` → Genérico, infraestructura no española.  
- `bancaonline-bancosantander-es.com/...` → Santander, mezcla de tokens y TLD global.  
- `info.163-123-143-56.cprapid.com/bbva.es` → BBVA, host global pero marcador `.es`.

---

## 7️⃣ Conclusión general

| Criterio | Resultado |
|-----------|------------|
| Integridad estructural | ✅ Sin nulos ni duplicados |
| Ruido promedio | ✅ Muy bajo (≈ 10 %) |
| Estandarización de notas | ✅ Alta |
| Equilibrio sectorial | ⚠️ Débil (banca y logística dominan) |
| Presencia de campañas reales | ✅ Alta |
| Casos dudosos útiles | ⚠️ Pocos pero necesarios (ruido ≈ 50) |

---

## 💡 Recomendaciones

| Acción | Descripción |
|---------|-------------|
| ✅ Mantener 180–190 URLs | Phishing español claro (ruido ≤ 20 %) |
| ⚠️ Marcar 10–20 URLs como “frontera” | Ruido 30–50 %, usar para validación o test |
| 🔧 Estandarizar campos | Renombrar columnas y normalizar “Genérico”/“Generico” |
| 🧭 Ampliar sectores | Incluir SaaS, cripto, energía, retail y administración pública |

---

**Conclusión:**  
El dataset es sólido, homogéneo y altamente representativo de campañas reales de phishing en España.  
Solo requiere diversificación por sectores antes del reentrenamiento y la creación de conjuntos estratificados (train/val/holdout).

