# scripts/scoring_v1.py

import re
from urllib.parse import urlparse

# === Fallback fuzzy matcher ===
try:
    from rapidfuzz import fuzz
except ImportError:
    from difflib import SequenceMatcher
    def fuzz_ratio(a, b):
        return int(100 * SequenceMatcher(None, a, b).ratio())
    fuzz = type("FallbackFuzz", (), {"ratio": staticmethod(fuzz_ratio)})

# === Función principal ===

def score_url_v1(url: str, spanish_whitelist: list[str]) -> tuple[int, str]:
    """
    Scoring v1.0 — basado en señales específicas para campañas orientadas a España.
    Requiere una whitelist de dominios españoles conocidos.
    
    Args:
        url (str): URL completa
        spanish_whitelist (list[str]): lista de dominios válidos en minúscula

    Returns:
        score (int): puntuación total
        signals (str): señales activadas separadas por ';'
    """
    url_low = str(url).lower()
    parsed = urlparse(url_low)
    netloc = parsed.netloc or ''
    path = parsed.path or ''
    query = parsed.query or ''
    domain_core = netloc.split('.')[-2] if '.' in netloc else netloc

    score = 0
    signals = []

    # --- Listas base ---
    POSITIVE_KEYWORDS = ['multa','pago','verificación','cliente','acceso','seguridad','confirmación','factura','tarjeta']
    SPANISH_MARKERS = ['.es', '+34', '€']
    SPANISH_BRANDS = [
    # 🏦 Banca
    "bbva", "santander", "caixabank", "bankia", "bankinter", "openbank", "evo", "abanca",
    "unicaja", "kutxabank", "cajarural", "ing", "imaginbank",

    # 📡 Telecomunicaciones
    "movistar", "orange", "jazztel", "yoigo", "masmovil", "lowi", "pepephone",

    # ✉️ Envíos y logística
    "correos", "mrw", "seur", "gls", "nacex", "dhl", "envialia",

    # ⚡ Energía
    "iberdrola", "endesa", "naturgy", "repsol", "totalenergies",

    # 🛒 E-commerce y consumo
    "elcorteingles", "zara", "aliexpress", "amazon", "carrefour", "mediamarkt", "pccomponentes",

    # 🧾 Administración y servicios públicos
    "dgt", "aeat", "seg-social", "sede", "mapfre", "fnmt", "redsara", "catastro", "interior",

    # 💻 Hosting / servicios web conocidos en ES
    "ionos", "dinahosting", "hostalia", "cdmon"
]

    SPANISH_HOSTINGS = ['webcindario','rf.gd']

    GENERIC_SP_TOKENS = [
        'servicio','soporte','atencion','cliente','usuarios','ayuda','asistencia',
        'cuenta','acceso','inicio','login','sesion','datos','perfil','portal',
        'seguridad','verificacion','confirmacion','actualizacion','validacion','auth','clave','codigo',
        'envio','entrega','paquete','pedido','multa','factura','notificacion','aviso',
        'gob','oficial','tramite','tramites','agencia','impuestos','certificado'
    ]

    BANKING_TOKENS = [
        'banco','banca','bank','banking','transferencia','tarjeta','pin','clave','codigo','validacion',
        'firma','token','sms','autenticacion','movimientos','saldo','oficinavirtual','bancamovil',
        'appbanco','bancadigital','acceso','usuarios','verificacion','serviciocliente','soportecliente'
    ]

    INSTITUTIONAL_TOKENS = [
        'ayuntamiento','gob','gobierno','agencia','tramite','tramites','oficial','certificado',
        'seg-social','catastro','impuestos','tributos','dgt','hacienda','dni','salud','sanidad'
    ]

    PROFESSIONAL_TOKENS = [
        'asesoria','gestoria','abogado','despacho','consultoria','contable','laboral','fiscal','bufete','notaria'
    ]

    ECOMMERCE_TOKENS = [
        'pedido','pedidos','compra','compras','factura','facturas','recibo','recibos',
        'abonado','tarifa','tarifas','servicios','renovar','renovacion','contrato',
        'suscripcion','envio','entrega','paquete','envios','devolucion'
    ]

    LATAM_TLDS = ['.co', '.mx', '.cl', '.ar', '.br', '.pe', '.ec', '.uy', '.py', '.bo', '.sv', '.hn', '.cr', '.gt', '.do']
    GLOBAL_TLDS = ['.com', '.app', '.net', '.org', '.io', '.web.app', '.dev']

    # --- Reglas base ---
    for kw in POSITIVE_KEYWORDS:
        if kw in url_low:
            score += 1
            signals.append(f'has_kw:{kw}')

    for m in SPANISH_MARKERS:
        if m in url_low:
            score += 2 if m == '.es' else 1
            signals.append(f'spanish_marker:{m}')

    for b in SPANISH_BRANDS:
        if b in url_low:
            score += 1
            signals.append(f'spanish_brand:{b}')

    for h in SPANISH_HOSTINGS:
        if h in url_low:
            score += 2
            signals.append(f'spanish_hosting:{h}')

    if '.com.es' in url_low:
        score += 2
        signals.append('tld_combo_com_es')

    # --- Patrones acción + entrega ---
    verbs = ['modifica','modificar','actualiza','actualizar','cambia','cambiar','reprograma','reprogramar','ajusta','ajustar','corrige','corregir']
    delivery = ['entrega','envio','envío','pedido','paquete']
    hyphen_pattern = re.compile(r'(' + '|'.join(verbs) + r')[-_%2d]*(tu|mi|su)?[-_%2d]*(' + '|'.join(delivery) + r')', flags=re.IGNORECASE)
    if hyphen_pattern.search(url_low):
        m = hyphen_pattern.search(url_low)
        score += 2
        signals.append(f'action_delivery:{m.group(0)}')

    if any(h in url_low for h in ['github.io','forms.app','pages.dev','pages.github','netlify.app','webflow.io']):
        if any(tok in url_low for tok in delivery):
            score += 2
            signals.append('susp_hoster_plus_delivery')

    # --- Semánticas combinadas con .es ---
    if '.es' in url_low:
        if sum(tok in url_low for tok in GENERIC_SP_TOKENS) >= 2:
            score += 3
            signals.append('generic_service_combo_es')
        if any(tok in url_low for tok in BANKING_TOKENS):
            score += 3
            signals.append('banking_combo_es')
        if any(tok in url_low for tok in INSTITUTIONAL_TOKENS + PROFESSIONAL_TOKENS):
            score += 3
            signals.append('institutional_professional_es')
        if any(tok in url_low for tok in ECOMMERCE_TOKENS):
            score += 2
            signals.append('ecommerce_combo_es')

    # --- Whitelist exacta o fuzzy ---
    for legit in spanish_whitelist:
        if legit in url_low:
            score += 2
            signals.append(f'spanish_whitelist_match:{legit}')
            break
        else:
            legit_base = legit.split('.')[0]
            sim = fuzz.ratio(domain_core, legit_base)
            if sim >= 80:
                score += 2
                signals.append(f'fuzzy_whitelist_match:{legit}:{sim:.0f}')
                break

    # --- Reglas recuperación ---
    spanish_tokens_for_brand = ['ayuda','cliente','esapp','es','spain','movil','ayuntamiento','paqueteria','paquete','envio','entrega']
    if any(b in url_low for b in SPANISH_BRANDS) and any(tok in url_low for tok in spanish_tokens_for_brand):
        score += 2
        signals.append('brand_plus_spanish_token')

    try:
        parts = netloc.split('.')
        if len(parts) > 2:
            subparts = parts[:-2]
            subdomain_str = '.'.join(subparts)
            if any(b in subdomain_str for b in SPANISH_BRANDS):
                score += 2
                signals.append('brand_in_subdomain')
    except:
        pass

    shorteners = ['l.ead.me','bit.ly','t.co','tinyurl.com','ow.ly','is.gd']
    if any(s in netloc for s in shorteners):
        short_tokens = ['spain','es','dgt','bbva','correos','ing','santander','caixabank']
        if any(tok in path or tok in query for tok in short_tokens):
            score += 2
            signals.append('shortener_spain')

    # --- Boost marca en TLD global sin .es ---
    try:
        has_spanish_brand = any(b in url_low for b in SPANISH_BRANDS)
        host_has_global_tld = any(tld in netloc for tld in GLOBAL_TLDS)
        host_has_es = '.es' in netloc
        if has_spanish_brand and host_has_global_tld and not host_has_es:
            score += 1
            signals.append('brand_global_tld_boost')
    except:
        pass

    # --- Penalizaciones LATAM ---
    for tld in LATAM_TLDS:
        if url_low.endswith(tld) or f"{tld}/" in url_low:
            score -= 2
            signals.append(f'latam_tld:{tld}')

    for pk in ['pagamento','fatura','acesso','faturas']:
        if pk in url_low:
            score -= 2
            signals.append(f'pt_kw:{pk}')

    for lb in ['banrural','pichincha','itau','bradesco','yape','daviplata']:
        if lb in url_low:
            score -= 1
            signals.append(f'latam_brand:{lb}')

    for brand in SPANISH_BRANDS:
        sim = fuzz.ratio(domain_core, brand)
        if sim >= 80:
            score += 2
            signals.append(f'fuzzy_brand_match:{brand}:{sim:.0f}')
            break

    return score, ';'.join(signals)
