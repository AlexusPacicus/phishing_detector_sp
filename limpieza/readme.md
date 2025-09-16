# 🧹 Limpieza de datos

En esta carpeta se documenta el proceso de **limpieza y curación de URLs** (legítimas y de phishing) usado para construir el dataset del prototipo de detección de phishing en el contexto español.

## 📂 Estructura

limpieza/
├── legitimas/ # Limpieza sectorial de URLs legítimas
│ ├── limpieza_legitimas_banca.ipynb
│ ├── limpieza_legitimas_cripto.ipynb
│ ├── limpieza_legitimas_ecommerce.ipynb
│ ├── limpieza_legitimas_energia.ipynb
│ └── limpieza_legitimas_template.ipynb
│
├── phishing/ # Limpieza de feeds de phishing
│ ├── limpieza_phishtank.ipynb
│ ├── limpieza_1_tf.ipynb
│ ├── lotes_tf.ipynb
│ └── tweetfeed/ # Lotes de TweetFeed por mes
│
├── limpieza_pt.md 
├── limpieza_prototipo_legitimas.md
├── limpieza_prototipo_phishing.md
└── limpieza_tf.md


## 🏗️ Proceso

1. **Datos legítimos**
   - Recolectados por sector (banca, cripto, ecommerce, energía).
   - Limpieza manual y deduplicación.
   - Selección final documentada en  
     → `limpieza_prototipo_legitimas.md`.

2. **Datos de phishing**
   - Feeds principales: PhishTank, TweetFeed, OpenPhish, PhishStats, URLHaus.
   - Aplicación de heurísticas (tokens sospechosos, hosting gratuito, TLD).
   - Revisión manual en casos específicos:  
     → `limpieza_manual_pt.md`.  
   - Selección final documentada en  
     → `limpieza_prototipo_phishing.md`.

3. **Decisión final (prototipo)**
   - Elección manual de 100 legítimas + 100 phishing.  
   - Balanceadas por clase y representativas del contexto español.  
   - Base del dataset de prototipo: `dataset/dataset_prototipo.csv`.

## 📑 Documentación asociada

- `limpieza_prototipo_legitimas.md` → criterios para las 100 legítimas finales.  
- `limpieza_prototipo_phishing.md` → criterios para las 100 phishing finales.  
- `limpieza_manual_pt.md` → ejemplo de curación manual sobre feed de PhishTank.  
- `limpieza_tf.md` → notas sobre la limpieza aplicada a TweetFeed.  
