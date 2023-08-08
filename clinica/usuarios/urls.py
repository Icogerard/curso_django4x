from django.contrib.auth import views as auth_view
from django.urls import path
from .forms import MiFormularioDeAutenticacion
from .views import mi_vista_inicio_sesion, mi_vista_cierre_sesion

urlpatterns = [
    path('login/', mi_vista_inicio_sesion, {'form_class': MiFormularioDeAutenticacion}, name='login'),
    path('logout/', mi_vista_cierre_sesion, {'next_page': '/registro/login/'}, name='logout'),
]