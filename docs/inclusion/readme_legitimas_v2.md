# README — Inclusión de URLs Legítimas (v2)

**Fecha de cierre**: 23/10/2025
**Responsable**: Alexis Zapico Fernández
**Dataset resultante**: `legitimas_v2_final.csv` (150 URLs)

---

## 🌟 Objetivo

Construir un conjunto actualizado de 150 URLs legítimas verificadas manualmente, cubriendo múltiples sectores con especial enfoque en el contexto español. Este conjunto se usará para:

* Mejorar la detección de falsos positivos del modelo actual.
* Servir de contrapeso semántico frente al phishing real.
* Evaluar robustez por sector, entidad y tipo de ruta.

---

## 📊 Distribución por sectores

| Sector                        | Nº URLs |  % aprox |
| ----------------------------- | ------: | -------: |
| 🏦 Banca                      |      59 |    39.3% |
| 🚚 Logística                  |      36 |    24.0% |
| ☁️ SaaS / Cloud / Plataformas |      10 |     6.7% |
| 📱 Telecomunicaciones         |      10 |     6.7% |
| 💳 Cripto / Fintech           |      10 |     6.7% |
| 🔌 Energía / Seguros          |      10 |     6.7% |
| 🏛️ Administración pública    |       5 |     3.3% |
| 🛒 Retail / e-commerce        |      10 |     6.7% |
| ⚙️ Genérico / Otros           |      10 |     6.7% |
| **TOTAL**                     | **150** | **100%** |

Cada sector está documentado por separado en `docs/legitimas_v2.md`, con detalle de entidades, rutas utilizadas y justificaciones.

---

## 🪡 Criterios globales de inclusión

* Selección manual desde portales oficiales, verificando que la página responda correctamente.
* Evitar URLs con contenido genérico, homepages sin contexto o enlaces inactivos.
* Cobertura semántica variada: login, clientes, facturas, soporte, sede, API, etc.
* Incorporar casos "hard negatives": URLs válidas que pueden parecer sospechosas (subdominios, callbacks, token en ruta o parámetros).
* Exclusión de cualquier URL ya presente en `legitimas_final.csv` del prototipo.

---

## 🔹 Validación manual

* Todas las URLs fueron revisadas visualmente el 22 de octubre de 2025.
* Se garantizó su operatividad (carga completa de la página) y su pertenencia a entidades reales.
* Se completaron los campos:

  * `url`, `sector`, `entidad`, `route_type`, `source`, `confidence`, `timestamp`

---

## 🔍 Cobertura semántica y valor para el modelo

Las rutas incluidas aportan diversidad y tokens valiosos para el modelo, como:

* `clientes`, `area-cliente`, `sede`, `tramites`, `seguridad`, `faq`, `contacto`, `facturas`, `login`, `dashboard`, `soporte`, `status`, etc.

Se incluyeron rutas complejas como:

* URLs con parámetros (`orderID`, `?token=...`)
* Subdominios de autenticación (`auth0`, `login.microsoftonline.com`)
* Páginas técnicas y de integración (`/docs`, `/api`, `/callback`)

Estas aportaciones ayudan a entrenar mejor la feature `trusted_path_token` y a reducir el sesgo hacia estructuras simplificadas.

