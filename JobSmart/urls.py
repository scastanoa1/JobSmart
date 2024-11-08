"""
URL configuration for JobSmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from resumes import views as resumesViews 
from vacantes import views as vacantesViews 

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls,name='Admin'),
    path('vacantes/', vacantesViews.busquedaVacantes,name='vacantes'),
    path('aplicar/<int:vacante_id>/', vacantesViews.aplicar_vacante, name='aplicar_vacante'),
    path('',resumesViews.showHomepage, name='home'),
    path('resume/',resumesViews.uploadResume, name='resumes'),
    path('iniciar_proceso/<int:resume_id>/<int:vacante_id>/', resumesViews.obtenerPreguntas, name='iniciar_proceso'),
    path('resultado/<int:resume_id>/<int:vacante_id>/', resumesViews.generarRecomendacionesFinales, name='generar_recomendaciones'),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)