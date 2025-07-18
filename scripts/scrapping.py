"""
Script de prueba para hacer scraping básico de la web de PhishTank.
Solo muestra el título de la página.
"""



import requests

url = "https://data.phishtank.com/data/online-valid.csv"
response = requests.get(url)

with open('phistank_urls.csv', 'wb') as f:
    f.write(response.content)

print('Descargado: phistank_urls.csv')