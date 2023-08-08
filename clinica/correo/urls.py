from django.urls import path
from . import views


urlpatterns = [
    path('', views.correo, name='correo'),
    path('enviar_correo/', views.enviar_correo, name='enviar_correo'),
    # path('ruta2/', views.vista2, name='vista2'),
]
