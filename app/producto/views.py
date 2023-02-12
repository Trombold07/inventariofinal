import json
from urllib import request
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Producto, Categoria
from app.proveedor.models import Proveedor
from .forms import RegistrarProductoForm, EditarProductoForm, CategoriaForm
from app.user.mixins import ValidatePermissionRequiredMixin

# Create your views here.

class CrearProductoView(ValidatePermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Producto
    form_class = RegistrarProductoForm
    template_name = 'registrar_producto.html'
    permission_required= 'add_producto'
    success_url = reverse_lazy('listar_productos')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "buscarproveedor":
                data = []
                proveedor = Proveedor.objects.filter(cod_proveedor__icontains = request.POST['term'])[0:10]
                for i in proveedor:
                    item = i.toJson()
                    item['text'] = i.cod_proveedor
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    producto = Producto()
                    producto.categoria_id = request.POST.get('categoria')
                    producto.cod_producto = request.POST.get('cod_producto')
                    producto.cod_proveedor_id = request.POST.get('cod_proveedor')
                    producto.nombre = request.POST.get('nombre')
                    producto.precio_unitario = request.POST.get('precio_unitario')
                    producto.stock = int(request.POST.get('stock'))
                    producto.imagen = request.FILES.get('imagen')
                    producto.save()
                    print(request.POST.get('categoria'))
                    messages.success(request, 'Producto creado con Exito')
                    
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['titulo'] = "Registrar Producto"
        context['success_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('index')
        return context

class ListarProductosView(ValidatePermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Producto
    template_name = "listar_productos.html"
    permission_required= 'view_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'ver_productos':
                data= []
                for i in Producto.objects.all():
                    data.append(i.toJson())
            elif action == 'delete':
                producto = Producto.objects.get(pk = request.POST['id'])
                producto.delete()
                messages.success(request, "Producto eliminado con Exito")
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Lista de Productos"
        context['list_actualizar'] = reverse_lazy('listar_productos')
        return context    

class EditarProductoView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = EditarProductoForm
    template_name = "editar_producto.html"
    success_url = reverse_lazy('listar_productos')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "edit":
                producto = Producto.objects.get(pk = kwargs['pk'])
                producto.cod_producto = request.POST.get('cod_producto')
                producto.cod_proveedor_id = request.POST.get('cod_proveedor')
                producto.nombre = request.POST.get('nombre')
                producto.precio_unitario = request.POST.get('precio_unitario')
                producto.stock = int(request.POST.get('stock'))
                producto.imagen = request.FILES.get('imagen')
                producto.save()
                messages.success(request, "Producto editado con Exito")
            else:
                data['error'] = "Ha ocurrido un error"

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "edit"
        context['mensaje_informacion'] = "¿ Seguro que desea Editar este registro ?"
        context['titulo'] = "Editar Producto"
        context['success_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('listar_productos')
        return context

#Categoria
class CrearCategoriaView(ValidatePermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = "categorias/crear_categoria.html"
    success_url = reverse_lazy('ver_categorias')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    categoria = Categoria()
                    categoria.nombre = request.POST.get('nombre')
                    categoria.descripcion = request.POST.get('descripcion')
                    categoria.imagen = request.FILES.get('imagen')
                    categoria.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['titulo'] = 'Registrar Categoria'
        context['success_url'] = self.success_url
        context['cancel_url'] = reverse_lazy('ver_categorias')
        return context

class VerCategoriasView(ValidatePermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Categoria
    template_name = "categorias/listar_categorias.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'ver_categorias':
                data= []
                for i in Categoria.objects.all():
                    data.append(i.toJson())
            elif action == 'delete':
                producto = Categoria.objects.get(pk = request.POST['id'])
                producto.delete()
                messages.success(request, "Categoria eliminado con Exito")
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Lista de Productos"
        context['list_actualizar'] = reverse_lazy('ver_categorias')
        return context 