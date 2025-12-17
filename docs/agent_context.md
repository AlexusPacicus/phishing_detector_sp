# Agents Context — Phishing Detector

Este documento define el **contexto general, el contrato técnico y la arquitectura**
del proyecto *Phishing Detector*, y sirve como **fuente única de verdad**
para cualquier agente o automatización que interactúe con el repositorio.

 Este proceso es **arquitectónico**, no de mejora funcional.

---

## 1. Estado del proyecto (CONTRATO)

- **Prototipo vigente:** V2 — **CERRADO**
- **Extractor contractual vigente:** `FEATURES_V3`
- **FEATURES_V2:** **OBSOLETO** (prohibido)
- **No existe un prototipo V3 funcional todavía**

`FEATURES_V3` es una **corrección estructural** del extractor del prototipo V2.
No constituye una nueva versión del sistema.

---

## 2. Objetivo del trabajo actual

- Reorganizar el repositorio según una arquitectura clara y defendible
- Separar explícitamente:
  - código vigente
  - histórico del prototipo V2
  - investigación exploratoria
- Mantener **inalterados**:
  - lógica
  - métricas
  - resultados
  - modelos entrenados

---

## 3. Principios no negociables

Cualquier agente o proceso automatizado debe cumplir:

- ❌ No introducir nuevas features
- ❌ No reinterpretar versiones (V2 ≠ V3)
- ❌ No reactivar `FEATURES_V2`
- ❌ No mejorar código, rendimiento o métricas
- ❌ No borrar archivos

✔ `FEATURES_V3` es el **único extractor permitido**  
✔ Ante cualquier ambigüedad → **detenerse y preguntar**

---

## 4. Arquitectura objetivo del repositorio

phishing-detector/
│
├── README.md
│
├── data/
│ ├── raw/
│ ├── interim/
│ │ └── prototipo_v2/
│ └── processed/
│ └── prototipo_v2/
│
├── docs/
│ ├── arquitectura.md
│ ├── limpieza/
│ ├── eda/
│ ├── scoring/
│ ├── features/
│ │ ├── features_v2.md # OBSOLETO
│ │ └── features_v3.md # CONTRACTUAL
│ └── inclusion/
│
├── notebooks/
│ ├── limpieza/
│ ├── eda/
│ ├── scoring/
│ ├── entrenamiento/
│ └── semantic/
│
├── src/
│ ├── scraping/
│ ├── scoring/
│ │ ├── scoring_v2.py # legacy
│ │ └── scoring_v3.py # vigente
│ ├── features/
│ │ ├── features_v2.py # legacy (prohibido)
│ │ └── features_v3.py # extractor contractual
│ ├── model/
│ └── semantic/
│
├── api/
│ └── fastapi_azure.py
│
├── models/
│ └── prototipo_v2/
│ ├── logreg_phishing.joblib
│ └── metadata.json
│
├── scripts/
├── outputs/
├── reports/
├── legacy/
│ └── _unsorted/
└── logs/

---

## 5. Separación conceptual de áreas

- **`src/`**  
  Código ejecutable alineado con el contrato vigente.

- **`legacy/`**  
  Material histórico del prototipo V2. No se modifica.

- **`notebooks/`**  
  Investigación y exploración sin contrato.

- **`docs/`**  
  Documentación viva alineada con la realidad del sistema.

---

## 6. Uso por agentes

Cualquier agente debe:
1. Leer y respetar este documento antes de actuar
2. Ajustarse estrictamente al contrato aquí descrito
3. Ejecutar solo las acciones que le correspondan según su rol operativo

Los **prompts específicos de cada agente** se definen en un documento separado.
