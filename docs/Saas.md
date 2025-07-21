# Scraping de URLs Legítimas – Sector SaaS / Cloud / Correo

## 1. Objetivo

Documentar el proceso de recopilación de URLs legítimas de los principales servicios SaaS, cloud y correo electrónico, para construir el dataset de entrenamiento del modelo de detección de phishing.

## 2. Lista de servicios incluidos y resultados

| Empresa       | URLs únicas | Fecha      | Observaciones principales                      |
|---------------|------------|------------|-----------------------------------------------|
| Box           | 30         | 22/07/2025 | Muchos enlaces internos en home, pero mezcla de rutas (login, ayuda, TOS, etc.) |
| Slack         | 28         | 22/07/2025 | Muchos enlaces internos en home, mezcla de rutas relevantes y otras auxiliares   |
| Google        | 4          | 22/07/2025 | Muy pocos enlaces, home minimalista           |
| Zoom          | 3          | 22/07/2025 | Muy pocos enlaces, home minimalista           |
| Fastmail      | 2          | 22/07/2025 | Home minimalista, pocos enlaces               |
| OVHcloud      | 2          | 22/07/2025 | Home minimalista, pocos enlaces               |
| Mega          | 1          | 22/07/2025 | Solo la URL principal obtenida                |
| Yandex Mail   | 1          | 22/07/2025 | Solo la URL principal obtenida                |
| iCloud        | 1          | 22/07/2025 | Solo la URL principal obtenida                |

  |

## 3. Métodos y herramientas empleadas

- **Scraping básico** realizado con `requests` y `BeautifulSoup`.
- Solo se han extraído URLs directamente visibles (home, login, recuperación, área de acceso).
- **No se ha hecho limpieza de datos, crawling, uso de palabras clave, ni Selenium** en esta fase.
- Las URLs pueden contener enlaces poco relevantes y necesitan revisión manual en fases posteriores.

## 4. Datos obtenidos

- Total de URLs recopiladas: **72**
- URLs únicas tras limpieza: **72** (sin duplicados exactos)
- Ejemplo de datos:

    | Empresa   | URL relevante                                                |
    |-----------|-------------------------------------------------------------|
    | Box       | https://account.box.com/login                                |
    | Slack     | https://slack.com/signin                                     |
    | Google    | https://accounts.google.com/signin/usernamerecovery          |
    | Zoom      | https://zoom.us/signin#nested                                |

- Guardado en: `data/raw/saas_legitimas_crudo.csv`

## 5. Problemas encontrados y soluciones

- **Desbalance**: Box y Slack aportan la mayoría de URLs; el resto de empresas tienen muy pocos resultados.
- Varias webs presentan homes minimalistas y apenas enlazan rutas internas útiles.
- No hay limpieza ni filtrado de URLs poco relevantes todavía (pendiente).
- Algunas webs pueden requerir técnicas de scraping avanzado (Selenium) para extraer rutas adicionales.

## 6. Lecciones aprendidas y recomendaciones

- El scraping básico solo es eficaz en webs con muchas rutas internas públicas.
- Para mejorar calidad y cantidad de datos:
  - Filtrar por palabras clave (“login”, “signin”, “reset”, etc.).
  - Implementar crawling más profundo.
  - Probar Selenium en webs con protección o contenido dinámico.
- Documentar siempre limitaciones de cada fase antes de iterar.

## 7. Próximos pasos

- Implementar filtrado y limpieza de URLs (palabras clave relevantes).
- Ampliar crawling y probar Selenium donde sea necesario.
- Revisar empresas con baja cobertura aplicando nuevas técnicas en el futuro.


