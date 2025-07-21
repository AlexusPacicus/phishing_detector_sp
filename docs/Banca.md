# Scraping de URLs Legítimas – Sector Banca

## 1. Objetivo

Documentar el proceso de recopilación de URLs legítimas de bancos en España para construir el dataset de entrenamiento del modelo de detección de phishing.

## 2. Lista de bancos incluidos y resultados

| Banco                        | URLs únicas | Fecha      | Estado / Observaciones                    |
|------------------------------|------------|------------|-------------------------------------------|
| Banco Santander              | 0          | 21/07/2025 | Intentado, sin resultados                 |
| CaixaBank                    | 3          | 21/07/2025 | Muy pocos resultados, ampliar             |
| Sabadell                     | 0          | 21/07/2025 | Intentado, sin resultados                 |
| ING España                   | 0          | 21/07/2025 | Intentado, sin resultados                 |
| Openbank                     | 32         | 21/07/2025 | Revisar login/acceso                      |
| Bankinter                    | 0          | 21/07/2025 | Intentado, sin resultados                 |
| Kutxabank                    | 4          | 21/07/2025 | Muy pocos resultados                      |
| Evo Banco                    | 0          | 21/07/2025 | Intentado, sin resultados                 |
| Unicaja Banco                | 35         | 21/07/2025 | Revisar login/acceso                      |
| Banco de España              | 671        | 22/07/2025 | OK                                        |
| Cajamar                      | 118        | 21/07/2025 | OK                                        |
| Abanca                       | 47         | 21/07/2025 | Revisar login/acceso                      |
| Santander Consumer Finance   | 0          | 22/07/2025 | Intentado, sin resultados                 |
| Banca March                  | 85         | 22/07/2025 | OK                                        |
| Ibercaja                     | 74         | 21/07/2025 | OK                                        |
| Targobank                    | 0          | 21/07/2025 | Intentado, sin resultados                 |

## 3. Métodos y herramientas empleadas

- **Scraping básico** realizado con `requests` y `BeautifulSoup`.
- Solo se han extraído URLs directamente visibles (home, login, recuperación, área cliente).
- **No se ha hecho limpieza de datos, crawling, uso de palabras clave, ni Selenium** en esta fase.
- Las URLs pueden contener duplicados y necesitan revisión manual en fases posteriores.

## 4. Datos obtenidos

- Total de URLs recopiladas: **(suma total aquí)**
- URLs únicas tras limpieza: **(pendiente de calcular)**
- Ejemplo de datos:

    | Banco          | URL relevante                                  |
    | -------------- | ---------------------------------------------- |
    | Santander      | https://www.bancosantander.es/particulares/acceso |
    | BBVA           | https://www.bbva.es/general/login/login-empresas |
    | ...            | ...                                            |

- Guardado en: `data/raw/legit_banks.csv`

## 5. Problemas encontrados y soluciones

- Varios bancos con protección (captcha, etc.): no scrapear directamente.
- Solo se han obtenido las URLs principales, por lo que la cobertura es limitada.
- No hay limpieza ni deduplicado de datos todavía (pendiente).
- Webs con pocos resultados: anotar para aplicar otras técnicas más adelante.

## 6. Lecciones aprendidas y recomendaciones

- El script básico es reutilizable para otros sectores.
- Para aumentar la cantidad y calidad de datos:
  - Limpiar y deduplicar URLs.
  - Implementar crawling y búsqueda por palabras clave (“login”, “acceso”, etc.).
  - Probar Selenium u otras técnicas anti-bot cuando sea necesario.
- Mejor empezar simple e ir añadiendo mejoras de forma iterativa.

## 7. Próximos pasos

- Scraping de servicios digitales (cloud).
- Implementar limpieza y crawling para ampliar el dataset.
- Revisar bancos sin resultados con técnicas más avanzadas en el futuro.

