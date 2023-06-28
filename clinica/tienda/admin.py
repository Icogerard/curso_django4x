from django.contrib import admin
from tienda.models import Categoria, Producto, Pedido, DetallePedido
# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)