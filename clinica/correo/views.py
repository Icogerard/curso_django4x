from django.shortcuts import render
from .forms import FormCorreo
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from usuarios.models import UsuarioPersonalizado

# Create your views here.

@csrf_protect
def enviar_correo(request):
    mensaje_correo = None
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    'success': False,
                    'errores': {'nombre': ['Es necesario ser un usuario activo para enviar correos.']}
                }
            )
        elif request.user.is_staff:
            nombre = request.POST.get('nombre', '').strip()
            if not nombre:
                return JsonResponse({'success': False, 'errores': {'nombre': ['Porfavor, completa tu nombre en el perfil']}})

        form = FormCorreo(request.POST)

        destinatarios = []
        usuarios_sin_correo = []
        for usuario in form['usuarios'].value():
            try:
                usuario_obj = UsuarioPersonalizado.objects.get(pk=usuario)
                if usuario_obj.email:
                    destinatarios.append(usuario_obj.email)
                else:
                    usuarios_sin_correo.append(usuario_obj.username)
            except UsuarioPersonalizado.DoesNotExist:
                pass
        if usuarios_sin_correo:
            mensaje_correo = f'Los siguientes usuarios no tienen una direccion de correo electrónico válida: {", ".join(usuarios_sin_correo)}. Completa tu correo en el perfil'
            return JsonResponse({'success': False, 'errores': {'destinatarios': [mensaje_correo]}})

        if form.is_valid():
            registro = form.save()
            asunto = registro.asunto
            nombre = registro.nombre
            email = registro.email
            mensaje = registro.mensaje
            latitud = registro.latitud
            longitud = registro.longitud

            mensaje_correo = f'<table><tr><td>Nombre:</td><td>{nombre}</td></tr><tr><td>Mensaje:</td><td>{mensaje}</td></tr>'
            if email:
                mensaje_correo += f'<tr><td>Correo electrónico alternativo:</td><td>{email}</td></tr>'
            if latitud:
                mensaje_correo += f'<tr><td>Latitud:</td><td>{latitud}</td></tr>'
            if longitud:
                mensaje_correo += f'<tr><td>Longitud:</td><td>{longitud}</td></tr>'
            mensaje_correo += '</table>'

            if not destinatarios:
                mensaje_correo = {'general': ['No se ha seleccionado ningún destinatario válido.']}
                return JsonResponse({"success": False, "errores": mensaje_correo})           
            else:
                ruta_imagen = None
                if request.user.is_authenticated and request.user.imagen_perfil:
                    ruta_imagen = request.user.imagen_perfil.path
                else:
                    ruta_imagen = './static/assets/img/cc.jpeg'

                email = EmailMessage(
                    asunto,
                    mensaje_correo,
                    'cursodjango4.x@gmail.com',
                    destinatarios,
                    reply_to=['otro@dominio.com'],
                    headers={'Message-ID': 'Checked Code'}
                )

                email.attach_file(ruta_imagen)
                email.content_subtype = "html"

                email.send(fail_silently=False)
                return JsonResponse({"success": True})
        else:
            if 'usuario' in form.errors.as_data():
                print("codigo:", form.errors.as_data()['usuario'][0].code)
            print({"errores": form.errors})
            # mostrar las validaciones
            return JsonResponse({'success': False, 'errores': form.errors})
    else:
        if request.user.is_authenticated:
            nombre_inicial = request.user.first_name
            apellidos_iniciales = request.user.last_name
        else:
            nombre_inicial = 'Anónimo'
            apellidos_iniciales = None
        # En caso cuya solicitud no sea POST
        form = FormCorreo(nombre_inicial=nombre_inicial, apellidos_iniciales=apellidos_iniciales)
        return render(request, 'enviar.html', {'form': form})

def correo(request):
    return render(request, 'correo.html')

