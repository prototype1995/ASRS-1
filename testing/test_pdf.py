from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

import fpdf #pip3 install fpdf
 
pdf = fpdf.FPDF() #pdf format
c = canvas.Canvas('overlay.pdf')


pdf.add_page() #create new page
pdf.set_font("Arial", 'B', size=16) # font and textsize


pdf.cell(200, 10, txt="Heading", ln=1, align="L")


c.drawImage('test.jpg', 22, 770, 50, 50) # (x1, y1) : coordinates - (x2, y2) : image size
c.drawImage('test.jpg', 102, 770, 50, 50) # (x1, y1) : coordinates - (x2, y2) : image size

c.save()

watermark = PdfFileReader(open("overlay.pdf", "rb"))

# Get our files ready
output_file = PdfFileWriter()
input_file = PdfFileReader(open("test.pdf", "rb"))

input_page = input_file.getPage(0)
input_page.mergePage(watermark.getPage(0))
# add page from input file to output document
output_file.addPage(input_page)


pdf.set_font("Arial", size=10) # font and textsize

pdf.cell(100, 8, txt="your text", ln=1, align="L")
pdf.cell(100, 8, txt="your text", ln=2, align="L")
pdf.cell(100, 8, txt="your text", ln=3, align="L")

pdf.output("test.pdf")

# finally, write "output" to document-output.pdf
with open("doc.pdf", "wb") as outputStream:
    output_file.write(outputStream)

