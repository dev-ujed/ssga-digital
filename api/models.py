from django.db import models
from django.contrib.auth.models import User
from datetime import date


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
    
    def progreso(self):
        total_dias = (self.fecha_fin - self.fecha_inicio).days
        # print(total_dias)
        if total_dias <= 0:  # Manejo de errores para fechas inválidas
            return 0
        dias_transcurridos = (min(self.fecha_fin, date.today()) - self.fecha_inicio).days
        return max(0, min((dias_transcurridos / total_dias) * 100, 100))
    
    @property
    def dias_restantes(self):
        hoy = date.today()
        return max((self.fecha_fin - hoy).days, 0)