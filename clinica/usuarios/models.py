from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UsuarioPersonalizado(AbstractUser):
    imagen_perfil = models.ImageField(upload_to='perfiles', blank=True, null=True)
