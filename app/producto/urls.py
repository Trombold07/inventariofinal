from django.urls import path

from .views import CrearProductoView, ListarProductosView, EditarProductoView
from .views import CrearCategoriaView, VerCategoriasView

urlpatterns = [
    path('registrar/', CrearProductoView.as_view(), name="registrar_producto"),
    path('listar/', ListarProductosView.as_view(), name="listar_productos"),
    path('editar/<int:pk>/', EditarProductoView.as_view(), name="editar_producto"),
    #Categoria
    path('categoria/registrar/', CrearCategoriaView.as_view(), name="crear_categoria"),
    path('categorias/listar/', VerCategoriasView.as_view(), name="ver_categorias")
]
