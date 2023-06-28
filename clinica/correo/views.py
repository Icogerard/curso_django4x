from django.shortcuts import render
from .forms import FormCorreo
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import send_mail

# Create your views here.

@csrf_protect
def mensaje_correo(request):
    if request.method == 'POST':
        form = FormCorreo(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            # Procesar los datos del formulario
            send_mail(
                'Checked Code | Curso Django 4.2',
                f'Nombre: {nombre}\n Email: {email}\n Mensaje: {mensaje}',
                'correo-de-envio@empresa.com',
                [form.cleaned_data['usuario'].email],
                fail_silently=False,
            )
            return JsonResponse({"mensaje": "Mensaje envíado!"})
    else:
        # En caso cuya solicitud no sea POST
        form = FormCorreo()
    return render(request, 'correo.html', {'form': form})
