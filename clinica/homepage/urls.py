from django.urls import path
from homepage.views import mostrar


urlpatterns = [
    path('', mostrar)
]   


