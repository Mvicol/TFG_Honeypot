import os
import sys
import subprocess
from datetime import datetime

# Asegura que las dependencias estén instaladas
try:
    import docx
except ImportError:
    print("[+] Instalando python-docx...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    import docx

from docx import Document

# → Pedir al usuario el nombre del archivo (sin extensión)
nombre_base = input("Introduce el nombre del informe (sin extensión): ").strip()
if not nombre_base:
    print("[!] El nombre del informe no puede estar vacío.")
    sys.exit(1)

# Obtener escritorio del usuario real (incluso si se ejecuta como root)
home_real = os.path.expanduser("~" + os.getenv("SUDO_USER") if os.getenv("SUDO_USER") else "~")
desktop = os.path.join(home_real, "Desktop")
if not os.path.isdir(desktop):
    desktop = os.path.join(home_real, "Escritorio")  # fallback por si está en español

# Crear carpeta de salida
output_dir = os.path.join(desktop, "HoneyPot_Informes")
os.makedirs(output_dir, exist_ok=True)

# Crear el documento
doc = Document()
doc.add_heading('Informe de Prueba', 0)
doc.add_paragraph('Este es un informe generado automáticamente con python-docx en Linux.')

doc.add_heading('Resumen de Datos Simulados', level=1)
table = doc.add_table(rows=1, cols=3)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'ID'
hdr_cells[1].text = 'Nombre'
hdr_cells[2].text = 'Resultado'

datos = [
    (1, 'Escaneo Web', 'OK'),
    (2, 'Detección de WAF', 'WAF encontrado'),
    (3, 'Scraper Dark Web', 'Sin actividad maliciosa')
]

for fila in datos:
    row_cells = table.add_row().cells
    for i, valor in enumerate(fila):
        row_cells[i].text = str(valor)

doc.add_paragraph("\nFecha de generación: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

# Guardar .docx
docx_path = os.path.join(output_dir, f"{nombre_base}.docx")
doc.save(docx_path)
print(f"[✓] Informe DOCX creado: {docx_path}")

# Convertir a PDF con libreoffice
print("[+] Convirtiendo a PDF...")
try:
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, docx_path], check=True)
    print(f"[✓] Informe PDF creado: {os.path.join(output_dir, f'{nombre_base}.pdf')}")
except FileNotFoundError:
    print("[!] LibreOffice no está instalado. Ejecuta: sudo apt install libreoffice")
