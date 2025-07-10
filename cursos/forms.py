from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields='__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'True'}),
            # 'fecha_inicio_inscripcion': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            # 'fecha_fin_inscripcion': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            # 'fecha_inicio_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            # 'fecha_fin_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'folio': forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'true'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cupo': forms.NumberInput(attrs={'class': 'form-control'}),
            'maestros': forms.CheckboxSelectMultiple(),
        }



class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields='__all__'
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
        }


# class ComprobanteForm(forms.ModelForm):
#     class Meta:
#         model = ComprobantePago
#         fields='__all__'
#         # exclude = ['aprobado']
#         widgets = {
#             'inscripcion': forms.Select(attrs={'class': 'form-control'}),
#             'archivo': forms.FileInput(attrs={'class': 'form-control'}),
#             'pago': forms.Select(attrs={'class': 'form-control'}),
#         }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Marcamos los campos que pueden ser null como no requeridos
    #     for field_name, field in self.fields.items():
    #         if field_name in ['aprobado']:
    #             field.required = False  


# class PeriodoUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Periodo
#         fields='__all__'


# class RegistroUsuarioForm(UserCreationForm):
#     email = forms.EmailField(required=True)  # Agregar campo de email obligatorio

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        exclude = ['id','curso', 'usuario'] 


class MaestroForm(forms.ModelForm):
    class Meta:
        model = Maestro  # Especifica el modelo asociado
        fields = '__all__'  # Usa todos los campos del modelo
        widgets = {
            'nombre':       forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'cv':           forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['matricula', 'nombre', 'apellido']
        
        # Personalización de widgets
        widgets = {
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ABC123'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Carlos'

            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pérez Gómez'
            }),

        }
        

