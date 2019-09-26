import fpdf #pip3 install fpdf
 
pdf = fpdf.FPDF() #pdf format

pdf.add_page() #create new page
pdf.set_font("Arial", 'B', size=16) # font and textsize


pdf.cell(200, 10, txt="Heading", ln=1, align="L")

pdf.set_font("Arial", size=10) # font and textsize

pdf.cell(100, 8, txt="your text", ln=1, align="L")

pdf.cell(100, 8, txt="your text", ln=2, align="L")

pdf.cell(100, 8, txt="your text", ln=3, align="L")

pdf.output("test.pdf")
