from pyexpat import model
from django.contrib import admin

from .models import Producto, Categoria
# Register your models here.

class AdminCategoria(admin.ModelAdmin):
    class Meta:
        model = Categoria

admin.site.register(Categoria,AdminCategoria)

class AdminProducto(admin.ModelAdmin):
    class Meta:
        model = Producto

admin.site.register(Producto,AdminProducto)

