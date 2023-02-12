from django.shortcuts import render
from django.views.generic import TemplateView, ListView

#Modelos
from app.producto.models import Producto

# Create your views here.
class HomePage(TemplateView):
    template_name = 'home/home_index.html'

class HomeProductos(ListView):
    template_name = 'home/home_productos.html'
    paginate_by = 5
    model = Producto

