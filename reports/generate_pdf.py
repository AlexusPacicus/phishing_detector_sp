from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'EDA de Features v3 — Detección de URLs de Phishing', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 12)

# Página 1 - Contexto y tabla
comet1 = ("Este documento presenta un análisis detallado de las características ",
          "implementadas en el extractor v3 para detectar URLs de phishing.",
          "El análisis se centró en verificar la estabilidad, coherencia y ",
          "poder discriminativo de las características definidas.")

pdf.multi_cell(0, 10, '\n'.join(comet1))
pdf.ln(5)

features_table = [
    "domain_complexity",
    "domain_whitelist",
    "trusted_token_context",
    "host_entropy",
    "infra_risk",
    "brand_in_path",
    "brand_match_flag"
]

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Tabla FEATURES_V3:', 0, 1)

pdf.set_font('Arial', '', 12)
for feature in features_table:
    pdf.cell(0, 10, feature, 0, 1)

# Página 2 - Evidencias visuales
pdf.add_page()
images = [
    ('fig1_structural_signals.png', 'Separación por clase en señales estructurales.'),
    ('fig2_ttc_whitelist.png', 'Relación contractual entre whitelist y TTC.'),
    ('fig3_features_correlation.png', 'Correlaciones internas entre FEATURES_V3.')
]

img_dir = '/Users/test/Desktop/phishing-detector/EDA/img_v3/'
for img_file, caption in images:
    img_path = os.path.join(img_dir, img_file)
    if os.path.exists(img_path):
        pdf.image(img_path, w=190)
        pdf.ln(1)
        pdf.set_font('Arial', 'I', 10)
        pdf.multi_cell(0, 10, caption)
        pdf.ln(5)

# Página 3 - Estado y Siguiente paso
pdf.add_page()
pdf.set_font('Arial', '', 12)
status_text = ("EDA v3 cerrado. Invariantes validadas. Señales sin redundancia.",
              "Siguiente paso: entrenamiento baseline con split anti-leakage ",
              "(sin métricas).")

pdf.multi_cell(0, 10, '\n'.join(status_text))

# Save the PDF to the desired path
output_path = '/Users/test/Desktop/phishing-detector/reports/EDA_features_v3.pdf'
pdf.output(output_path)
print(f"PDF generado: {output_path}")



