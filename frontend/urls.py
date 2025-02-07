from django import views
from frontend import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('nuevo_evento/', views.EventosCreateView.as_view(), name='nuevo_evento'),
]
