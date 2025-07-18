import pandas as pd

df = pd.read_csv('phishtank_urls.csv', encoding='latin-1')

palabras_clave = [
    '.es', 'caixabank', 'bbva', 'correos', 'sepe', 'mapfre', 'suma', 'aeat', 'renfe', 'iberdrola', 'suma', 'sabadell'
]

mask = df['url'].str.contains('|'.join(palabras_clave), case=False, na=False)
df_filtrado = df[mask]

df_filtrado.to_csv('phistank_es.csv', index = False)

print(f'Filtradas {len(df_filtrado)} URLs posiblemente españolas.')