from django.db import models
from django.contrib.auth.models import User
from datetime import date
import json
from datetime import date, datetime 



# Create your models here.
class Direccion(models.Model):
    nombre = models.CharField(max_length=90)

    def __str__(self):
        return self.nombre
    

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', verbose_name='Usuario')
    departamento = models.ForeignKey(Direccion, on_delete=models.CASCADE, verbose_name='departamento')

    class Meta:
        verbose_name='perfil'
        verbose_name_plural='perfiles'
        ordering=['-id']

    def __str__(self):
        return self.user.username  
    

class Evento(models.Model):
    actividad       = models.CharField(max_length=255)
    descripcion     = models.CharField(max_length=255)
    fecha_inicio    = models.DateField()
    fecha_fin       = models.DateField()
    usuario         = models.ForeignKey(User, on_delete=models.CASCADE)
    actualizado_en  = models.DateTimeField(auto_now=True)
    cambios         = models.JSONField(default=dict, blank=True)
    

    def __str__(self):
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
    

    # --Registro de modificacion
    def save(self, *args, **kwargs):
        if self.pk:
            original = Evento.objects.get(pk=self.pk)
            cambios_detectados = {}

            for field in self._meta.fields:
                field_name = field.name
                if field_name not in ["actualizado_en", "cambios"]:
                    old_value = getattr(original, field_name)
                    new_value = getattr(self, field_name)

                    # ✅ Convertir fechas a string antes de guardarlas en JSON
                    if isinstance(old_value, (date, datetime)):  
                        old_value = old_value.strftime('%Y-%m-%d') if old_value else None
                    if isinstance(new_value, (date, datetime)):  
                        new_value = new_value.strftime('%Y-%m-%d') if new_value else None

                    if old_value != new_value:
                        cambios_detectados[field_name] = {"antes": old_value, "despues": new_value}

            if cambios_detectados:
                self.cambios = cambios_detectados  

        super().save(*args, **kwargs)