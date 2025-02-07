from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'direcciones', views.DireccionViewSet)
router.register(r'eventos', views.EventoViewSet)

urlpatterns = [
    path('', include(router.urls))
]