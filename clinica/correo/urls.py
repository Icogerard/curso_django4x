from django.urls import path
from . import views

app_name = 'correo'

urlpatterns = [
    path('mensaje/', views.mensaje_correo, name='mensaje_correo'),
    # path('ruta2/', views.vista2, name='vista2'),
]
