import sys

from faker import Faker
sys.path.append("C:\\Users\\yumkimil\\Documents\\Repos\\curso_django4x\\clinica")
from clinica.wsgi import *
from tienda.models import Categoria, Producto, Pedido, DetallePedido
from django.db.models import Q, Avg, Min, Max, Sum
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Count


admin = User.objects.get(username="admin")

# crear categorias aleatorias
"""def crear_categorias_aleatorias(n):
    for i in range(n):
        fake = Faker("es_ES")  # crear un objeto Faker en español
        categoria = fake.word()  # generamos una palabra aleatoria 
        nombre = categoria
        # print(nombre)
        try:
            categoria = Categoria.objects.create(nombre=nombre, autor_id=admin)
            print(f"Se ha creado la categoria {nombre}")
        except Exception as e:
            print("La categoria", e, "ya ha sido agregada.")


crear_categorias_aleatorias(5)"""

(num, dic) = Producto.objects.filter(categoria_id__nombre="Juguetes").delete()

print(num)
print(dic)