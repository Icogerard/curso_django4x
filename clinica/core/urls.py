from django.urls import path
from core.views import mostrar, mostrarDateTime


urlpatterns = [
    path('ruta1/', mostrar),
    path('datetime/', mostrarDateTime),
]