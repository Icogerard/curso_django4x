from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.


def mostrar(request):
    return HttpResponse("<h2> Bienvenidos! Esto es Checked Code</h2>")

def mostrarDateTime(request):
    dt = datetime.datetime.now()
    dt = str(dt)
    c = "<h2> Fecha y hora actual: </h2>" + "<b>" + dt +"</b>"
    return HttpResponse(c)
