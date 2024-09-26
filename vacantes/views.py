from django.shortcuts import render

# Mostrar todas las vacantes
def vacantes(request):
    return render(request,'vacantes.html')
# Create your views here.
