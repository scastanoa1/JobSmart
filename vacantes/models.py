from django.db import models
class Vacante(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    area = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    fecha_publicacion = models.DateField(auto_now_add=True)
    fecha_cierre = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('open', 'Abierta'),
        ('closed', 'Cerrada'),
        ('ongoing', 'En proceso')
    ], default='abierta')
    jornada = models.CharField(max_length=50, choices=[
        ('fullTime', 'Tiempo completo'),
        ('halfTime', 'Medio tiempo')
    ])
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titulo
# Create your models here.
