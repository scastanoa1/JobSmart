from django.shortcuts import render, redirect
from .models import Resume
import pdfplumber


# Create your views here.
def showHomepage(request):
    return render(request,'home.html' )

def leer_pdf(pdf_file):
    """Función que utiliza pdfplumber para extraer el texto de un PDF"""
    texto = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
    return texto

def uploadResume(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        # Leer el contenido del PDF usando pdfplumber
        texto = leer_pdf(pdf_file)

        # Crear una nueva instancia de Resume y guardarla en la base de datos
        resume = Resume(nombre=pdf_file.name, contenido=texto)
        resume.save()

        # Redirigir a otra vista o renderizar una respuesta
        return redirect('resultado')

    return render(request,'resume.html')

def resultado(request):
    # Puedes pasar información a la plantilla si lo necesitas
    
    return render(request, 'resultado.html')
