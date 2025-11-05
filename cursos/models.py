from datetime import date
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    matricula = models.CharField(max_length=10, null=True, blank=True)
    nombre = models.CharField(max_length=90, null=True, blank=True)
    apellido = models.CharField(max_length=90, null=True, blank=True)

    def __str__(self):
        return f"{self.user}, {self.matricula}"


################################
class Periodo(models.Model):
    nombre = models.CharField(max_length=90)
    # fecha_inicio_inscripcion = models.DateField()   
    # fecha_fin_inscripcion = models.DateField()
    # fecha_inicio_pago = models.DateField()
    # fecha_fin_pago = models.DateField()

    def __str__(self):
        return self.nombre 

    # def ha_finalizado(self):
    #     from django.utils import timezone
    #     return timezone.now().date() > self.fecha_fin_inscripcion

    # def progreso(self):
    #     total_dias = (self.fecha_fin_inscripcion - self.fecha_inicio_inscripcion).days
    #     # print(total_dias)
    #     if total_dias <= 0:  # Manejo de errores para fechas inválidas
    #         return 0
    #     dias_transcurridos = (min(self.fecha_fin_inscripcion, date.today()) - self.fecha_inicio_inscripcion).days
    #     return max(0, min((dias_transcurridos / total_dias) * 100, 100))   
    
    # def __str__(self):
    #     return f"{self.nombre} (Inscripción: {self.fecha_inicio_inscripcion} - {self.fecha_fin_inscripcion}, Pago: {self.fecha_inicio_pago} - {self.fecha_fin_pago})"

    # def esta_activo_inscripcion(self):
    #     hoy = timezone.now().date()
    #     return self.fecha_inicio_inscripcion <= hoy <= self.fecha_fin_inscripcion

    # def esta_activo_pago(self):
    #     hoy = timezone.now().date()
    #     return self.fecha_inicio_pago <= hoy <= self.fecha_fin_pago
    
    # def delete(self, *args, **kwargs):
    #     # Validar si el período ya concluyó
    #     hoy = timezone.now().date()
    #     if hoy > self.fecha_fin_pago:
    #         raise ValidationError("No se puede eliminar un período cuyo tiempo ya concluyó.")
    #     super().delete(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.pk:  # Verifica si el objeto ya existe (es una actualización)
    #         if self.fecha_fin_pago < now().date():
    #             raise ValidationError("No se puede actualizar después de la fecha límite.")
    #     super().save(*args, **kwargs)

    # @property
    # def dias_restantes(self):
    #     hoy = date.today()
    #     return max((self.fecha_fin_inscripcion - hoy).days, 0)
    

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
class Maestro(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=255)
    cv = models.FileField(upload_to='archivos_cv/', null=True, blank=True)
    def __str__(self):
        return self.nombre    

################################
class Curso(models.Model):
    folio = models.IntegerField(null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='cursos')
    status = models.BooleanField(default=False)
    cupo = models.IntegerField(null=True)
    maestros = models.ManyToManyField(Maestro, related_name='cursos')
    flayer = models.FileField(upload_to='flayers/', null=True, blank=True)


    def inscritos_count(self):
        """Devuelve la cantidad de usuarios inscritos"""
        return self.inscripciones.count()  # "inscripciones" viene del related_name

    def cupos_disponibles(self):
        """Calcula los cupos restantes"""
        return self.cupo - self.inscritos_count()

    def __str__(self):
        return self.nombre
    
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

#################################
class Inscripcion(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Si usas el modelo de usuario de Django
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            curso = Curso.objects.select_for_update().get(pk=self.curso.pk)
            if curso.inscritos_count() >= curso.cupo:
                raise ValidationError("El curso no tiene cupos disponibles.")
            if not self.curso.status:
                raise ValidationError("No se puede inscribir a un curso inactivo")
            if Inscripcion.objects.filter(usuario=self.usuario, curso=curso).exists():
                raise ValidationError("Este usuario ya está inscrito en el curso.")
            super().save(*args, **kwargs) 

    class Meta:
        unique_together = ['usuario', 'curso']  # Evita inscripciones duplicadas
        
    def __str__(self):
        return f"{self.usuario.username} en {self.curso.nombre}"
    
################################
# class ComprobantePago(models.Model):
#     STATUS_PAGO = [
#         ('concluido', 'Concluido'),
#         ('parcial', 'Parcial'),
#         ('convenio', 'Convenio'),
#         ('prorroga', 'Prorroga'),
#         ('acreditacion', 'Acreditacion'),
#         ('pendiente', 'Pendiente'),
#     ]

#     inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='comprobantes')
#     archivo = models.FileField(upload_to='comprobantes/')
#     fecha_subida = models.DateField(auto_now_add=True)
#     pago = models.CharField(max_length=20, choices=STATUS_PAGO, default='pendiente')  # Campo para indicar si fue aprobado

#     def __str__(self):
#         return f"Comprobante de {self.inscripcion.usuario.username} para {self.inscripcion.curso.nombre}"
   