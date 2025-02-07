from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Direccion(models.Model):
    nombre = models.CharField(max_length=90)

    def __str__(self):
        return self.nombre
    

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', verbose_name='Usuario')
    departamento = models.ForeignKey(Direccion, on_delete=models.CASCADE)

    class Meta:
        verbose_name='perfil'
        verbose_name_plural='perfiles'
        ordering=['-id']

    def _str_(self):
        return self.user.username  
    

class Evento(models.Model):
    actividad       = models.CharField(max_length=255)
    descripcion     = models.CharField(max_length=255)
    fecha_inicio    = models.DateField()
    fecha_fin       = models.DateField()
    usuario         = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.actividad 