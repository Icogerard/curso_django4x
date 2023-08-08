from django import forms
from django.contrib.auth.forms import AuthenticationForm

class MiFormularioDeAutenticacion(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs.update({'class': 'form-control'})