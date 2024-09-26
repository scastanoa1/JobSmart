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
        texto = leer_pdf(pdf_file)

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
load_dotenv(dotenv_path='api_key.env')

# Obtener la clave de API desde el archivo .env
openai.api_key = os.getenv('OPENAI_API_KEY')

def obtener_recomendaciones(contenido_cv, vacante):
    prompt = f"""
    Un candidato ha aplicado a la siguiente vacante:
    Título de la vacante: {vacante.titulo}
    Descripción: {vacante.descripcion}
    Area: {vacante.area}
    Ubicación: {vacante.ubicacion}

    Aquí está el contenido de su hoja de vida:
    {contenido_cv}

    Por favor, proporciona recomendaciones detalladas sobre cómo el candidato puede adaptar su hoja de vida para que se ajuste mejor a esta vacante.
    """
    
    # Llamada a la API de ChatGPT
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        recomendaciones = response.choices[0].text.strip()
        return recomendaciones
    except Exception as e:
        print(f"Error al obtener recomendaciones: {e}")
        return "No se pudieron generar recomendaciones en este momento."

def resultado(request, resume_id, vacante_id):
    resume = get_object_or_404(Resume, id=resume_id)
    vacante = get_object_or_404(Vacante, id=vacante_id)

    # Obtener recomendaciones basadas en la hoja de vida y la vacante
    recomendaciones = obtener_recomendaciones(resume.contenido, vacante)

    return render(request, 'resultado.html', {'resume': resume, 'vacante': vacante, 'recomendaciones': recomendaciones})