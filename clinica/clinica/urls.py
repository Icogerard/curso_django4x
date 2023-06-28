from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', include('homepage.urls')),
    path('', views.categorias),
    path('juguetes/', views.juguetes),
    path('', include('correo.urls', namespace='correo')),
]
