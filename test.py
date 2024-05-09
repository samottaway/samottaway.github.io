from reportlab.pdfgen.canvas import Canvas
from  reportlab.lib.units import cm,inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from  reportlab.lib.enums import  TA_JUSTIFY,TA_CENTER
from  reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image
from reportlab.lib.styles import  getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch

#https://docs.reportlab.com/reportlab/userguide/ch2_graphics/
# def create_recipe_pdf(recipe_file):
#
#     pdf = f'{recipe_file.recipe_name.data}.pdf'
#     canvas = Canvas(f'assets/recipes/{pdf}', pagesize=(8.5 * inch, 11 * inch))
#     canvas.save()
#     document = []
#     document.append(Image(f'static/assets/recipe_image/{}'))
#
#     canvas.drawImage(Image(f"static/assets/recipe_image/{image}"),0,0)
#     #canvas.drawString()
#     #canvas.drawText()
#     #canvas.drawText()
#
#     canvas.save()

# pdf = 'hello.pdf'
# canvas = Canvas(f'assets/recipes/{pdf}',pagesize=(8.5*inch,11 * inch))
#
# canvas.drawString(72,72,'hello world!')
#
# canvas.save()

#
# document = []
#
# document.append(Image('2640.jpg',2.2*inch,2.2*inch))
#
# def add_title(doc):
#     doc.append(Spacer(1,20))
#     doc.append(Paragraph('MEMEMEGP',ParagraphStyle(name='name',FontFamily='Helvetica',fontsize=36,aligment=TA_CENTER)))
#     doc.append(Spacer(1,50))
#     return doc
#
# def add_paragraph(doc):
#         with open('text.txt') as txt:
#             for line in txt.read().split('\n'):
#                 doc.append(Paragraph(line))
#                 doc.append(Spacer(1,20))
#         return doc
#
# document = add_title(document)
# SimpleDocTemplate('dave.pdf',pagesize=LETTER,
#                   rightmargin=12,leftmargin=12,topmargin=12,bottonmargin=6).build(add_paragraph(document))
#
#
#
