# 📊 EDA Comparativo — Prototipo vs Inclusión v2

**Fecha:** 2025-10-29  
**Responsable:** *Alexis Zapico Fernández*  

**Archivos analizados:**
- `features_prototipo_con_sector_entidad.csv` → 200 URLs (10 features + categoría + entidad)  
- `predicciones_inclusion_v2.csv` → 300 URLs (10 features + inferencias + sectores)

---

## 1️⃣ Contexto

Este análisis compara la evolución del **dataset del prototipo (v1)** frente al nuevo **dataset de Inclusión v2**, utilizado para validar el modelo actual y planificar el reentrenamiento.

### Objetivos:
- Detectar *drift semántico y estructural* entre ambas versiones.  
- Analizar la evolución por sectores y entidades.  
- Identificar cambios en las *features* y su impacto en el modelo.  
- Servir de base para el rediseño de `features_v2.py` y el ajuste del *scoring v3*.

---

## 2️⃣ Distribución general de clases

| Dataset | Nº URLs | % Phishing | % Legítimas |
|----------|----------|------------|-------------|
| Prototipo | 200 | 50 % | 50 % |
| Inclusión v2 | 300 | 50 % | 50 % |

✅ Ambos conjuntos están perfectamente balanceados, lo que permite una comparación estadística coherente.

---

## 3️⃣ Evolución por sectores

| Sector | Prototipo (%) | Inclusión v2 (%) | Cambio | Interpretación |
|--------|---------------:|-----------------:|--------|----------------|
| **Banca** | 40.0 | 44.3 | +4.3 pp | Sector dominante, se mantiene estable. |
| **Logística** | 6.5 | 30.3 | **+23.8 pp** | Crecimiento muy fuerte: campañas de Correos, SEUR, DHL… |
| **Cripto / Fintech** | 5.0 | 4.0 | −1.0 pp | Estabilidad relativa. |
| **SaaS / Cloud / Plataformas** | 9.0 | 3.3 | −5.7 pp | Reducción; menor peso de logins corporativos. |
| **Público / Administración** | 7.0 | 2.0 | −5.0 pp | Menor presencia; priorización de sectores más activos. |
| **Otros (retail, energía, genérico)** | 32.5 | 16.1 | −16.4 pp | Dataset más consolidado y menos disperso. |

**Conclusión:**  
El v2 presenta un **drift sectorial claro hacia la logística**, reflejando las campañas más frecuentes en España (Correos, SEUR, DHL).  
Esto mejora la representatividad y reduce la dispersión temática del prototipo.

---

## 4️⃣ Evolución por entidades

| Entidad | Prototipo | v2 | Δ | Observaciones |
|----------|-----------:|--:|--:|----------------|
| **Correos** | 4 | 70 | 🔺 +66 | Se convierte en la entidad más representada. |
| **Santander** | 7 | 40 | 🔺 +33 | Fuerte aumento de campañas bancarias. |
| **CaixaBank** | 5 | 24 | 🔺 +19 | Refuerza presencia de banca nacional. |
| **BBVA** | 10 | 16 | +6 | Ligera subida. |
| **ING** | 17 | 11 | −6 | Leve descenso. |
| **Binance / Bankinter / Sabadell / SEUR** | 0 | 4–6 | Nuevas incorporaciones. |
| **DGT / Ionos / Netflix / Orange** | 5–9 | 0 | Eliminadas — ruido global depurado. |
| **Genérico / sin marca** | 34 | 29 | −5 | Kits sin marca aún presentes pero controlados. |

**Conclusión:**  
El v2 concentra campañas **orientadas al usuario español real**, con foco en banca y logística.  
Elimina entidades internacionales irrelevantes, aumentando la calidad y coherencia del dataset.

---

## 5️⃣ Implicaciones directas en el modelo

| Aspecto | Impacto observado | Recomendación |
|----------|------------------|---------------|
| **Generalización** | Mayor diversidad semántica (banca + logística). | Mejor recall en campañas modernas. |
| **Sesgo sectorial** | Menor dependencia de banca exclusiva. | Reduce overfitting por marca. |
| **Tokens lingüísticos** | Nuevos términos: `paquete`, `aduanas`, `recibir`, `envío`. | Añadir reglas en `features_v2.py`. |
| **Infraestructura** | Más TLDs `.live`, `.app`, `.shop`. | Incluir `tld_risk_weight`. |

---

## 6️⃣ Evolución de features numéricas

| Feature | Prototipo (Phish) | v2 (Phish) | Δ (%) | Prototipo (Legit) | v2 (Legit) | Δ (%) | Observación |
|----------|------------------:|-----------:|------:|------------------:|-----------:|------:|-------------|
| **domain_length** | 11.27 | 6.33 | 🔻 −44 % | 8.14 | 7.69 | 🔻 −5 % | Dominios phishing más cortos y creíbles. |
| **domain_entropy** | 2.89 | 2.18 | 🔻 −25 % | 2.47 | 2.44 | ≈ | Menor aleatoriedad; más legibles. |
| **num_params** | 0.09 | 0.26 | 🔺 +189 % | 0.04 | 0.07 | 🔺 +82 % | Aumento de rutas con parámetros dinámicos. |

📌 **Conclusión:**  
Las URLs de phishing en v2 son **más cortas, menos caóticas y con más parámetros**, coherente con campañas modernas que imitan portales reales.

---

## 7️⃣ Evolución de features binarias

| Feature | Prototipo (%) | v2 (%) | Δ (%) | Interpretación |
|----------|---------------:|-------:|------:|----------------|
| **trusted_path_token** | 19.0 | 19.3 | ≈ | Sin cambio relevante. |
| **suspicious_path_token** | 15.0 | 48.7 | 🔺 +33.7 pp | Gran aumento de rutas engañosas (`/verify`, `/sms`, `/envio`). |
| **free_hosting** | 11.0 | 0.0 | 🔻 −11 pp | Desaparecen hostings gratuitos: campañas más profesionales. |
| **protocol (https)** | 92.5 | 88.7 | 🔻 −3.8 pp | Variación normal por muestreo. |

📌 **Conclusión:**  
Las rutas y parámetros son ahora las señales dominantes del phishing moderno.  
Las variables de infraestructura pierden relevancia predictiva.

---

## 8️⃣ Visualizaciones principales

### 📊 Distribución sectorial
![sectores](../EDA/imagenes/eda_sectores_proto_v2.png)

### 🏦 Top 10 entidades
![entidades](../EDA/imagenes/eda_entidades_proto_v2.png)

### 📈 Boxplots comparativos
![boxplots](../EDA/imagenes/eda_boxplots_proto_v2.png)

### 🔬 Correlaciones
![correlaciones](../EDA/imagenes/eda_correlaciones_proto_v2.png)

### 🔍 Variaciones relativas
![resumen](../EDA/imagenes/eda_resumen_variaciones_proto_v2.png)


---

## 9️⃣ Síntesis técnica

| Observación | Implicación |
|--------------|-------------|
| Dominios más cortos y menos caóticos | Crear `domain_complexity` o reajustar pesos de `entropy`. |
| Aumento de `num_params` | Nueva feature `param_count_boost`. |
| Incremento de `suspicious_path_token` | Subir ponderación en *scoring* (+1.5 / +2). |
| Caída de `free_hosting` | Reducir peso o eliminar del modelo. |
| Nuevas correlaciones en `path` | Añadir `path_depth` y `token_density`. |

---

## 🔟 Conclusión general del EDA comparativo

> El salto del prototipo al dataset v2 representa una **maduración del phishing en España**.  
> Las campañas son más limpias, cortas y contextualizadas, con tokens semánticos en lugar de señales técnicas.  
> El modelo debe adaptarse a esta nueva dinámica priorizando las **features lingüísticas y estructurales** sobre las de infraestructura.

---

## 11️⃣ Resumen cuantitativo del drift

El análisis final resume las diferencias relativas entre versiones:

- `domain_length`  −44 %  
- `domain_entropy`  −25 %  
- `num_params`  +189 %  
- `suspicious_path_token`  +33.7 pp  

![resumen_variaciones](../EDA/imagenes/eda_resumen_variaciones_proto_v2.png)

### 📘 Interpretación final
- **Cambio estructural:** URLs más cortas y limpias, pero con rutas más elaboradas.  
- **Cambio semántico:** predominan tokens de acción (`verificar`, `recibir`, `paquete`).  
- **Cambio predictivo:** `free_hosting` deja de ser útil; `suspicious_path_token` se convierte en la mejor señal.

### ⚙️ Implicaciones
- Rediseñar `features_v2.py` con nuevas métricas (`domain_complexity`, `tld_risk_weight`).  
- Reentrenar modelo con ponderaciones actualizadas.  
- Recalibrar umbral de decisión (≈ 0.50).

---

## ✅ Conclusión global

> El EDA confirma un **drift estructural y semántico** entre el prototipo y el dataset v2.  
>  
> El phishing actual en España utiliza **URLs más simples y específicas por sector**, priorizando la semántica de ruta sobre la infraestructura.  
>  
> Este cambio valida la creación de `features_v2.py` y el *reentrenamiento del modelo v2* con reglas y pesos adaptados a las campañas modernas.

---

**Imágenes generadas:**
- `../images/eda_boxplots_proto_v2.png`  
- `../images/eda_correlaciones_proto_v2.png`  
- `../images/eda_resumen_variaciones_proto_v2.png`
