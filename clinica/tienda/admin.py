from django.contrib import admin
from tienda.models import Categoria
# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']

admin.site.register(Categoria, CategoriaAdmin)