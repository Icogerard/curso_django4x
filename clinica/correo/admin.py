from django.contrib import admin
from .models import RegistroCorreoForm


class RegistroCorreoFormAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mensaje', 'latitud', 'longitud', 'usuarios_lista', 'creado')

    def usuarios_lista(self, obj):
        return ", ".join([str(destinatario) for destinatario in obj.destinatarios.all()])
    usuarios_lista.short_description = "Destinatarios"

admin.site.register(RegistroCorreoForm, RegistroCorreoFormAdmin)
