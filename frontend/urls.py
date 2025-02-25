from django import views
from frontend import views
from django.urls import path


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('cerrar_sesion/', views.LogoutView.as_view(), name='logout'),
    path('registrarme/', views.user_register, name='registro'),
    path('nuevo_evento/', views.EventosCreateView.as_view(), name='nuevo_evento'),
    path('listar_eventos/', views.EventosListView.as_view(), name='eventos'),
    path('eliminar-evento/<int:pk>/', views.EliminarEventoView.as_view(), name='eliminar_evento'),
    path('editar_evento/<int:pk>', views.EventoUpdateView.as_view(),          name='editar_evento'),
    path('events/', views.EventosView.as_view(), name='get_events'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('direcciones_admin/', views.DireccionesAdminView.as_view(), name='direcciones'),
]
