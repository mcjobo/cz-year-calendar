from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


c = canvas.Canvas("rotate.pdf")

c.line( 2*cm, 21*cm, 2*cm, 16*cm)
c.line( 2*cm, 16*cm, 11*cm, 16*cm )

c.setFillColorRGB( 0, 0, 1 )
c.rect( 2.5*cm, 16*cm, 1.5*cm, 3*cm, fill = 1 )
c.setFillColorRGB( 0, 1, 0 )
c.rect( 4.5*cm, 16*cm, 1.5*cm, 4*cm, fill = 1 )
c.setFillColorRGB( 1, 0, 0 )
c.rect( 6.5*cm, 16*cm, 1.5*cm, 2*cm, fill = 1 )

c.setFillColorRGB( 0, 0, 0 )

i=0
for str in ["blue", "green", "red"]:
    c.saveState()
    c.translate( (i + 3.5) * cm, 15.5 * cm )
    c.rotate( 90 )
    c.drawRightString( 0, 0, str )
    c.restoreState()
    i += 2

c.showPage()
c.save()
