from django.db import models
from django.utils import timezone
from usuarios.models import UsuarioPersonalizado


class RegistroCorreoForm(models.Model):
    asunto = models.CharField(max_length=100)
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    mensaje = models.TextField()
    usuarios = models.ManyToManyField(UsuarioPersonalizado)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    creado = models.DateTimeField(default=timezone.now)
    actualizado = models.DateTimeField(auto_now=True)

