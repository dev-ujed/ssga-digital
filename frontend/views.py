from datetime import timezone
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from api.models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.
class LoginView(FormView):
    template_name = 'login.html'  # Ruta al archivo de plantilla
    form_class = BootstrapAuthenticationForm
    success_url = reverse_lazy('eventos')  # Redirigir después de iniciar sesión

    def dispatch(self, request, *args, **kwargs):
        """Cierra la sesión antes de procesar cualquier solicitud a esta vista"""
        logout(request)  # Cierra cualquier sesión activa
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Inicia sesión al validar el formulario"""
        user = form.get_user()  # Obtiene el usuario autenticado
        login(self.request, user)  # Inicia la sesión del usuario
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        """Maneja el caso en que el formulario no es válido (credenciales incorrectas)"""
        messages.error(self.request, "Usuario o contraseña incorrectos.")  # Envía un mensaje de error
        return super().form_invalid(form)  # Vuelve a mostrar el formulario con errores

    def get_success_url(self):
        """Redirigir después del login, con soporte para ?next="" en la URL"""
        return self.request.GET.get('next', self.success_url)


# Cerrar sesión
class LogoutView(View):
    def get(self, request):
        # Cierra la sesión del usuario
        logout(request)
        # Redirige a la página de inicio u otra página después de cerrar la sesión
        return redirect(reverse('login'))


def user_register(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm 
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # Añade un mensaje de éxito
                messages.success(request, 'Usuario creado correctamente.')
                # Redirige al usuario a la página de login
                return redirect('login')
            except:
                # return HttpResponse('el usuario ya existe')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error' : 'Usuario ya existe' 
                })
        # return HttpResponse('passwords no coinciden')
        return render(request, 'signup.html', {
            'form': UserCreationForm, 
            'error': 'Passwords no coinciden'
        })

class EventosCreateView(CreateView):
    model = Evento
    template_name = 'crear_evento.html'
    form_class = EventoForm
    success_url = reverse_lazy('eventos')

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # ¡Clave aquí!
        response = super().form_valid(form)
        messages.success(self.request, "¡Evento guardado correctamente!")
        return response

# Decorador para verificar perfil y login
class ProfileRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'perfil'):
            return redirect('nombre_de_tu_vista_para_crear_perfil')  # Ajusta esto
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class EventosListView(ProfileRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        direccion = self.request.user.perfil.departamento
        return Evento.objects.filter(
            usuario__perfil__departamento=direccion
        ).select_related('usuario')


@method_decorator(login_required, name='dispatch')
class EliminarEventoView(ProfileRequiredMixin, DeleteView):
    model = Evento
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('eventos')

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


@method_decorator(login_required, name='dispatch')
class EventoUpdateView(ProfileRequiredMixin, UpdateView):
    model = Evento
    template_name = 'editar_evento.html'
    form_class = EventoForm
    success_url = reverse_lazy('eventos')

    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


@method_decorator(login_required, name='dispatch')
class EventosView(ProfileRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        direccion = request.user.perfil.departamento
        eventos = Evento.objects.filter(
            usuario__perfil__departamento=direccion
        ).select_related('usuario')
        
        eventos_data = [self._evento_to_dict(e) for e in eventos]
        return JsonResponse(eventos_data, safe=False)

    def _evento_to_dict(self, evento):
        return {
            'id': evento.id,
            'title': evento.actividad,
            'start': evento.fecha_inicio.isoformat(),
            'end': evento.fecha_fin.isoformat(),
            'extendedProps': {
                'descripcion': evento.descripcion,
                'progreso': evento.progreso(),
                'dias_restantes': evento.dias_restantes,
                'usuario': evento.usuario.get_full_name(),
                'direccion': evento.usuario.perfil.departamento.nombre
            },
            'color': self._get_color(evento),
            'editable': evento.usuario == self.request.user
        }

    def _get_color(self, evento):
        # Ejemplo: Color diferente para eventos del usuario actual
        if evento.usuario == self.request.user:
            return '#766ec5'  # mis eventos
        return '#7c7c7c'     # otros
    

@method_decorator(login_required, name='dispatch')
class CalendarView(ProfileRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'direccion_actual': request.user.perfil.departamento.nombre
        }
        return render(request, 'calendar.html', context)