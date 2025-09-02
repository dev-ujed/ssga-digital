from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd

class ArchivoExcel(models.Model):
    archivo = models.FileField(upload_to="excels/")  # Guarda el archivo en MEDIA_ROOT/excels/
    fecha_subida = models.DateTimeField(auto_now_add=True)
    nombre_original = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre_original} - {self.fecha_subida}"

class Producto(models.Model):
    folio = models.CharField(max_length=20, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    figura = models.CharField(max_length=90, null=True, blank=True)
    actividad = models.CharField(max_length=255, null=True, blank=True)
    periodo = models.CharField(max_length=255, null=True, blank=True)
    autoridad_uno = models.CharField(max_length=255, null=True, blank=True)
    autoridad_dos = models.CharField(max_length=255, null=True, blank=True)
    autoridad_tres = models.CharField(max_length=255, null=True, blank=True)
    archivo = models.ForeignKey(  # Opcional: Relacionar productos con el archivo
        ArchivoExcel, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre
    

# models.py (añadir esto al final)
@receiver(post_save, sender=ArchivoExcel)
def procesar_excel(sender, instance, created, **kwargs):
    if created and instance.archivo:
        try:
            # Leer el archivo Excel
            df = pd.read_excel(instance.archivo.path)
            
            # Validar estructura del Excel
            required_columns = ['folio', 'nombre', 'figura', 'actividad', 'periodo', 'autoridad_uno', 'autoridad_dos', 'autoridad_tres']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("El archivo no tiene las columnas requeridas")
            
            # Procesar cada fila
            productos = []
            for _, row in df.iterrows():
                productos.append(Producto(
                    folio=row['folio'],
                    nombre=row['nombre'],
                    figura=row['figura'],                    
                    actividad=row['actividad'],
                    periodo=row['periodo'],
                    autoridad_uno=row['autoridad_uno'],
                    autoridad_dos=row['autoridad_dos'],
                    autoridad_tres=row['autoridad_tres'],
                    archivo=instance
                ))
            
            # Bulk create para mejor performance
            Producto.objects.bulk_create(productos)
            
        except Exception as e:
            # Manejar errores apropiadamente
            instance.delete()  # Eliminar archivo si hay error
            print(f"Error procesando archivo: {str(e)}")


