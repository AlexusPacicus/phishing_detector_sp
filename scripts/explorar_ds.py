import pandas as pd
df = pd.read_csv('phishtank_es.csv', encoding='latin-1')
print(df.head(10))