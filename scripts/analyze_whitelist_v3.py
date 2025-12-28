"""
Script de análisis de whitelist v3.
Compara whitelist actual vs backup y propone eliminaciones adicionales.
"""

import pandas as pd
import tldextract
from collections import Counter

# Dominios que deberían haberse eliminado
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


def extract_tld(domain):
    """Extrae TLD de un dominio."""
    try:
        ext = tldextract.extract(domain)
        return ext.suffix.lower() if ext.suffix else ""
    except:
        return ""


def analyze_whitelist():
    whitelist_path = "docs/whitelist.csv"
    backup_path = "docs/whitelist_backup_20251213_111136.csv"
    
    print("=" * 80)
    print("ANÁLISIS DE WHITELIST V3")
    print("=" * 80)
    
    # 1. Cargar ambos CSVs
    print(f"\n1. Cargando archivos...")
    df_current = pd.read_csv(whitelist_path, encoding="utf-8", on_bad_lines="skip")
    df_backup = pd.read_csv(backup_path, encoding="utf-8", on_bad_lines="skip")
    
    print(f"   Whitelist actual: {len(df_current)} dominios")
    print(f"   Backup: {len(df_backup)} dominios")
    
    # 2. Comparar y detectar dominios que deberían haberse eliminado
    print(f"\n2. Verificando dominios a eliminar...")
    current_domains = set(df_current["domain"].str.strip().str.lower())
    backup_domains = set(df_backup["domain"].str.strip().str.lower())
    
    dominios_en_backup = backup_domains & DOMINIOS_A_ELIMINAR
    dominios_en_actual = current_domains & DOMINIOS_A_ELIMINAR
    
    print(f"   Dominios a eliminar encontrados en backup: {len(dominios_en_backup)}")
    if dominios_en_backup:
        for d in sorted(dominios_en_backup):
            print(f"     - {d}")
    
    print(f"   Dominios a eliminar aún presentes en actual: {len(dominios_en_actual)}")
    if dominios_en_actual:
        for d in sorted(dominios_en_actual):
            print(f"     - {d}")
    
    # 3. Análisis de TLDs
    print(f"\n3. Análisis de TLDs (whitelist actual)...")
    df_current["tld"] = df_current["domain"].apply(extract_tld)
    tld_counts = df_current["tld"].value_counts()
    
    print(f"   Total TLDs únicos: {len(tld_counts)}")
    print(f"   Top 15 TLDs:")
    for tld, count in tld_counts.head(15).items():
        print(f"     {tld}: {count}")
    
    # 4. Detectar ruido residual (patrones sospechosos)
    print(f"\n4. Detección de ruido residual...")
    
    # Patrones de infraestructura/SaaS
    infra_patterns = [
        "cloudflare", "cloudfront", "amazonaws", "azure", "googleapis",
        "googleusercontent", "githubusercontent", "cdn", "akamai",
        "fastly", "digitalocean", "hetzner", "linode", "ovh", "ionos"
    ]
    
    # Patrones de medios/lifestyle
    medios_patterns = [
        "vogue", "glamour", "vanityfair", "fotogramas", "bonviveur",
        "fragrantica", "tvguia", "instyle"
    ]
    
    # Patrones de contenido adulto
    adult_patterns = ["xnxx", "xvideos"]
    
    # Dominios con subdominios de infraestructura
    infra_domains = []
    medios_domains = []
    adult_domains = []
    
    for domain in current_domains:
        domain_lower = domain.lower()
        
        # Infraestructura
        if any(pattern in domain_lower for pattern in infra_patterns):
            infra_domains.append(domain)
        
        # Medios
        if any(pattern in domain_lower for pattern in medios_patterns):
            medios_domains.append(domain)
        
        # Adulto
        if any(pattern in domain_lower for pattern in adult_patterns):
            adult_domains.append(domain)
    
    print(f"   Dominios de infraestructura detectados: {len(infra_domains)}")
    if infra_domains:
        for d in sorted(infra_domains):
            print(f"     - {d}")
    
    print(f"   Dominios de medios/lifestyle detectados: {len(medios_domains)}")
    if medios_domains:
        for d in sorted(medios_domains):
            print(f"     - {d}")
    
    print(f"   Dominios de contenido adulto detectados: {len(adult_domains)}")
    if adult_domains:
        for d in sorted(adult_domains):
            print(f"     - {d}")
    
    # 5. Proponer eliminaciones adicionales
    print(f"\n5. Propuesta de eliminaciones adicionales...")
    
    # Combinar todos los candidatos a eliminar
    candidatos_eliminar = set()
    
    # Agregar dominios que deberían haberse eliminado pero aún están
    candidatos_eliminar.update(dominios_en_actual)
    
    # Agregar dominios de infraestructura detectados
    candidatos_eliminar.update(infra_domains)
    
    # Agregar dominios de medios detectados
    candidatos_eliminar.update(medios_domains)
    
    # Agregar dominios de contenido adulto
    candidatos_eliminar.update(adult_domains)
    
    # Agregar otros patrones sospechosos (solo los más claros de infraestructura)
    otros_sospechosos = []
    for domain in current_domains:
        domain_lower = domain.lower()
        
        # Subdominios de servicios globales (CDN/infraestructura pura)
        if any(x in domain_lower for x in ["githubstatus", "paypalobjects", "stripe.network", 
                                            "walletconnect", "fbcdn", "gstatic", "uecdn",
                                            "cloudflareinsights", "cloudflarestatus", "cloudflarestream",
                                            "githubusercontent", "googleapis", "googleusercontent",
                                            "cdn.apple-cloudkit"]):
            otros_sospechosos.append(domain)
        
        # Dominios de hosting genérico
        if any(x in domain_lower for x in ["metooo", "mi-dominio"]):
            otros_sospechosos.append(domain)
        
        # Hosting providers (mantener solo los más claros)
        if domain_lower in ["hetzner.com", "linode.com", "ovh.com", "ionos.es", "azure.com", "amazonaws.com"]:
            otros_sospechosos.append(domain)
    
    candidatos_eliminar.update(otros_sospechosos)
    
    # Ajustar para llegar a rango 240-250
    total_actual = len(df_current)
    objetivo_min = 240
    objetivo_max = 250
    objetivo_ideal = 245
    eliminaciones_ideales = total_actual - objetivo_ideal  # 7
    
    # Priorizar candidatos por criticidad (infraestructura pura primero)
    candidatos_priorizados = [
        # Infraestructura crítica (CDN/hosting puro) - más críticos primero
        "amazonaws.com", "azure.com", "hetzner.com", "linode.com", "ovh.com", "ionos.es",
        # Subdominios de servicios globales
        "githubstatus.com", "githubusercontent.com", "googleapis.com", "googleusercontent.com",
        "fbcdn.net", "gstatic.com", "uecdn.es", "cdn.apple-cloudkit.com",
        "cloudflareinsights.com", "cloudflarestatus.com", "cloudflarestream.com",
        "paypalobjects.com", "stripe.network", "walletconnect.network",
        # Hosting genérico
        "metooo.es", "mi-dominio.es",
        # Medios/lifestyle
        "instyle.es"
    ]
    
    # Seleccionar solo los candidatos que están en la lista priorizada y en el set
    # Tomar exactamente los necesarios para llegar al objetivo ideal
    candidatos_finales = []
    for cand in candidatos_priorizados:
        if cand in candidatos_eliminar:
            candidatos_finales.append(cand)
            if len(candidatos_finales) >= eliminaciones_ideales:
                break
    
    candidatos_eliminar = set(candidatos_finales)
    total_propuesto = total_actual - len(candidatos_eliminar)
    
    print(f"   Candidatos iniciales detectados: {len(candidatos_eliminar) + (len(candidatos_priorizados) - len(candidatos_finales))}")
    print(f"   Candidatos finales seleccionados: {len(candidatos_eliminar)}")
    print(f"   Total actual: {total_actual}")
    print(f"   Total propuesto: {total_propuesto}")
    print(f"   Objetivo ideal: {objetivo_ideal} (eliminaciones: {eliminaciones_ideales})")
    
    if total_propuesto < 240:
        print(f"   ⚠️  Total propuesto ({total_propuesto}) es menor a 240")
    elif total_propuesto > 250:
        print(f"   ⚠️  Total propuesto ({total_propuesto}) es mayor a 250")
    else:
        print(f"   ✓ Total propuesto ({total_propuesto}) está en rango 240-250")
    
    print(f"\n   Lista completa de candidatos a eliminar:")
    for d in sorted(candidatos_eliminar):
        print(f"     - {d}")
    
    # 6. Generar lista final para eliminación
    print(f"\n6. Generando lista de eliminación...")
    lista_eliminacion = sorted(candidatos_eliminar)
    
    print(f"   Total de dominios a eliminar: {len(lista_eliminacion)}")
    print(f"   Dominios restantes tras eliminación: {total_propuesto}")
    
    return lista_eliminacion, total_propuesto


if __name__ == "__main__":
    lista_eliminar, total_final = analyze_whitelist()
    
    print(f"\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Dominios a eliminar: {len(lista_eliminar)}")
    print(f"Total final propuesto: {total_final}")
    print(f"Rango objetivo: 240-250")
    
    if 240 <= total_final <= 250:
        print("✓ Propuesta cumple rango objetivo")
    else:
        print("⚠️  Propuesta NO cumple rango objetivo")

