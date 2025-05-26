from django.urls import path
from folios import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('subir/',  views.subirExcel, name='subir'),
    path('lista_participantes/', views.ParticipantesListView.as_view(), name='participantes'),
    path('autenticidad_folio/', views.buscar_folio, name='buscar_folio'),
    path('agregar_participantes/', views.AddParticipante.as_view(), name='agregar_participante'),
    path('del_participante/<int:pk>/', views.DelParticipante.as_view(), name='del_participante'),
    path('actualizar_participante/<int:pk>/', views.UpdateParseView.as_view(), name='upd_parse'),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 