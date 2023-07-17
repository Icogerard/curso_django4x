from django import forms
from django.core.validators import validate_email, MinLengthValidator
from usuarios.models import UsuarioPersonalizado
from .models import RegistroCorreoForm


class CampoOpcionMultipleModeloUsuario(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.username} ({obj.email})'


class FormCorreo(forms.Form):
    class Meta:
        model = RegistroCorreoForm
        fields = ['asunto', 'nombre', 'email', 'mensaje', 'usuarios', 'latitud', 'longitud']

    asunto = forms.CharField(
        label='Asunto',
        max_length=100, 
        validators=[MinLengthValidator(3)],
        required=True,
        error_messages={
            'required': 'El asunto es un campo requerido.',
        }
    )

    nombre = forms.CharField(
        label="Nombre completo", 
        min_length=3,
        max_length=100,
        # validators=[MinLengthValidator(3)],
        required=True,
        error_messages={
            'required': 'El nombre es un campo requerido. Agrega un nombre válido.',
            'min_length': 'El nombre debe tener al menos 3 caracteres.'
        }
    )
    email = forms.EmailField(
        label="Correo alternativo", 
        error_messages={
            'invalid': 'Ingrese una direccion de correo electrónico válida.',
        },
        required=False
    )
    mensaje = forms.CharField(
        label="Mensaje",
        min_length=3,
        widget=forms.Textarea,
        error_messages={
            'min_length': 'Mensaje de por lo menos 3 caracteres.',
            'required': 'El mensaje es un campo requerido.'
        }
    )
    usuarios = CampoOpcionMultipleModeloUsuario(
        queryset=UsuarioPersonalizado.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False)
        # required=False)
    latitud = forms.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitud = forms.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        required=False,
        widget=forms.TextInput(attrs={'readonly':'readonly'})
        )

    def __init__(self, *args, **kwargs):
        nombre_inicial = kwargs.pop('nombre_inicial', None)
        apellidos_iniciales = kwargs.pop('apellidos_iniciales', None)
        super().__init__(*args, **kwargs)
        if nombre_inicial and apellidos_iniciales:
            self.fields['nombre'].initial = f'{nombre_inicial} {apellidos_iniciales}'
        elif nombre_inicial:
            self.fields['nombre'].initial = nombre_inicial
        self.fields['asunto'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['mensaje'].widget.attrs.update({'class': 'form-control'})
        self.fields['usuarios'].widget.attrs.update({'class': 'form-control'})
        self.fields['latitud'].widget.attrs.update({'class': 'form-control'})
        self.fields['longitud'].widget.attrs.update({'class': 'form-control'})


        # self.fields['nombre'].label_suffix = ': *'

        for field_name, field in self.fields.items():
            if field.required:
                field.label_suffix = ' *'
            else:
                field.label_suffix = '  '

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        mensaje = cleaned_data.get('mensaje')
        usuario = cleaned_data.get('usuarios')


        if not nombre and not mensaje and not usuario:
            raise forms.ValidationError("¡Debe ingresar al menos uno de los campos!.")
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if "example.com" in email:
            raise forms.ValidationError("No se permiten correos de example.com")
        return email
        
    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        if "spam" in mensaje:
            raise forms.ValidationError("No se permite la palabra 'spam' en el mensaje.", code='spam')
        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.", code='txt_corto')
        if len(mensaje) > 100:
            raise forms.ValidationError("El mensaje no puede tener más de 100 caracteres.", code='txt_largo')
        return mensaje

    def clean_usuarios(self):
        usuarios = self.cleaned_data.get('usuarios')
        #if not usuarios:
        #    raise forms.ValidationError("El usuario para envío de correo es necesario", code='necesario')
        for usuario in usuarios:
            if not usuario.is_active:
                raise forms.ValidationError("El usuario seleccionado no está activo.", code='inactivo')
            if usuario.username.startswith('admin'):
                raise forms.ValidationError("No se permite enviar correo a usuarios con nombre de usuario que comience con 'admin'.", code='admin')
        return usuarios

    def clean_latitud(self):
        latitud = self.cleaned_data['latitud']
        if latitud is not None:
            if latitud < -90:
                raise forms.ValidationError("La latitud no puede ser menor a -90.", code='num_corto')
            if latitud > 90:
                raise forms.ValidationError("La latitud no puede ser mayor a 90.", code='num_largo')
        return latitud

    def clean_longitud(self):
        longitud = self.cleaned_data['longitud']
        if longitud is not None:
            if longitud < -180:
                raise forms.ValidationError("La longitud no puede ser menor a -180.", code='num_corto')
            if longitud > 180:
                raise forms.ValidationError("La longitud no puede ser mayor a 180.", code='num_largo')
        return longitud
    
    def save(self):
        asunto = self.cleaned_data['asunto']
        nombre = self.cleaned_data['nombre']
        email = self.cleaned_data['email']
        mensaje = self.cleaned_data['mensaje']
        usuarios = self.cleaned_data['usuarios']
        latitud = self.cleaned_data['latitud']
        longitud = self.cleaned_data['longitud']

        registro = RegistroCorreoForm.objects.create(
            asunto=asunto,
            nombre=nombre,
            email=email,
            mensaje=mensaje,
            latitud=latitud,
            longitud=longitud
        )
        registro.usuarios.set(usuarios)
        return registro
