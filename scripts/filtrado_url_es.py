"""
Script para filtrar el dataset de PhishTank y extraer URLs relacionadas con empresas españolas.
Lee:   ../data/raw/phishtank_urls.csv
Guarda: ../data/raw/phishtank_es.csv
"""


import pandas as pd

df = pd.read_csv('../data/raw/phishtank_urls.csv')


palabras_clave = [
    '.es', 'caixabank', 'bbva', 'correos', 'sepe', 'mapfre', 'suma', 'aeat', 'renfe', 'iberdrola', 'suma', 'sabadell'
]

mask = df['url'].str.contains('|'.join(palabras_clave), case=False, na=False)
df_filtrado = df[mask]

df_filtrado.to_csv('../data/raw/phishtank_es.csv', index=False)


print(f'Filtradas {len(df_filtrado)} URLs posiblemente españolas.')