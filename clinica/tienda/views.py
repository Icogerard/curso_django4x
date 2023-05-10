from django.shortcuts import render

# Create your views here.
def juguetes(request):
    dict_productos = {
        "juguete1":"Pelota",
        "juguete2":"Balón",
        "juguete3":"Flauta"
        }
    return render(request, "tienda/juguetes.html", dict_productos) 

# Create your views here.
def zapatos(request):
    dict_productos = {
        "zapato1":"zapato1",
        "zapato2":"zapato2",
        "zapato3":"zapato3"
        }
    return render(request, "tienda/zapatos.html", dict_productos) 

def jardineria(request):
    contexto = {"usuario":"Azahara"}
    return render(request, "tienda/eco.html", contexto) 

def categoria(request):
    return render(request, "tienda/categorias.html") 