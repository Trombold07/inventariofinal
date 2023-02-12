from django.urls import path

#Vistas
from app.home.views import HomePage, HomeProductos

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('ver/productos', HomeProductos.as_view(), name="ver_productos_home")
]
