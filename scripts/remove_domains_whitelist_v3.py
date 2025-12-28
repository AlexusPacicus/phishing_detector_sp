"""
Script para eliminar dominios específicos de whitelist v3.
Elimina exactamente los 7 dominios validados por EDA.
"""

import pandas as pd
from datetime import datetime
import os

# Dominios a eliminar (validados por EDA)
DOMINIOS_A_ELIMINAR = {
    "amazonaws.com",
    "azure.com",
    "githubstatus.com",
    "hetzner.com",
    "ionos.es",
    "linode.com",
    "ovh.com",
}


def main():
    whitelist_path = "docs/whitelist.csv"
    
    # 1. Crear backup con timestamp
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"docs/whitelist_backup_{fecha}_final.csv"
    
    print("=" * 80)
    print("ELIMINACIÓN DE DOMINIOS DE WHITELIST V3")
    print("=" * 80)
    
    print(f"\n1. Creando backup: {backup_path}")
    df_backup = pd.read_csv(whitelist_path, encoding="utf-8", on_bad_lines="skip")
    df_backup.to_csv(backup_path, index=False)
    
    # Verificar que el backup se creó antes de continuar
    if not os.path.exists(backup_path):
        raise RuntimeError("No se creó el backup, abortando para proteger la whitelist.")
    
    print(f"   Backup creado: {len(df_backup)} dominios")
    
    # 2. Cargar whitelist actual
    print(f"\n2. Cargando {whitelist_path}")
    df = pd.read_csv(whitelist_path, encoding="utf-8", on_bad_lines="skip")
    total_inicial = len(df)
    print(f"   Total inicial: {total_inicial} dominios")
    
    # 3. Verificar qué dominios están presentes
    print(f"\n3. Verificando dominios a eliminar...")
    dominios_presentes = df[df["domain"].isin(DOMINIOS_A_ELIMINAR)]["domain"].tolist()
    print(f"   Dominios encontrados para eliminar: {len(dominios_presentes)}")
    for d in sorted(dominios_presentes):
        print(f"     - {d}")
    
    dominios_no_encontrados = DOMINIOS_A_ELIMINAR - set(dominios_presentes)
    if dominios_no_encontrados:
        print(f"   ⚠️  Dominios no encontrados en whitelist:")
        for d in sorted(dominios_no_encontrados):
            print(f"     - {d}")
    
    # 4. Eliminar dominios
    print(f"\n4. Eliminando dominios...")
    df_limpio = df[~df["domain"].isin(DOMINIOS_A_ELIMINAR)].copy()
    eliminados = total_inicial - len(df_limpio)
    print(f"   Dominios eliminados: {eliminados}")
    
    # 5. Guardar CSV limpio
    print(f"\n5. Guardando CSV limpio...")
    df_limpio.to_csv(whitelist_path, index=False)
    total_final = len(df_limpio)
    print(f"   Total final: {total_final} dominios")
    
    # 6. Verificar rango objetivo
    print(f"\n6. Verificación de rango objetivo (240-250):")
    if 240 <= total_final <= 250:
        print(f"   ✓ Total ({total_final}) está en rango 240-250")
    else:
        print(f"   ⚠️  Total ({total_final}) NO está en rango 240-250")
    
    # 7. Resumen final
    print(f"\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Backup creado: {backup_path}")
    print(f"Dominios eliminados: {eliminados}")
    print(f"Total inicial: {total_inicial}")
    print(f"Total final: {total_final}")
    print(f"\nDominios eliminados:")
    for d in sorted(dominios_presentes):
        print(f"  - {d}")


if __name__ == "__main__":
    main()

