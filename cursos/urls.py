from django.urls import path
from cursos import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # PERIODOS
    path('periodos/',               views.PeriodosListView.as_view(),           name='periodos'),
    path('crear_periodos/',         views.PeriodoCreateView.as_view(),          name='crear_periodos'),
    path('editar_periodo/<int:pk>', views.PeriodoUpdateView.as_view(),          name='editar_periodo'),
    path('eliminar_periodo/<int:pk>/', views.EliminarPeriodo.as_view(),         name='eliminar_periodo'),
    # CURSOS
    path('cursos/',                 views.CursosListView.as_view(),             name='cursos'),
    path('crear_curso/',            views.CursoCreateView.as_view(),            name='crear_curso'),
    path('curso_detail/<int:pk>/',  views.detail, name='curso_detail'),
    # path('curso/delete/<int:pk>/',    views.CursoDeleteView.as_view(),          name='curso_delete'),
    path('inscripcion/delete/<int:pk>/',    views.InscripcionDeleteView.as_view(),  name='inscripcion_delete'),
    path('profile/',                views.UserRecordsView.as_view(),            name="perfil"), 
    #;;;;;;;; admin ;;;;;;;;;;
    path('cursos-admin/', views.CursosAdListView.as_view(), name='cursos_admin'),
    path('eliminar-curso/<int:pk>/', views.EliminarCursoView.as_view(), name='eliminar_curso'),
    path('editar_curso/<int:pk>', views.CursoUpdateView.as_view(),          name='editar_curso'),
    path('obtener_cv/<int:pdf_id>/', views.obtener_cv,    name='obtener_cv'),
    path('obtener_flayer/<int:pdf_id>/', views.obtener_flayer,    name='obtener_flayer'),
    path('cursos/<int:curso_id>/usuarios/', views.UsuariosCursoListView.as_view(), name='usuarios-curso'),
    #;;;;;;;;;;;;;;;; Maestros
    path('maestros/', views.MaestroListView.as_view(), name='maestros'),
    path('registrar_maestro/', views.MaestroCreateView.as_view(), name='add_maestro'),
    path('editar_maestro/<int:pk>', views.MaestroUpdateView.as_view(),          name='editar_maestro'),
    path('eliminar_maestro/<int:pk>/', views.EliminarMaestroView.as_view(), name='eliminar_maestro'),
    # map
    path('mapa-sitio/', views.MapaSitioView.as_view(), name='mapa_sitio'),
    path('editar_perfil/', views.EditarPerfil.as_view(), name='editar_perfil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)