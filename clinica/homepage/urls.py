from django.urls import path
from homepage.views import pagina_principal


urlpatterns = [
    path('', pagina_principal, name='pagina_principal')
]   


