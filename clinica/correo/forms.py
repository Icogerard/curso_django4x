from django import forms
from django.core.validators import validate_email, MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class FormCorreo(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo", 
        max_length=100,
        validators=[MinLengthValidator(3)],
        required=True,
        error_messages={
            'required': 'El nombre es un campo requerido. Agrega un nombre válido.',
            'min_lenght': 'El nombre debe tener al menos 3 caracteres.'
        }
    )
    email = forms.EmailField(
        label="Correo alternativo", 
        error_messages={
            'min_lenght': 'El nombre debe tener al menos 3 caracteres.',
            'required': 'El correo electronico no es un campo requerido.'
        },
        required=False
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea,
        error_messages={
            'invalid': 'Ingrese una direccion de correo electrónico válida.',
            'required': 'El mensaje es un campo requerido.'
        }
    )
    usuario = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['mensaje'].widget.attrs.update({'class': 'form-control'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control'})

        # self.fields['nombre'].label_suffix = ': *'

        for field_name, field in self.fields.items():
            print(field_name)
            if field.required:
                field.label_suffix = ' *'

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        email = cleaned_data.get('email')
        mensaje = cleaned_data.get('mensaje')
        usuario = cleaned_data.get('usuario')


        if not nombre and not email and not mensaje:
            raise forms.ValidationError("Debe ingresar al menos uno de los campos!.")
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if "example.com" in email:
            raise forms.ValidationError("No se permiten correos de example.com")
        return email
        
    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        if "spam" in mensaje:
            raise forms.ValidationError("No se permite la palabra 'spam' en el mensaje.")
        return mensaje  
