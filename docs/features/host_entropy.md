### 🧩 Feature: host_entropy (v2.3, revisada)

**Objetivo:** medir la aleatoriedad y complejidad del *subdominio*, sin solaparse con `domain_complexity`.

**Definición:**

1) `subdomain_clean = subdomain.replace(".", "")`

2) `host_entropy` se calcula como entropía de Shannon sobre `subdomain_clean`:
   - Si `subdomain_clean == ""` → `host_entropy = 0`
   - En otro caso:
     H = −Σ p(c) · log₂ p(c), donde p(c) es la frecuencia relativa de cada carácter.

**Motivación:**
- Captura ruido estructural típico de kits automáticos (`ingress-*`, `cprapid`, `builderall`…)
- No interfiere con `domain_complexity`, que opera sobre el *registered_domain*.

---

### 🔍 Subfeature auxiliar: `subdomain_missing_flag`

Para cubrir campañas modernas sin subdominio:

- `subdomain_missing_flag = 1` si:
  - `subdomain == ""` **y**
  - `TLD` no es `.es`
- En otro caso: `0`

**Motivación:**  
La mayoría del phishing sin subdominio (p.ej. `.xyz`, `.shop`, `.co.za`, `.com.vn`) aparece en este patrón; muy pocas webs legítimas españolas lo siguen.

---

### ✔️ Propiedades

- No pisa `domain_complexity`.
- No introduce doble conteo.
- `host_entropy` sigue siendo una feature especializada (solo subdominio).
- `subdomain_missing_flag` añade una señal ligera pero útil sin romper la semántica original.
