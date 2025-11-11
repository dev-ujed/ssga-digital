from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import FileResponse


# Vista para Perfil
class UserRecordsView(ListView):
    template_name = 'perfil_egresado.html'
    context_object_name = 'records'
    
    def get_queryset(self):
        registros_modelo1 = Inscripcion.objects.all()

        return list(chain(registros_modelo1))

# ;;;;;;;;;;;;;;;;;;; Periodos ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

# Lista Periodos View
class PeriodosListView(ListView):
    model = Periodo
    template_name = 'lista_periodos.html'
    context_object_name = 'periodos'


# class EliminarPeriodoView(DeleteView):
#     model = Periodo
#     template_name = 'periodo_confirm_delete.html'
#     success_url = reverse_lazy('periodos')  



# @login_required
class PeriodoCreateView(CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'crear_periodo.html'
    success_url = reverse_lazy('periodos')  # Redirigir después de la creación


class PeriodoUpdateView(UpdateView):
    model = Periodo
    template_name = 'editar_periodo.html'
    form_class = PeriodoForm
    success_url = reverse_lazy('periodos')


class EliminarPeriodo(DeleteView):
    model = Periodo
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('periodos')


# ;;;;;;;;;;;;;;;;;;; Inscripciones ;;;;;;;;;;;;;;;;;;;;;;;;;;    

@login_required
def detail(request, pk):
    curso = get_object_or_404(Curso, pk=pk)

    # 🔒 Verificar si el perfil está completo
    try:
        profile = request.user.profile
        campos_obligatorios = [profile.nombre, profile.apellido, profile.matricula]
        if not all(campos_obligatorios):
            messages.warning(request, "Por favor, completa tu perfil antes de inscribirte en un curso.")
            return redirect('editar_perfil')  # 👉 redirige a la vista donde el usuario llena su perfil
    except Profile.DoesNotExist:
        messages.warning(request, "Debes crear tu perfil antes de inscribirte.")
        return redirect('perfil')

    # Procesamiento normal del formulario
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    curso_bloqueado = Curso.objects.select_for_update().get(pk=curso.pk)

                    # Verificar inscripción existente
                    if Inscripcion.objects.filter(usuario=request.user, curso=curso_bloqueado).exists():
                        messages.warning(request, "Ya estás inscrito en este curso.")
                        return redirect('curso_detail', pk=pk)
                    
                    # Verificar cupos disponibles
                    if curso_bloqueado.cupos_disponibles() <= 0:
                        messages.error(request, "El curso no tiene cupos disponibles.")
                        return redirect('curso_detail', pk=pk)
                    
                    # Crear la inscripción
                    inscripcion = form.save(commit=False)
                    inscripcion.curso = curso_bloqueado
                    inscripcion.usuario = request.user
                    inscripcion.save()
                    
                    messages.success(request, "¡Inscripción exitosa!")
                    return redirect('curso_detail', pk=pk)
                    
            except Exception as e:
                messages.error(request, f"Error en la inscripción: {str(e)}")
                return redirect('curso_detail', pk=pk)
    else:
        form = InscripcionForm()
    
    return render(request, 'curso_detail.html', {
        'curso': curso,
        'form': form,
        'cupos_disponibles': curso.cupos_disponibles()
    })
    


# Vista para eliminar un inscripcion
class InscripcionDeleteView(DeleteView):
    model = Inscripcion
    template_name = 'inscripcion_confirm_delete.html'
    success_url = reverse_lazy('inscripciones')    
  

# ;;;;;;;;;;;;;;;;;;;; Comprobantes ;;;;;;;;;;;;;;;;;;;;;;;;;;;


# class ComprobantesListView(ListView):
#     model = ComprobantePago
#     template_name = 'lista_comprobantes.html'  # Opcional: Django usa <modelo>_list.html por defecto
#     context_object_name = 'comprobantes'    # Cambia el nombre del contexto por defecto


# class ComprobanteCreateView(CreateView):
#     model = ComprobantePago
#     form_class = ComprobanteForm
#     template_name = 'comprobante.html'
#     success_url = reverse_lazy('comprobantes')  # Redirigir después de la creación 


# # Vista para eliminar un comprobante
# class ComprobanteDeleteView(DeleteView):
#     model = ComprobantePago
#     template_name = 'comprobante_confirm_delete.html'
#     success_url = reverse_lazy('comprobantes')
 

#;;;;;;;;;;;;;; CURSOS  ;;;;;;;;;;;;;;;;

# @usuarios
class CursosListView(ListView):
    model = Curso
    template_name = 'cursos.html'  
    context_object_name = 'cursos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Solo mostrar el alert si el usuario no lo desactivó
        mostrar_alerta = not self.request.session.get('alerta_deshabilitada', False)
        context['mostrar_alerta'] = mostrar_alerta

        return context   
    

def desactivar_alerta(request):
    request.session['alerta_deshabilitada'] = True
    request.session.modified = True
    return JsonResponse({'status': 'ok'})


# @admin
class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'crear_curso.html'
    success_url = reverse_lazy('cursos_admin') 


class CursosAdListView(ListView):
    model = Curso
    template_name = 'cursos_admin.html'
    context_object_name = 'cursos'


class UsuariosCursoListView(ListView):
    template_name = 'usuarios_por_curso.html'
    context_object_name = 'inscripciones'
    
    def get_queryset(self):
        curso_id = self.kwargs['curso_id']
        return get_object_or_404(Curso, id=curso_id).inscripciones.all().select_related('usuario')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = get_object_or_404(Curso, id=self.kwargs['curso_id'])
        
        # Agregamos los datos calculados al contexto
        context['curso'] = curso
        context['inscritos_count'] = curso.inscritos_count()
        context['cupos_disponibles'] = curso.cupos_disponibles()
        
        return context
    

class EliminarInscripcionView(View):
    def post(self, request, *args, **kwargs):
        inscripcion_id = kwargs.get('inscripcion_id')
        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
        inscripcion.delete()
        return JsonResponse({'success': True})     
       

class CursoUpdateView(UpdateView):
    model = Curso
    template_name = 'editar_curso.html'
    form_class = CursoForm
    success_url = reverse_lazy('cursos_admin') 


class EliminarCursoView(DeleteView):
    model = Curso
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('cursos_admin')


#;;;;;;;;;;;;; MAESTROS ;;;;;;;;;;;;;;;;;;;;;;;;

# @admin    
class MaestroCreateView(CreateView):
    model = Maestro
    form_class = MaestroForm
    template_name = "add_maestro.html"
    success_url = reverse_lazy('maestros')


class MaestroListView(ListView):
    model = Maestro
    template_name = "list_maestros.html"
    context_object_name = 'maestros'


class MaestroUpdateView(UpdateView):
    model = Maestro
    template_name = 'editar_maestro.html'
    form_class = MaestroForm
    success_url = reverse_lazy('maestros') 

class EliminarMaestroView(DeleteView):
    model = Maestro
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('maestros')  

#;;;;;;;;;;;;;;;; METODOS ;;;;;;;;;;;;;;;;;;;;;;;;

def obtener_cv(request, pdf_id):
    pdf = get_object_or_404(Maestro, pk = pdf_id)
    response = FileResponse(pdf.cv, content_type='application/pdf')
    return response


def obtener_flayer(request, pdf_id):
    pdf = get_object_or_404(Curso, pk = pdf_id)
    response = FileResponse(pdf.flayer, content_type='application/pdf')
    return response


class MapaSitioView(View):
    template_name = 'mapa.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# Editar perfil
class EditarPerfil(UpdateView):
    model = Profile
    template_name = 'editar_usuario.html'
    form_class = ProfileForm
    success_url = reverse_lazy('perfil')  # Redirigir después de iniciar sesión

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile



