from django.contrib import admin
from .models import RegistroCorreoForm


class RegistroCorreoFormAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'mensaje', 'latitud', 'longitud', 'usuarios_lista', 'creado')

    def usuarios_lista(self, obj):
        return ", ".join([str(usuario) for usuario in obj.usuarios.all()])
    usuarios_lista.short_description = "Usuarios"

admin.site.register(RegistroCorreoForm, RegistroCorreoFormAdmin)
