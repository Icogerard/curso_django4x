from django import forms
from django.core.validators import validate_email, MinLengthValidator
from usuarios.models import UsuarioPersonalizado
from .models import RegistroCorreoForm


class CampoOpcionMultipleModeloUsuario(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.username} ({obj.email})'


class FormCorreo(forms.ModelForm):
    class Meta:
        model = RegistroCorreoForm
        fields = ['asunto', 'nombre', 'mensaje', 'destinatarios', 'latitud', 'longitud']

    asunto = forms.CharField(
        label='Asunto *',
        max_length=50, 
        validators=[MinLengthValidator(3)],
        required=False,
    )
    nombre = forms.CharField(
        label="Nombre completo *", 
        min_length=3,
        max_length=50,
        # validators=[MinLengthValidator(3)],
        required=False,
    )
    mensaje = forms.CharField(
        label="Mensaje",
        min_length=5,
        widget=forms.Textarea,
        required=False,
        error_messages={
            'min_length': 'Mensaje de por lo menos 5 caracteres.',
        }
    )
    destinatarios = CampoOpcionMultipleModeloUsuario(
        queryset=UsuarioPersonalizado.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label='Destinatarios *')
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
        usuario_actual_pk = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)
        if nombre_inicial and apellidos_iniciales:
            self.fields['nombre'].initial = f'{nombre_inicial} {apellidos_iniciales}'
        elif nombre_inicial:
            self.fields['nombre'].initial = nombre_inicial

        for campo in ['asunto', 'nombre', 'mensaje', 'destinatarios', 'latitud', 'longitud']:
            self.fields[campo].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'readonly': 'readonly'})

        if usuario_actual_pk is not None:
            self.fields['destinatarios'].queryset = UsuarioPersonalizado.objects.exclude(email='').exclude(pk=usuario_actual_pk.pk).filter(is_active=True, is_staff=True)
        else:
            self.fields['destinatarios'].queryset = UsuarioPersonalizado.objects.exclude(email='').filter(is_active=True, is_staff=True)


        # self.fields['nombre'].label_suffix = ': *'

        for field_name, campo in self.fields.items():
            if campo.required:
                campo.label_suffix = ' *'
            else:
                campo.label_suffix = '  '

    def clean(self):
        cleaned_data = super().clean()
        asunto = cleaned_data.get('asunto')
        mensaje = cleaned_data.get('mensaje')
        destinatarios = cleaned_data.get('destinatarios')

        campos_no_validados = []
        if not asunto and not self.has_error('asunto'):
            campos_no_validados.append('asunto')
        if not mensaje and not self.has_error('mensaje'):
            campos_no_validados.append('mensaje')
        if not destinatarios:
            campos_no_validados.append('destinatarios')

        if campos_no_validados:
            self.campos_validados = campos_no_validados
            mensaje_error = f"¡Debes ingresar {', '.join(campos_no_validados)}!"
            raise forms.ValidationError(mensaje_error, code='requeridos')
        
    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        if len(mensaje) > 100:
            raise forms.ValidationError("El mensaje no puede tener más de 100 caracteres.", code='txt_largo')
        return mensaje

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
    

