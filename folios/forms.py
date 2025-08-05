from django import forms
from .models import ArchivoExcel, Producto
from django.core.exceptions import ValidationError
import pandas as pd


class SubirExcelForm(forms.ModelForm):
    class Meta:
        model = ArchivoExcel
        fields = ['archivo']  # Asegúrate que coincide con tu modelo

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        
        # Validar extensión
        if not archivo.name.lower().endswith(('.xls', '.xlsx')):
            raise ValidationError("Solo se permiten archivos Excel (.xls, .xlsx).")
        
        # Validar estructura del Excel
        try:
            df = pd.read_excel(archivo)
            required_columns = ['folio', 'nombre']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValidationError(f"Faltan columnas: {', '.join(missing_columns)}")
        except Exception as e:
            raise ValidationError(f"Error al leer el archivo: {str(e)}")
        
        return archivo


class BuscarFolioForm(forms.Form):
    folio = forms.CharField(
        label='Ingrese el folio a buscar',
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: UJED2025'})
    )

    # def clean_folio(self):
    #     folio = self.cleaned_data['folio']
    #     if not folio.isdigit():
    #         raise forms.ValidationError("El folio debe ser numérico")
    #     return folio
    

class AddProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        exclude = ('archivo',)
        widgets = {
            'folio': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'true'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'figura': forms.TextInput(attrs={'class': 'form-control'}),
            'actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo': forms.TextInput(attrs={'class': 'form-control'}),
            'autoridad_uno': forms.TextInput(attrs={'class': 'form-control'}),
            'autoridad_dos': forms.TextInput(attrs={'class': 'form-control'}),
        }
