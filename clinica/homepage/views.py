from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.


def pagina_principal(request):
    return render(request, 'pagina_principal.html')

