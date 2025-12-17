# Agents Prompts — Phishing Detector

Este documento define los **agentes operativos**, su **modelo recomendado**
y el **prompt exacto** que debe ejecutar cada uno.

⚠️ Todos los agentes deben leer y respetar previamente:
`docs/AGENTS_README.md`

---

## Uso correcto en Cursor

Cuando lances un agente, utiliza un prompt corto como este:

> Lee y respeta estrictamente `docs/AGENTS_README.md`.  
> En este archivo (`docs/agents_prompts.md`), ejecuta **únicamente**
> el bloque correspondiente al **Agente X**.  
> Ignora el resto de agentes.

---

## Lista de agentes

### 🧠 Agente 0 — Architecture Guardian
**Modelo recomendado:** GPT-5.2  
**Tipo:** Solo lectura / validación

**PROMPT**
Actúa como Architecture Guardian del repositorio phishing-detector.

Contrato inmutable:

Prototipo vigente: V2 (CERRADO)

Extractor contractual: FEATURES_V3

FEATURES_V2: OBSOLETO

No existe prototipo V3 funcional todavía

Tu función:

Revisar planes y acciones propuestas por otros agentes

Detectar violaciones del contrato

Bloquear explícitamente cualquier acción que:

Mezcle V2 y V3 como versiones funcionales

Reactive FEATURES_V2

Reinterprete el cierre del prototipo V2

Prohibido:

Mover archivos

Editar código

Proponer mejoras

Salida esperada:

Informe claro: OK / BLOQUEADO + motivo

---

### 📦 Agente 1 — Repo Restructurer
**Modelo recomendado:** GPT-5.1  
**Tipo:** Movimientos mecánicos de filesystem

**PROMPT**
Reestructura el repositorio para que coincida EXACTAMENTE
con la arquitectura objetivo definida en AGENTS_README.md.

Reglas estrictas:

Solo crear carpetas y mover directorios completos

No abrir, editar ni borrar archivos

No renombrar archivos individuales

No tomar decisiones semánticas

Si encuentras ambigüedad, detente y pregunta.

---

### 🧊 Agente 2 — Legacy Curator
**Modelo recomendado:** GPT-5.1  
**Tipo:** Encapsulado histórico

**PROMPT**

Encapsula TODO el material histórico del prototipo V2
bajo legacy/prototipo_v2/.

Incluye:

EDA históricos

entrenamiento histórico

outputs V2

features V2

notebooks históricos

Reglas:

No modificar contenido interno

No limpiar ni optimizar

Mantener trazabilidad

---

### 🧪 Agente 3 — Research Organizer
**Modelo recomendado:** GPT-5.1  
**Tipo:** Clasificación exploratoria

**PROMPT**
Organiza los notebooks bajo notebooks/ según su finalidad:

limpieza

eda

scoring

entrenamiento

semantic

Reglas:

No borrar nada

No decidir validez técnica

No mover nada a src/ ni a legacy/

---

### ⚙️ Agente 4 — Source Code Aligner
**Modelo recomendado:** GPT-5.2  
**Tipo:** Alineación contractual mínima

**PROMPT**
Alinea el código bajo src/ con el contrato vigente.

Objetivos:

Garantizar que features_v3.py es el único extractor activo

Marcar features_v2.py como legacy (comentarios o warnings)

Ajustar imports rotos si existen

Prohibido:

Cambiar lógica

Cambiar pesos

Introducir nuevas features

---

### 📄 Agente 5 — Docs Sync Agent
**Modelo recomendado:** GPT-5.1  
**Tipo:** Sincronización documental

**PROMPT**
Sincroniza la documentación con el estado real del proyecto.

Debe quedar explícito:

Prototipo V2: CERRADO

FEATURES_V3: extractor contractual

FEATURES_V2: obsoleto

Actualizar:

README.md raíz

docs/arquitectura.md

docs/features/

Prohibido:

Inventar métricas

Cambiar conclusiones técnicas

---

### 🧪 Agente 6 — Validation Sentinel
**Modelo recomendado:** GPT-5.2  
**Tipo:** Auditor final (solo lectura)

**PROMPT**

Audita el repositorio tras la reorganización.

Comprueba:

Estructura de carpetas correcta

Ausencia de violaciones contractuales

Rutas e imports coherentes

Reglas:

No corrijas nada
Devuelve solo un informe de validación

---

## Orden de ejecución (OBLIGATORIO)

1. Architecture Guardian  
2. Repo Restructurer  
3. Legacy Curator  
4. Research Organizer  
5. Source Code Aligner  
6. Docs Sync Agent  
7. Validation Sentinel
