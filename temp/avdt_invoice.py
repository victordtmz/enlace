from fpdf import FPDF
from globalElements import constants

class PDF(FPDF):
    def configureElements(self):
        self.add_font('orbitron','',f'{constants.dbOth}/fonts/orbitron/Orbitron-Regular.ttf')
    
    def header(self):
        logo = f'{constants.rootDb}/oth/icons/enlace.png'
        self.image(logo, 5, 5, 10)
        self.set_font('orbitron', size=14)
        self.set_xy(16,7)
        self.set_text_color(3,169,244)
        self.cell(txt='AVD TRUCKING')
        self.set_text_color(255,165,0)
        self.cell(txt='LLC')
        self.set_text_color(153,159,168)
        self.set_font('helvetica', size=10)
        self.set_xy(16,13)
        self.cell(txt='Kennewick, WA - MC1130230')
        self.line(5,17,80,17)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('orbitron','',10)
        self.cell(0,10, f'{self.page_no()}/{{nb}}')
        

# todo: create FPDF object
#LAYOUT(P>portrait, L> landscape)
#units(mm, cm, in)
#format (A3, A4 (DEFAULT), A5, Letter, legal (w,h) )
pdf = PDF('P', 'mm', 'Letter')
pdf.configureElements()
#add page
pdf.add_page()
# pdf.set_font('helvetica','',16)
logo = f'{constants.rootDb}/oth/icons/enlace.png'
pdf.image(logo, 5, 5, 10)
pdf.set_font('orbitron', size=14)
pdf.set_xy(16,7)
pdf.set_text_color(3,169,244)
pdf.cell(txt='AVD TRUCKING')
pdf.set_text_color(255,165,0)
pdf.cell(txt='LLC')
pdf.set_text_color(153,159,168)
pdf.set_font('helvetica', size=10)
pdf.set_xy(16,13)
pdf.cell(txt='Kennewick, WA - MC1130230')
pdf.line(5,17,80,17)


pdf.set_auto_page_break(True, margin=15)
#add text
# w, h
# pdf.cell(txt=f'''AVD TRUCKING LLC -
# This is a test to run multiple lines and forrmated strings are not being passed as such, we have to write line by line
# so ..... lets struggle with it''',ln=True,  border=True)

# for i in range(1,41):
#     pdf.cell(0, 10, f'This is line {i} ', ln=True)


pdf.output('pdf_1.pdf')