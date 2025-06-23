from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Inscripcion



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricula', 'nombre', 'apellido')  # Muestra estos campos en la lista
    list_filter = ('apellido',)  # Filtro por sexo
    search_fields = ('user__username', 'matricula', 'nombre', 'apellido')  # Búsqueda por usuario, matrícula y curp
    ordering = ('user',)  # Ordena por usuario
    readonly_fields = ('user',)  # Evita que el usuario se edite desde el admin
    fieldsets = (
        ('Información del Usuario', {'fields': ('user', 'matricula', 'nombre', 'apellido')}),
    )

# Register your models here.    
# admin.site.register(Profile)
admin.site.register(Periodo)


# admin.py
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cupo', 'inscritos_count', 'cupos_disponibles')
    filter_horizontal = ('maestros',)  # Interfaz amigable para seleccionar maestros
    
    def inscritos_count(self, obj):
        return obj.inscritos_count()
    
    def cupos_disponibles(self, obj):
        return obj.cupos_disponibles()

admin.site.register(Curso, CursoAdmin)


@admin.register(Maestro)
class MaestroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'cv_link')  # Muestra estos campos en la lista
    search_fields = ('nombre', 'especialidad')  # Permite buscar por nombre y especialidad
    list_filter = ('especialidad',)  # Agrega filtro por especialidad
    ordering = ('nombre',)  # Ordena por nombre alfabéticamente
    fieldsets = (
        ('Información Personal', {'fields': ('nombre', 'especialidad')}),
        ('Documentos', {'fields': ('cv',)}),
    )

    def cv_link(self, obj):
        """Muestra un enlace para descargar el archivo CV si está disponible."""
        if obj.cv:
            return format_html('<a href="{}" target="_blank">Ver CV</a>', obj.cv.url)
        return "No disponible"
    
    cv_link.short_description = "Currículum"


#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'fecha_inscripcion', 'estado_curso')  # Muestra estado del curso
    list_filter = ('curso', 'fecha_inscripcion')  # Filtra por curso y fecha
    search_fields = ('usuario__username', 'curso__nombre')  # Búsqueda por usuario y curso
    ordering = ('-fecha_inscripcion',)  # Ordena por inscripciones recientes primero
    
    def estado_curso(self, obj):
        """Muestra si el curso está activo o inactivo."""
        return "Activo" if obj.curso.status else "Inactivo"
    
    estado_curso.short_description = "Estado del Curso"

    def save_model(self, request, obj, form, change):
        """Validaciones antes de guardar la inscripción."""
        with transaction.atomic():
            if not obj.curso.status:
                raise ValidationError("No se puede inscribir a un curso inactivo")
            
            if Inscripcion.objects.filter(usuario=obj.usuario, curso=obj.curso).exists():
                raise ValidationError("Este usuario ya está inscrito en el curso.")
            
            super().save_model(request, obj, form, change)