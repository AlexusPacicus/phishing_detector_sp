"""
Script de limpieza de whitelist v3.
Elimina dominios no válidos según especificaciones contractuales.
"""

import pandas as pd
from datetime import datetime
import os

# Dominios a eliminar
DOMINIOS_A_ELIMINAR = {
    # Infraestructura o SaaS global
    "vercel.app",
    "vercel.com",
    "render.com",
    "webnode.es",
    "blogspot.com.es",
    "blogs.es",
    "s3.amazonaws.com",
    "windows.net",
    "cdn.shopify.com",
    "shopify.com",
    "cloudfront.net",
    "fastly.net",
    "fastlylb.net",
    "akamaiedge.net",
    "google.com",
    "google.es",
    "gmail.com",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "meta.com",
    "microsoft.com",
    "office.com",
    "office365.com",
    "outlook.com",
    "paypal.com",
    "stripe.com",
    "slack.com",
    "zoom.us",
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "atlassian.com",
    "okta.com",
    "auth0.com",
    "oracle.com",
    "salesforce.com",
    "cloudflare.com",
    "aws.amazon.com",
    "digitalocean.com",
    "cloudinary.com",
    "akamai.com",
    "akamaitechnologies.com",
    "dropbox.com",
    "dropboxusercontent.com",
    # Contenido adulto o irrelevante
    "xnxx.es",
    "xvideos.es",
    # Medios/lifestyle sin valor de seguridad
    "vogue.es",
    "glamour.es",
    "revistavanityfair.es",
    "fotogramas.es",
    "bonviveur.es",
    "fragrantica.es",
    "tvguia.es",
}


def main():
    whitelist_path = "docs/whitelist.csv"
    
    # 1. Crear backup con fecha
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"docs/whitelist_backup_{fecha}.csv"
    
    print(f"1. Creando backup: {backup_path}")
    df_backup = pd.read_csv(whitelist_path, encoding="utf-8", on_bad_lines="skip")
    df_backup.to_csv(backup_path, index=False)
    
    # Verificar que el backup se creó antes de continuar
    if not os.path.exists(backup_path):
        raise RuntimeError("No se creó el backup, abortando para proteger la whitelist.")
    
    print(f"   Backup creado: {len(df_backup)} dominios")
    
    # 2. Cargar whitelist
    print(f"\n2. Cargando {whitelist_path}")
    df = pd.read_csv(whitelist_path, encoding="utf-8", on_bad_lines="skip")
    total_inicial = len(df)
    print(f"   Total inicial: {total_inicial} dominios")
    
    # 3. Eliminar dominios especificados
    print(f"\n3. Eliminando dominios no válidos...")
    df_limpio = df[~df["domain"].isin(DOMINIOS_A_ELIMINAR)].copy()
    eliminados = total_inicial - len(df_limpio)
    print(f"   Eliminados: {eliminados} dominios")
    
    # Eliminar espacios y filas vacías
    df_limpio["domain"] = df_limpio["domain"].astype(str).str.strip()
    df_limpio = df_limpio[df_limpio["domain"] != ""]
    df_limpio = df_limpio[df_limpio["domain"] != "nan"]
    
    # 4. Guardar CSV limpio
    print(f"\n4. Guardando CSV limpio...")
    df_limpio.to_csv(whitelist_path, index=False)
    total_final = len(df_limpio)
    print(f"   Total final: {total_final} dominios")
    
    # 5. Verificar que sea < 250
    print(f"\n5. Verificación:")
    if total_final < 250:
        print(f"   ✓ Total ({total_final}) es inferior a 250")
    else:
        print(f"   ✗ Total ({total_final}) NO es inferior a 250")
    
    # Mostrar dominios eliminados
    print(f"\nDominios eliminados:")
    eliminados_list = df[df["domain"].isin(DOMINIOS_A_ELIMINAR)]["domain"].tolist()
    for dom in sorted(eliminados_list):
        print(f"  - {dom}")


if __name__ == "__main__":
    main()

