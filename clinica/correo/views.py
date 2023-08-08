from django.shortcuts import render
from .forms import FormCorreo
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from usuarios.models import UsuarioPersonalizado
from functools import wraps
from django.shortcuts import redirect


def solo_miembros_del_personal(vista_protegida):
    @wraps(vista_protegida)
    def _vista_envuelta(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        elif not request.user.is_staff:
            return redirect('/')
        else:
            return vista_protegida(request, *args, **kwargs)
    return _vista_envuelta

@solo_miembros_del_personal
@csrf_protect
def enviar_correo(request):
    mensaje_error = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if not nombre:
            return JsonResponse({'success': False, 'errores': {'nombre': ['Porfavor, completa tu nombre en el perfil']}})
        if not request.user.email:
            mensaje_error = {'email': ['No cuentas con email. Completa el campo en el perfil']}
            return JsonResponse({'success': False, 'errores': mensaje_error})


        form = FormCorreo(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            errores = form.errors.as_data()
            mensaje_error = {}
            for campo, lista_errores in errores.items():
                if campo == '__all__':
                    campo = form.campos_validados
                errores_str = []
                for error in lista_errores:
                    errores_str.append(str(error))
                mensaje_error[(str(campo))] = errores_str
            return JsonResponse({'success': False, 'errores': mensaje_error})
    else:
        if request.user.is_authenticated:
            if request.user.first_name and request.user.last_name:
                nombre_inicial = request.user.first_name
                apellidos_iniciales = request.user.last_name
            else:
                nombre_inicial = request.user.first_name
                apellidos_iniciales = None
        else:
            nombre_inicial = None
            apellidos_iniciales = None
        
        # En caso cuya solicitud no sea POST
        form = FormCorreo(nombre_inicial=nombre_inicial, apellidos_iniciales=apellidos_iniciales, usuario_actual=request.user)
        return render(request, 'enviar.html', {'form': form})

@solo_miembros_del_personal
def correo(request):
    return render(request, 'correo.html')

