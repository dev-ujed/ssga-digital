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



# Create your views here.
class LoginView(FormView):
    template_name = 'login.html'  # Ruta al archivo de plantilla
    form_class = AuthenticationForm
    success_url = reverse_lazy('nuevo_evento')  # Redirigir después de iniciar sesión

    def form_valid(self, form):
        """Inicia sesión al validar el formulario"""
        user = form.get_user()  # Obtiene el usuario autenticado
        login(self.request, user)  # Inicia la sesión del usuario
        return redirect(self.get_success_url())

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
                # usuario
                #login(request, user)
                return redirect('login')
            except:
                # return HttpResponse('el usuario ya existe')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error' : 'usario ya existe' 
                })
        # return HttpResponse('passwords no coinciden')
        return render(request, 'signup.html', {
            'form': UserCreationForm, 
            'error': 'passwords no coinciden'
    })


class EventosCreateView(CreateView):
    model = Evento
    template_name = 'crear_evento.html'
    form_class = EventoForm
    success_url = reverse_lazy('eventos')


class EventosListView(ListView):
    model = Evento
    template_name = 'eventos.html'
    context_object_name = 'eventos'


class EliminarEventoView(DeleteView):
    model = Evento  # Modelo a eliminar
    template_name = 'confirmar_eliminacion.html'  # Template de confirmación (opcional)
    success_url = reverse_lazy('eventos')


class EventoUpdateView(UpdateView):
    model = Evento
    template_name = 'editar_evento.html'
    form_class = EventoForm
    success_url = reverse_lazy('eventos')


class EventosView(View):
    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        eventos_data = [
            {
                'title': f"{evento.actividad} - {evento.progreso():.2f}% ({evento.dias_restantes} días restantes)",
                'start': evento.fecha_inicio.isoformat(),
                'end': evento.fecha_fin.isoformat(),
                'progreso': evento.progreso(),
                'extendedProps': {
                    'descripcion': evento.descripcion
                },
                'backgroundColor': '#ff5733',
                'borderColor': '#c70039',
                'textColor': '#ffffff',
            }
            for evento in eventos
        ]
        return JsonResponse(eventos_data, safe=False)
    

class CalendarView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'calendar.html')  # Renderiza la plantilla del calendario
