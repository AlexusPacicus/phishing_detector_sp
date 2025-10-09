# Whitelist de dominios españoles (Tranco)

## 1️⃣ Objetivo
Crear una lista de dominios `.es` legítimos y con tráfico real para:
- detectar coincidencias exactas o difusas con marcas españolas,
- reforzar la detección de campañas de phishing orientadas a España,
- mejorar la explicabilidad del scoring heurístico.

---

## 2️⃣ Fuente de datos
**Fuente:** [Tranco – Top 1M Domains](https://tranco-list.eu/)  
**Fecha de descarga:** YYYY-MM-DD  
**Método:** Descarga directa del CSV global `top-1m.csv`, filtrando por dominios que terminan en `.es`.  

El dataset Tranco es público y se actualiza semanalmente, lo que garantiza reproducibilidad y trazabilidad.

---

## 3️⃣ Script utilizado

```python
import pandas as pd

url_tranco = "https://tranco-list.eu/top-1m.csv"
df = pd.read_csv(url_tranco, names=["rank","domain"])
df_es = df[df["domain"].str.endswith(".es")].reset_index(drop=True)
df_es_top = df_es.head(200)
df_es_top.to_csv("data/spanish_domains.csv", index=False)
print(f"Generado data/spanish_domains.csv con {len(df_es_top)} dominios .es")
