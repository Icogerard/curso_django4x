from django.shortcuts import render
from tienda.models import Categoria


def categorias(request):
    categorias = Categoria.objects.all()
    cat_dic = {'cat_dic': categorias}
    return render(request, 'tienda/categorias.html', cat_dic)


# Create your views here.
def juguetes(request):
    dict_productos = {
        "juguete1":"Pelota",
        "juguete2":"Balón",
        "juguete3":"Flauta"
        }
    return render(request, "tienda/juguetes.html", dict_productos) 




def categoria(request):
    return render(request, "tienda/categorias.html") 