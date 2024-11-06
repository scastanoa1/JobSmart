from django.db import models

# Create your models here.
class Resume(models.Model):
    nombre = models.CharField(max_length=255)
    contenido = models.TextField()

    def __str__(self):
        return self.nombre