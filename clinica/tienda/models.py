from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        unique=True
    )
    descripcion = models.CharField(
        max_length=400,
        verbose_name='descripcion',
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.nombre

