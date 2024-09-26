from django.shortcuts import render
from .models import Vacante
from datetime import datetime

# Mostrar todas las vacantes
def mostrarVacantes(request):
    fechahoy = datetime.now()
    vacantes = Vacante.objects.all().filter(fecha_cierre__gte=fechahoy)
    return render(request,'vacantes.html',{"vacantes":vacantes})
# Create your views here.
def busquedaVacantes(request):
    searchTerm = request.GET.get('buscarVacante')
    fechahoy = datetime.now()
    vacantes = Vacante.objects.all().filter(fecha_cierre__gte=fechahoy)
    if searchTerm:
        vacantes = vacantes.filter(titulo__icontains=searchTerm)
    return render(request,'vacantes.html',{"vacantes":vacantes})
    