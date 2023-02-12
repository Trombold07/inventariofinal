from email.policy import default
from django.db import models
from app.proveedor.models import Proveedor
from django.forms.models import model_to_dict
from inventario.settings import MEDIA_URL, STATIC_URL

from datetime import datetime

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=250, null=False)
    descripcion = models.TextField(max_length=250, null=False)
    imagen = models.ImageField(upload_to='categoria/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def obtener_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
        
    def toJson(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        item['descripcion'] = self.descripcion
        item['imagen'] = self.obtener_imagen()
        return item

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete= models.CASCADE)
    cod_proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE)
    cod_producto = models.CharField(max_length=10, unique= True, null=False)
    nombre = models.CharField(max_length = 250, null=False)
    precio_unitario = models.DecimalField( max_digits=10, decimal_places=2, null=False)
    stock = models.IntegerField(null=False)
    imagen = models.ImageField(upload_to='producto/%Y/%m/%d', null=True, blank=True)
    fecha_creacion = models.DateField(default = datetime.now)

    def __str__(self):
        return self.cod_producto
    
    def obtener_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJson(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.nombre
        item['cod_proveedor'] = self.cod_proveedor.cod_proveedor
        item['cod_producto'] = self.cod_producto
        item['nombre'] = self.nombre
        item['precio_unitario'] = self.precio_unitario
        item['stock'] = self.stock
        item['imagen'] = self.obtener_imagen()
        item['fecha_creacion'] = self.fecha_creacion
        return item



    