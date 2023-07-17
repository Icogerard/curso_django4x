
function obtenerUbicacion(callback, errorCallback = mostrarError) {
    console.log('Obteniendo ubicación...')
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const { latitude: latitud, longitude: longitud } = position.coords;
                console.log(`Latitud: ${latitud} Longitud: ${longitud}`);
                callback(latitud, longitud);
        }, // Si ocurre un error al obtener la ubicación
            errorCallback
        );
    } else {
        console.log('Geolocalización no soportada por el navegador.')
    }
}


function mostrarError(error) {
    // utilizamos switch para verificar el código de error y mostrar mensaje apropiado
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.log("El usuario denegó la solicitud de geolocalización.")
            break;
        case error.POSITION_UNAVAILABLE:
            console.log("La información de ubicación no estpa disponible.")
            break;
        case error.TIMEOUT:
            console.log("Se agotó el tiempo de espera de la solicitud.")
            break;
        case error.UNKNOWN_ERROR:
            console.log("Un error desconocido ocurrió.")
            break;
    }
}

function mostrarUbicacion() {
    obtenerUbicacion((lat, long) => {
        $('#id_latitud').val(lat)
        $('#id_longitud').val(long)
    });
    $('#id_boton_mostrar').hide();
    $('#id_boton_borrar').show();
}

function borrarUbicacion(){
    $('#id_latitud').val('')
    $('#id_longitud').val('') 
    // ocultando el boton borrar ubicacion 
    $('#id_boton_borrar').hide(); 
    // mostrando el boton mostrar ubicacion 
    $('#id_boton_mostrar').show();
}

function verificarUbicacion() {
    if ($('#id_latitud').val() && $('#id_longitud').val()) {
        // si los campos latitud y longitud tienen valores, muestra el boton mostrar ubicacion y oculta borrar ubicacion
        $('#id_boton_borrar').show();
        $('#id_boton_mostrar').hide();
    } else {
        $('#id_boton_mostrar').show();
        $('#id_boton_borrar').hide();
    }
}

$('form.mensaje_correo').on('submit', function(event) {
    event.preventDefault();
    var form = this;
    console.log("Manejando el evento submit");
    $.ajax({
        type: 'POST',
        url: '/enviar_correo/',
        data: $(form).serialize(),
        success: function(response) {
            if (response.success) {
                // los datos del formulario son válidos
                swal('Mensaje enviado con éxito')
                // limpiar formulario
                form.reset();
            } else {
                // los datos del formulario no son válidos
                var errores = response.errores;
                console.log(errores)
                var errorMensaje = '';
                for (var campo in errores) {
                    var errorLista = errores[campo];
                    for (var i = 0; i < errorLista.length; i++) {
                        var error = errorLista[i];
                        errorMensaje += 'Error en el campo ' + campo + ': ' + error + '\n';
                    }
                }
                swal(errorMensaje);
            }
            verificarUbicacion();
        }
    });
});



