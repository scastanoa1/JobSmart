from django.core.management.base import BaseCommand
from vacantes.models import Vacante
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        # Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        # El path del archivo vacante_descriptions con respecto a DjangoProjectBase sería la carpeta anterior
        json_file_path = 'vacantes\\management\\commands\\vacantes.json'

        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            vacantes = json.load(file)

        # Add products to the database
        for i in range(len(vacantes)):
            vacante = vacantes[i]
            Vacante.objects.create(titulo = vacante['titulo'],
                                     descripcion = vacante['descripcion'],
                                     area = vacante['area'],
                                     ubicacion = vacante['ubicacion'],
                                     fecha_publicacion = vacante['fecha_publicacion'],
                                     fecha_cierre = vacante['fecha_cierre'],
                                     estado = vacante['estado'],
                                     jornada = vacante['jornada'],
                                     salario = vacante['salario'],
                                     )

        # self.stdout.write(self.style.SUCCESS('Successfully added (cont) products to the database'))
