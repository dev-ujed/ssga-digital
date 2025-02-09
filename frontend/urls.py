from django import views
from frontend import views
from django.urls import path


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('cerrar_sesion/', views.LogoutView.as_view(), name='logout'),
    path('registrarme/', views.user_register, name='registro'),
    path('nuevo_evento/', views.EventosCreateView.as_view(), name='nuevo_evento'),
]
