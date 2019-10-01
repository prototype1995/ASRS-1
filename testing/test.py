from fpdf import FPDF

pdf = FPDF()


def fun():
    pdf.add_page()
    pdf.image('logo.png', 10, 8, 17)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(130)
    pdf.cell(0, 5, "BAS3D", ln=1)
    pdf.cell(130)
    pdf.cell(0, 5, "Thirunnakara, Kottayam", ln=1)
    pdf.cell(130)
    pdf.cell(0, 5, "Kerala, INDIA", ln=1)
    pdf.cell(130)
    pdf.cell(0, 5, "686001", ln=1)
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(200,10, txt="ASRS REPORT", ln=1, align="C")
    pdf.cell(500, 5, txt="------------------------------------------------------------------------------------------------------", ln=1)
    pdf.output('test.pdf')

fun()
