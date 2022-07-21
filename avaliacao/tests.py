from cStringIO import StringIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # Crie o objeto HttpResponse com o cabeçalho PDF apropriado.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    buffer = StringIO()

    # Crie um objeto PDF, usando o objeto StringIO como seu "arquivo."
    p = canvas.Canvas(buffer)

    # Desenhe coisas no PDF. Aqui é onde a geração do PDF acontece.
    # Veja a documentação do ReportLab para a lista completa de
    # funcionalidades.
    p.drawString(100, 100, "Hello world.")

    # Feche o objeto PDF.
    p.showPage()
    p.save()

    # Pegue o valor do buffer StringIO e escreva-o para o response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response