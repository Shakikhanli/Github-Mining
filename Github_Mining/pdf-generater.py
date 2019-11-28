from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter, landscape

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

c = canvas.Canvas("file3.pdf")

# c.drawString(0, 820, "HEllo Bitch :)")

# slices_files = [123, 345]
# activities = ["a1", "a2"]
# colors = ['r', 'g']
# img = plt.pie(slices_files, labels=activities, colors=colors, startangle=90, autopct='%.1f%%')
#
#
#
# c.drawString(220, 810, "Report document for project")
#
# c.drawString(5, 750, "Name of the Github user:")
# c.drawString(150, 750, "Ulvi Shakikhanli")
# c.drawString(5, 735, "Name of the project:")
# c.drawString(150, 735, "Github_Mining")
#
# c.drawString(5, 705, "This is a MEAN stack project. Used technologies are Mongo DB, ExpressJs, Angular and NodeJs")
#
# c.drawString(5, 690, "Total Number of commits:")
# c.drawString(150, 690, "134")
# c.drawString(5, 675, "Total number of front end:")
# c.drawString(150, 675, "94")
# c.drawString(5, 660, "Total number of front end:")
# c.drawString(150, 660, "40")
#
#
#
# c.showPage()


doc = SimpleDocTemplate("form_letter.pdf",
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

Story = []
logo = "image.png"

# We really want to scale the image to fit in a box and keep proportions.
im = Image(logo, 3 * inch, 3 * inch)
Story.append(im)

ptext = '''
<seq>. </seq>Some Text<br/>
<seq>. </seq>Some more test Text
'''
Story.append(Paragraph(ptext, styles["Bullet"]))

ptext = '<bullet>&bull;</bullet>Some Text'
Story.append(Paragraph(ptext, styles["Bullet"]))

doc.build(Story)
