# ROADMAP v3 — Plan de Artefactos Documentales

**Versión:** 3.0  
**Estado:** EN EJECUCIÓN  
**Fecha:** Diciembre 2024

---

## Resumen ejecutivo

El pipeline v3 requiere validación documental completa antes de ejecutar la extracción de features. Este roadmap establece los hitos obligatorios y sus dependencias.

---

## Artefactos documentales obligatorios

| # | Artefacto | Ruta | Estado |
|---|-----------|------|--------|
| 1 | README modificaciones dataset v2 | `docs/limpieza/README_modificaciones_dataset_v2.md` | ✅ Completado |
| 2 | README bootstrap v3 | `docs/README_v3_bootstrap.md` | ✅ Completado |
| 3 | Manifiesto v3 | `docs/MANIFIESTO_V3.md` | ✅ Completado |
| 4 | Metadata v3 | `outputs/dataset_v3_metadata.json` | ⏳ Pendiente |

---

## Plan secuencial

```
┌─────────────────────────────────────────────────────────────────┐
│                        FASE 1: DOCUMENTACIÓN                    │
├─────────────────────────────────────────────────────────────────┤
│  HITO 1.1 → README_modificaciones_dataset_v2.md     [✅ DONE]   │
│  HITO 1.2 → README_v3_bootstrap.md                  [✅ DONE]   │
│  HITO 1.3 → MANIFIESTO_V3.md                        [✅ DONE]   │
│  HITO 1.4 → Validación Arquitectura                 [⏳ PENDING]│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   GATE CHECK    │
                    │  Arquitectura   │
                    │   debe validar  │
                    │  hitos 1.1-1.3  │
                    └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FASE 2: EXTRACCIÓN                       │
├─────────────────────────────────────────────────────────────────┤
│  HITO 2.1 → Ejecutar extract_features_dataset_v3    [⏳ BLOCKED]│
│  HITO 2.2 → Generar dataset_v3_features.csv         [⏳ BLOCKED]│
│  HITO 2.3 → Generar dataset_v3_metadata.json        [⏳ BLOCKED]│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FASE 3: VALIDACIÓN                       │
├─────────────────────────────────────────────────────────────────┤
│  HITO 3.1 → Verificar NaN == 0 en FEATURES_V3       [⏳ BLOCKED]│
│  HITO 3.2 → Verificar checksums en metadata         [⏳ BLOCKED]│
│  HITO 3.3 → Validación final Arquitectura           [⏳ BLOCKED]│
└─────────────────────────────────────────────────────────────────┘
```

---

## Detalle de hitos

### FASE 1: Documentación

#### HITO 1.1 — README_modificaciones_dataset_v2.md

| Atributo | Valor |
|----------|-------|
| Estado | ✅ Completado |
| Ruta | `docs/limpieza/README_modificaciones_dataset_v2.md` |
| Contenido | Estado contractual, decisiones de diseño, limitaciones, advertencias v3 |
| Dependencias | Ninguna |
| Validador | Arquitectura |

#### HITO 1.2 — README_v3_bootstrap.md

| Atributo | Valor |
|----------|-------|
| Estado | ✅ Completado |
| Ruta | `docs/README_v3_bootstrap.md` |
| Contenido | Contrato initialize_v3(), prohibiciones, flujo de extracción |
| Dependencias | Ninguna |
| Validador | Arquitectura |

#### HITO 1.3 — MANIFIESTO_V3.md

| Atributo | Valor |
|----------|-------|
| Estado | ✅ Completado |
| Ruta | `docs/MANIFIESTO_V3.md` |
| Contenido | Fuentes canónicas, contrato dataset, contrato features, artefactos de salida |
| Dependencias | HITO 1.1, HITO 1.2 |
| Validador | Arquitectura |

#### HITO 1.4 — Validación Arquitectura (GATE)

| Atributo | Valor |
|----------|-------|
| Estado | ⏳ Pendiente |
| Responsable | Arquitectura |
| Entrada | Hitos 1.1, 1.2, 1.3 |
| Salida | Aprobación escrita para proceder a Fase 2 |
| Criterios | Consistencia, completitud, alineación con código |

**⚠️ BLOQUEO:** La Fase 2 NO puede iniciarse sin aprobación explícita de Arquitectura.

---

### FASE 2: Extracción

#### HITO 2.1 — Ejecutar extract_features_dataset_v3

| Atributo | Valor |
|----------|-------|
| Estado | ⏳ Bloqueado por HITO 1.4 |
| Script | `scripts/extract_features_dataset_v3.py` |
| Input | `notebooks/dataset_v2.csv` |
| Precondiciones | HITO 1.4 aprobado |

#### HITO 2.2 — Generar dataset_v3_features.csv

| Atributo | Valor |
|----------|-------|
| Estado | ⏳ Bloqueado por HITO 2.1 |
| Ruta destino | `outputs/dataset_v3_features.csv` |
| Schema | 6 columnas v2 + 7 FEATURES_V3 |
| Filas esperadas | 482 |

#### HITO 2.3 — Generar dataset_v3_metadata.json

| Atributo | Valor |
|----------|-------|
| Estado | ⏳ Bloqueado por HITO 2.2 |
| Ruta destino | `outputs/dataset_v3_metadata.json` |
| Contenido obligatorio | commit_hash, checksums, fecha, configuración extractor |
| Formato | JSON según MANIFIESTO_V3 §5.2 |

---

### FASE 3: Validación

#### HITO 3.1 — Verificar NaN == 0

| Atributo | Valor |
|----------|-------|
| Estado | ⏳ Bloqueado por HITO 2.2 |
| Verificación | `df[FEATURES_V3].isna().sum().sum() == 0` |
| Fallo | Invalida dataset, requiere debugging |

#### HITO 3.2 — Verificar checksums

| Atributo | Valor |
|----------|-------|
| Estado | ⏳ Bloqueado por HITO 2.3 |
| Verificación | Checksums en metadata coinciden con fuentes actuales |
| Fallo | Invalida reproducibilidad, requiere regeneración |

#### HITO 3.3 — Validación final Arquitectura

| Atributo | Valor |
|----------|-------|
| Estado | ⏳ Bloqueado por HITO 3.1, 3.2 |
| Responsable | Arquitectura |
| Entrada | dataset_v3_features.csv, dataset_v3_metadata.json |
| Salida | Dataset v3 marcado como CONTRACTUAL |

---

## Matriz de dependencias

```
HITO 1.1 ─────┐
              │
HITO 1.2 ─────┼──→ HITO 1.4 ──→ HITO 2.1 ──→ HITO 2.2 ──→ HITO 3.1 ──┐
              │                                    │                  │
HITO 1.3 ─────┘                                    │                  │
                                                   ▼                  │
                                              HITO 2.3 ──→ HITO 3.2 ──┼──→ HITO 3.3
                                                                      │
                                                                      │
                                                              [DATASET V3 VÁLIDO]
```

---

## Checklist de ejecución

### Pre-extracción (obligatorio)

- [ ] HITO 1.1: README_modificaciones_dataset_v2.md existe y está completo
- [ ] HITO 1.2: README_v3_bootstrap.md existe y está completo
- [ ] HITO 1.3: MANIFIESTO_V3.md existe y está completo
- [ ] HITO 1.4: Arquitectura ha validado hitos 1.1-1.3
- [ ] Aprobación escrita recibida para Fase 2

### Post-extracción (obligatorio)

- [ ] HITO 2.2: dataset_v3_features.csv generado
- [ ] HITO 2.3: dataset_v3_metadata.json generado
- [ ] HITO 3.1: NaN == 0 verificado
- [ ] HITO 3.2: Checksums coinciden
- [ ] HITO 3.3: Arquitectura valida output final

---

## Prohibiciones durante ejecución

| Acción | Estado |
|--------|--------|
| Ejecutar Fase 2 sin aprobación de HITO 1.4 | ❌ PROHIBIDO |
| Modificar fuentes canónicas durante extracción | ❌ PROHIBIDO |
| Generar dataset sin metadata | ❌ PROHIBIDO |
| Marcar dataset como válido con NaN > 0 | ❌ PROHIBIDO |
| Omitir validación de checksums | ❌ PROHIBIDO |

---

## Estado actual

| Fase | Progreso | Bloqueador |
|------|----------|------------|
| Fase 1: Documentación | 75% (3/4 hitos) | Validación Arquitectura pendiente |
| Fase 2: Extracción | 0% | Bloqueada por Fase 1 |
| Fase 3: Validación | 0% | Bloqueada por Fase 2 |

**Próximo paso:** Solicitar validación de Arquitectura para hitos 1.1, 1.2, 1.3.

---

*Roadmap contractual del pipeline v3.*
