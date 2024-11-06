from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from vacantes.models import Vacante
from datetime import datetime
import pdfplumber
import openai
import os
from dotenv import load_dotenv

from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from vacantes.models import Vacante
from datetime import datetime
import pdfplumber
import openai
import os
from dotenv import load_dotenv


# Create your views here.
def showHomepage(request):
    return render(request,'home.html' )

def leerPdf(pdf_file):
    """Función que utiliza pdfplumber para extraer el texto de un PDF"""
    texto = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
    return texto

def uploadResume(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        texto = leerPdf(pdf_file)

        # Guardar el resumen
        resume = Resume(nombre=pdf_file.name, contenido=texto)
        resume.save()

        # Obtener el vacante_id del formulario
        vacante_id = request.POST.get('vacante_id')

        # Redirigir a la vista resultado con los IDs correspondientes
        return redirect('resultado', resume_id=resume.id, vacante_id=vacante_id)

    # Obtener todas las vacantes para el formulario
    vacantes = Vacante.objects.filter(fecha_cierre__gte=datetime.now())
    return render(request, 'resume.html', {'vacantes': vacantes})


# Cargar las variables de entorno desde api_key.env
"""_ = load_dotenv('../api_keys.env')

# Obtener la clave de API desde el archivo .env
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    print("Error: la clave de la API de OpenAI no se ha cargado correctamente.")
else:
    print(f"Clave API cargada: {openai.api_key}")"""

openai.api_key = ''

def obtenerRecomendaciones(contenido_cv, vacante):
    """Función que utiliza la API de OpenAI para obtener recomendaciones para el CV"""
    prompt = f"""
    Dada la siguiente descripción de una vacante y el contenido de una hoja de vida, 
    proporciona recomendaciones sobre cómo mejorar la hoja de vida para que se ajuste mejor a la vacante.

    Descripción de la vacante:
    {vacante.descripcion}  # Asumiendo que 'descripcion' es un campo en el modelo Vacante

    Contenido de la hoja de vida:
    {contenido_cv}

    Recomendaciones:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Puedes elegir el modelo que prefieras
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500  # Ajusta el número de tokens según sea necesario
        )
        recomendaciones = response['choices'][0]['message']['content']
        return recomendaciones.strip()
    except Exception as e:
        print(f"Error al obtener recomendaciones: {e}")
        return "No se pudieron generar recomendaciones en este momento."



def resultado(request, resume_id, vacante_id):
    resume = get_object_or_404(Resume, id=resume_id)
    vacante = get_object_or_404(Vacante, id=vacante_id)

    # Obtener recomendaciones basadas en la hoja de vida y la vacante
    recomendaciones = obtenerRecomendaciones(resume.contenido, vacante)

    return render(request, 'resultado.html', {'resume': resume, 'vacante': vacante, 'recomendaciones': recomendaciones})