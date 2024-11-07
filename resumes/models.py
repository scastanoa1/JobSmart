from django.db import models
from accounts.models import User
# Create your models here.
class Resume(models.Model):
    nombre = models.CharField(max_length=255)
    contenido = models.TextField()
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, default='admin.id')

    def __str__(self):
        return self.nombre