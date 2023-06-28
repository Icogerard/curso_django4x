from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre", unique=True)
    descripcion = models.TextField(max_length=500, null=True, blank=True, verbose_name="Descripción")
    autor_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255,  unique=True, verbose_name="Nombre")
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio")
    imagen = models.ImageField(upload_to='productos/%Y/%m/%d', null=True, blank=True, verbose_name="Imagen")
    categoria_id = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    autor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre

    
class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return f'Pedido {self.id} de {self.cliente}'


class DetallePedido(models.Model):
    pedido_id = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)

    def __str__(self):
        return f'{self.pedido_id} - {self.producto_id}[{self.cantidad}]'
    