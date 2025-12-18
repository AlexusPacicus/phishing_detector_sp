

import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime
DEFAULT_INPUT = "/Users/test/Desktop/phishing-detector/data/clean/phishing/phishing_v2.csv"
DEFAULT_OUT_SELECTED = "/Users/test/Desktop/phishing-detector/data/clean/phishing/phishing_v2_150.csv"
DEFAULT_OUT_HOLDOUT = "/Users/test/Desktop/phishing-detector/data/processed/phishing_v2_holdout.csv"
DEFAULT_README = "/Users/test/Desktop/phishing-detector/docs/README_inclusion_phishing_v2.md"
 
# Objetivo por sector 
DEFAULT_TARGETS = {
    "Banca": 50,
    "Logística": 30,
    "SaaS": 15,
    "Telecomunicaciones": 10,
    "Cripto": 10,
    "Retail / e-commerce": 10,
    "Administración pública": 10,
    "Energía / Seguros": 10,
    "Genérico / Otros": 5
}

FREE_HOSTING_INDICATORS = [
    "webcindario","blogspot","web.app","replit","rf.gd","wcomhost","ewp.live",
    "serveirc","tempurl","cprapid","is-certified","swtest.ru"
]

def normalize_sector(s):
    if pd.isna(s):
        return "Genérico / Otros"
    s0 = str(s).strip()
    # mapeos directos
    direct_map = {
        "Banca": "Banca",
        "Logística": "Logística",
        "Genérico": "Genérico / Otros",
        "Público": "Administración pública",
        "SaaS": "SaaS",
        "Cripto": "Cripto",
        "Telecomunicaciones": "Telecomunicaciones",
        "Retail": "Retail / e-commerce",
        "E-commerce": "Retail / e-commerce",
        "Energía": "Energía / Seguros",
        "Seguros": "Energía / Seguros"
    }
    if s0 in direct_map:
        return direct_map[s0]
    sl = s0.lower()
    if "banca" in sl or "bank" in sl:
        return "Banca"
    if any(k in sl for k in ["correos","logistica","paquete","envio","seur","ups","gls","mrw"]):
        return "Logística"
    if "saa" in sl or "saas" in sl:
        return "SaaS"
    if any(k in sl for k in ["crypto","cripto","wallet","metamask","walletconnect"]):
        return "Cripto"
    if any(k in sl for k in ["tele", "movistar", "vodafone", "orange", "yoigo", "masmovil", "digi", "pepephone"]):
        return "Telecomunicaciones"
    if any(k in sl for k in ["retail", "amazon", "carrefour", "mercadona", "elsbruch", "ecom", "pccomponentes", "mediamarkt"]):
        return "Retail / e-commerce"
    if any(k in sl for k in ["dgt","agencia","administr", "sede", "gob", "ministerio", "tributaria", "seguridad social"]):
        return "Administración pública"
    if any(k in sl for k in ["energia","endesa","iberdrola","naturgy","repsol","mapfre","seguros","mutua"]):
        return "Energía / Seguros"
    return "Genérico / Otros"

def detect_free_hosting(domain, notes=""):
    domain = str(domain or "").lower()
    notes = str(notes or "").lower()
    for ih in FREE_HOSTING_INDICATORS:
        if ih in domain or ih in notes:
            return True
    return False

def select_urls(df, targets, debug=False):
    # Solo inclusion == 1
    df = df[df.get("inclusion", 1) == 1].copy()
    # Normalizar sector
    df["sector_norm"] = df.get("sector", "").apply(normalize_sector)
    # Orden preferente: ruido asc, confianza desc, score desc
    sort_cols = []
    if "ruido" in df.columns:
        sort_cols.append("ruido")
    if "confianza" in df.columns:
        sort_cols.append("confianza")
    if "score_total_v2" in df.columns:
        sort_cols.append("score_total_v2")
    # fillna to avoid sort issues
    df[sort_cols] = df[sort_cols].fillna( (9999 if "ruido" in sort_cols else 0) )
    df = df.sort_values(by=sort_cols, ascending=[True, False, False]).reset_index(drop=True)
    selected_idx = set()
    selected_rows = []
    # 1) seleccionar por buckets objetivo
    for bucket, tgt in targets.items():
        candidates = df[df["sector_norm"] == bucket].copy()
        # excluir ya seleccionados
        candidates = candidates[~candidates.index.isin(selected_idx)]
        take = candidates.head(tgt)
        for ix, row in take.iterrows():
            selected_rows.append(row.to_dict())
            selected_idx.add(ix)
        if debug:
            print(f"[DEBUG] bucket {bucket}: wanted {tgt}, taken {len(take)}")
    # 2) completar si faltan hasta 150 con mejores restantes
    if len(selected_rows) < 150:
        remaining = df[~df.index.isin(selected_idx)].copy()
        need = 150 - len(selected_rows)
        fill = remaining.head(need)
        for ix, row in fill.iterrows():
            selected_rows.append(row.to_dict())
            selected_idx.add(ix)
        if debug:
            print(f"[DEBUG] filled with {len(fill)} remaining rows to reach 150")
    # 3) asegurar longitud 150
    selected_rows = selected_rows[:150]
    df_selected = pd.DataFrame(selected_rows).reset_index(drop=True)
    df_selected["dataset_split"] = "train_val"
    # 4) holdout = resto de inclusion==1 no seleccionadas
    selected_urls = set(df_selected["url"].tolist())
    df_holdout = df[~df["url"].isin(selected_urls)].copy().reset_index(drop=True)
    df_holdout["dataset_split"] = "holdout"
    return df_selected, df_holdout

def generate_readme(df_original, df_selected, df_holdout, targets, out_readme):
    now = datetime.utcnow().isoformat() + "Z"
    lines = []
    lines.append("# README — Inclusión phishing v2\n")
    lines.append(f"Generado: {now}\n")
    lines.append("## Resumen\n")
    lines.append(f"- Fuente: `{Path(args.input).name}`\n")
    lines.append(f"- Total filas con inclusion==1 en el origen: {len(df_original)}\n")
    lines.append(f"- Seleccionadas para `phishing_v2_150.csv`: {len(df_selected)}\n")
    lines.append(f"- Restantes en `phishing_v2_holdout.csv`: {len(df_holdout)}\n")
    lines.append("\n## Criterios de inclusión\n")
    lines.append("- Se consideran sólo URLs con `inclusion == 1` (curadas manualmente)\n")
    lines.append("- Orden de preferencia: `ruido` ascendente, `confianza` descendente, `score_total_v2` descendente\n")
    lines.append("- Normalización de sectores y asignación por buckets objetivo\n")
    lines.append("- Si un sector no tiene suficientes candidatos, se rellenó con las mejores URLs restantes\n")
    lines.append("\n## Objetivos por sector\n")
    for k, v in targets.items():
        lines.append(f"- {k}: objetivo {v} URLs\n")
    lines.append("\n## Distribución final en el archivo seleccionado\n")
    for s, c in df_selected["sector_norm"].value_counts().items():
        lines.append(f"- {s}: {c}\n")
    lines.append("\n## Observaciones\n")
    lines.append("- El dataset original está muy sesgado hacia Banca y Logística. Se cubrieron los huecos con 'Genérico / Otros' y mejores restantes.\n")
    lines.append("- Recomendación: recolectar activamente URLs en SaaS, Telecomunicaciones, Cripto, Retail y Energía/Seguros para futuras versiones.\n")
    lines.append("\n## Archivos generados\n")
    lines.append(f"- `{Path(args.out_selected).name}` — dataset principal v2 (150 URLs)\n")
    lines.append(f"- `{Path(args.out_holdout).name}` — holdout (resto de URLs verificadas)\n")
    lines.append("\n---\n")
    with open(out_readme, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_readme

def main(args):
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    df = pd.read_csv(str(input_path))
    df_selected, df_holdout = select_urls(df, args.targets, debug=args.debug)
    # Guardar CSVs
    Path(args.out_selected).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_holdout).parent.mkdir(parents=True, exist_ok=True)
    df_selected.to_csv(args.out_selected, index=False)
    df_holdout.to_csv(args.out_holdout, index=False)
    rd = generate_readme(df, df_selected, df_holdout, args.targets, args.out_readme)
    print(f"Selected: {args.out_selected} ({len(df_selected)})")
    print(f"Holdout:  {args.out_holdout} ({len(df_holdout)})")
    print(f"README:   {rd}")
    return 0

if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="select_phishing_v2.py", description="Selecciona 150 URLs phishing para v2 y genera holdout + README")
    p.add_argument("--input", default=DEFAULT_INPUT, help="CSV de entrada con columnas como 'url','sector','inclusion','ruido','confianza' (default: %(default)s)")
    p.add_argument("--out_selected", default=DEFAULT_OUT_SELECTED, help="CSV de salida con 150 URLs (default: %(default)s)")
    p.add_argument("--out_holdout", default=DEFAULT_OUT_HOLDOUT, help="CSV de salida con holdout (default: %(default)s)")
    p.add_argument("--out_readme", default=DEFAULT_README, help="README de inclusión (default: %(default)s)")
    p.add_argument("--debug", action="store_true", help="Imprime mensajes debug durante la selección")
    # permitir pasar targets como JSON string opcional
    p.add_argument("--targets", type=str, default=None, help="JSON string con targets por sector. Si se pasa, sobreescribe DEFAULT_TARGETS.")
    args = p.parse_args()
    # cargar targets si se pasan
    import json
    if args.targets:
        try:
            args.targets = json.loads(args.targets)
        except Exception as e:
            raise ValueError("Error parsing --targets JSON: " + str(e))
    else:
        args.targets = DEFAULT_TARGETS
    main(args)
