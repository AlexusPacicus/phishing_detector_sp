def load_whitelist_v3(csv_path: str = "docs/whitelist.csv") -> set[str]:
    """
    Loader canónico v3 para la whitelist de dominios oficiales.

    - Lee docs/whitelist.csv (columna 'domain').
    - Extrae registered_domain con tldextract.
    - Normaliza a lower().strip().
    - Devuelve un set de dominios limpios.
    """
    import pandas as pd
    import tldextract

    df = pd.read_csv(csv_path)
    if "domain" not in df.columns:
        raise ValueError("Whitelist CSV debe contener una columna 'domain'.")
    wl = set()
    for d in df["domain"].dropna().astype(str):
        rd = tldextract.extract(d).registered_domain
        if rd:
            wl.add(rd.lower().strip())
    return wl


def load_brands_set_v3(csv_path: str = "docs/dominios_espanyoles.csv", constants=None):
    """
    Loader canónico v3 para el brands_set de dominios (solo core/marca).

    - Lee el csv_path (columna 'domain' o la primera si no existe 'domain')
    - Extrae el core de cada dominio con tldextract
    - Normaliza a lower().strip()
    - Guarda el set en constants["BRANDS_FROM_DOMAINS_ES"]
    - Devuelve el set
    """
    import pandas as pd
    import tldextract
    if constants is None:
        constants = {}
    df = pd.read_csv(csv_path)
    col = "domain" if "domain" in df.columns else df.columns[0]
    brands = set()
    for d in df[col].dropna().astype(str):
        core = tldextract.extract(d).domain
        if core:
            brands.add(core.lower().strip())
    constants["BRANDS_FROM_DOMAINS_ES"] = brands
    return brands


def initialize_v3(
    whitelist_path: str = "docs/whitelist.csv",
    brands_path: str = "docs/dominios_espanyoles.csv"
):
    """
    Inicializador canónico para el extractor v3.
    Carga whitelist, brands_set y constants de forma contractual.
    """
    from features.features_constantes import constants
    whitelist = load_whitelist_v3(whitelist_path)
    load_brands_set_v3(brands_path, constants)
    assert isinstance(whitelist, set) and len(whitelist) > 0
    assert "BRANDS_FROM_DOMAINS_ES" in constants
    assert isinstance(constants["BRANDS_FROM_DOMAINS_ES"], set)
    assert len(constants["BRANDS_FROM_DOMAINS_ES"]) > 0
    return whitelist, constants
