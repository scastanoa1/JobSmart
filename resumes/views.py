from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from vacantes.models import Vacante
from datetime import datetime
import pdfplumber
import openai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='api_key.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

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

        # Redirigir a la vista de preguntas con los IDs correspondientes
        return redirect('iniciar_proceso', resume_id=resume.id, vacante_id=vacante_id)

    # Obtener todas las vacantes para el formulario
    vacantes = Vacante.objects.filter(fecha_cierre__gte=datetime.now())
    return render(request, 'resume.html', {'vacantes': vacantes})  # Cambia 'resultado_preguntas.html' a 'resume.html'

def calcular_nivel_mejora(recomendaciones_aplicadas, total_recomendaciones):
    if total_recomendaciones == 0:
        return 0
    return (recomendaciones_aplicadas / total_recomendaciones) * 100

def calcularRelevancia(contenido_cv, vacante): #mostrar el %
    """Función que utiliza la API de OpenAI para calcular la relevancia del CV con respecto a la vacante"""
    prompt = f"""
    Dada la descripción de una vacante y el contenido de un CV, evalúa qué tan relevante es el CV para la vacante 
    en una escala del 0% al 100%. Devuelve solo el porcentaje de relevancia basado en la alineación entre el CV y los requisitos de la vacante.

    Descripción de la vacante:
    {vacante.descripcion}

    Contenido de la hoja de vida:
    {contenido_cv}

    Relevancia:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10  # Un número pequeño de tokens para solo obtener el porcentaje
        )
        relevancia = response['choices'][0]['message']['content']
        return relevancia.strip()
    except Exception as e:
        print(f"Error al calcular relevancia: {e}")
        return "No se pudo calcular la relevancia en este momento."

def calcularMejora(contenido_cv, recomendaciones):
    """Calcula el porcentaje de mejora en base a las recomendaciones dadas."""
    prompt = f"""
    Basado en el contenido inicial de un CV y las recomendaciones para mejorar, evalúa en qué porcentaje 
    el CV mejoraría si se aplicaran las recomendaciones dadas. Devuelve solo el porcentaje de mejora.

    Contenido original del CV:
    {contenido_cv}

    Recomendaciones para mejorar el CV:
    {recomendaciones}

    Porcentaje de mejora:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10
        )
        mejora = response['choices'][0]['message']['content']
        return mejora.strip()
    except Exception as e:
        print(f"Error al calcular mejora: {e}")
        return "No se pudo calcular la mejora en este momento."

def obtenerPreguntas(request, resume_id, vacante_id):
    resume = get_object_or_404(Resume, id=resume_id)
    vacante = get_object_or_404(Vacante, id=vacante_id)

    # Fusionar lógica de obtener preguntas en esta función
    prompt_preguntas = f"""
    La siguiente vacante y hoja de vida están siendo evaluadas. 
    Formula tres preguntas que ayuden a entender mejor la experiencia del candidato para mejorar la adecuación del CV a la vacante.

    Descripción de la vacante:
    {vacante.descripcion}

    Contenido de la hoja de vida:
    {resume.contenido}

    Preguntas:
    """
    response_preguntas = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_preguntas}]
    )
    preguntas = [p.strip() for p in response_preguntas['choices'][0]['message']['content'].split("\n") if p.strip()]

    # Redirigir a la página donde el usuario responderá las preguntas
    return render(request, 'resultado_preguntas.html', {
        'preguntas': preguntas,
        'resume_id': resume_id,
        'vacante_id': vacante_id,
    })

def generarRecomendacionesFinales(request, resume_id, vacante_id):
    if request.method == 'POST':
        # Obtener respuestas del usuario
        respuestas = [request.POST.get(f'respuesta_{i+1}') for i in range(3)]
        resume = get_object_or_404(Resume, id=resume_id)
        vacante = get_object_or_404(Vacante, id=vacante_id)

        # Fusionar lógica de obtener recomendaciones en esta función
        prompt_recomendaciones = f"""
        Basado en la siguiente descripción de la vacante y hoja de vida, así como las respuestas proporcionadas por el candidato, 
        proporciona recomendaciones para mejorar la hoja de vida.

        Descripción de la vacante:
        {vacante.descripcion}

        Contenido de la hoja de vida:
        {resume.contenido}

        Respuestas del candidato:
        {respuestas}

        Recomendaciones:
        """
        response_recomendaciones = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_recomendaciones}]
        )
        recomendaciones = response_recomendaciones['choices'][0]['message']['content']

        recomendaciones_items = [item.strip() for item in recomendaciones.split("\n") if item.strip()]
        recomendaciones_html = "<ul>"
        
        for item in recomendaciones_items:
            recomendaciones_html += f"<li>{item}</li>"
        
        recomendaciones_html += "</ul>"

        relevancia = calcularRelevancia(resume.contenido, vacante)
        mejora = calcularMejora(resume.contenido, recomendaciones)

        # Renderizar el resultado
        return render(request, 'resultado.html', {
            'resume': resume,
            'vacante': vacante,
            'recomendaciones': recomendaciones_html,
            'relevancia': relevancia,
            'mejora': mejora
        })