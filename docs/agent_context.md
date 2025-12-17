
---

# 3. Separación conceptual (MANDATARIA)

Carpeta | Rol
-------|-----
**src/** | Código vigente. Todo lo que esté activo debe vivir aquí.
**legacy/** | Material histórico del prototipo V2. No ejecutable. No editable.
**notebooks/** | Investigación libre sin contrato.
**scripts/** | Utilidades sueltas no contractuales.
**docs/** | Documentación sincronizada con el estado real del sistema.

---

# 4. Reglas NO negociables para agentes

## ❌ PROHIBIDO

- Usar, importar o reactivar `features_v2.py`
- Crear nuevas features o modificar `FEATURES_V3`
- Reinterpretar versiones (V2 ≠ V3)
- Alterar modelos, métricas o resultados ya generados
- Modificar o mover contenido dentro de `legacy/`
- Ejecutar cambios sin aprobación del Architecture Guardian

## ✔ OBLIGATORIO

- Validar cualquier acción contra este contrato
- Mantener `FEATURES_V3` como **único extractor activo**
- Respetar la arquitectura objetivo
- Detenerse y preguntar ante cualquier ambigüedad

---

# 5. Excepción explícita: **SCORING_V2 ES ACTIVO**

Aunque `FEATURES_V2` está deprecado,
**SCORING_V2 sigue siendo parte del sistema operativo**  
porque **NO depende de features_v2.py**.

Reglas:

- `scripts/scoring_v2.py` **permanece fuera de legacy/**
- No debe moverse
- No debe confundirse con features_v2.py
- Puede ser ejecutado libremente

✔ Regla clave:  
**SCORING_V2 ≠ FEATURES_V2**

---

# 6. Reglas para modificar este contrato

- Ningún agente puede modificar `agent_context.md`
- Solo el usuario tiene autoridad para cambiarlo
- Si un agente detecta ambigüedad → **DEBE detenerse**

---

# 7. Uso por agentes

Todos los agentes deben:

1. Leer este archivo **antes de actuar**
2. Validar cada acción contra el contrato
3. Emitir veredicto:
   - **OK** → se puede ejecutar  
   - **BLOQUEADO** → no permitido
4. Solo ejecutar si **Architecture Guardian** da luz verde  
5. Detenerse si el flujo involucra:
   - Reactivar V2  
   - Cambiar modelos  
   - Romper la arquitectura  

---

# Fin del contrato maestro
