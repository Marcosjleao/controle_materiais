import os
from reportlab.pdfgen import canvas

# Criar a pasta "pdfs" se ela não existir
if not os.path.exists("pdfs"):
    os.makedirs("pdfs")

# Criar o PDF
pdf_filename = "pdfs/teste.pdf"
c = canvas.Canvas(pdf_filename)
c.drawString(100, 750, "Teste de geração de PDF")
c.save()

print(f"PDF gerado: {pdf_filename}")
