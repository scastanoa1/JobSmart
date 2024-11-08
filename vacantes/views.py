from django.shortcuts import render, redirect
from .models import Vacante
from datetime import datetime
from django.contrib import messages

def aplicar_vacante(request, vacante_id):
    messages.success(request, "¡Aplicaste a la vacante exitosamente!")
    return redirect('vacantes')

def mostrarVacantes(request):
    fechahoy = datetime.now()
    vacantes = Vacante.objects.all().filter(fecha_cierre__gte=fechahoy)
    return render(request,'vacantes.html',{"vacantes":vacantes})

def busquedaVacantes(request):
    searchTerm = request.GET.get('buscarVacante')
    fechahoy = datetime.now()
    vacantes = Vacante.objects.all().filter(fecha_cierre__gte=fechahoy)
    if searchTerm:
        vacantes = vacantes.filter(titulo__icontains=searchTerm)
    return render(request,'vacantes.html',{"vacantes":vacantes})
    