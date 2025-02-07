from django.http import HttpResponse
from django.shortcuts import render
# from django.views.generic import ListView
from django.views.generic.edit import CreateView
from api.models import *
from .forms import *


# Create your views here.
def index(request):
    return HttpResponse("You're looking at question %s.")


class EventosCreateView(CreateView):
    model = Evento
    template_name = 'crear_evento.html'
    form_class = EventoForm
