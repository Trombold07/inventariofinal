from django.db import models

# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre Empresa")
    telefono = models.CharField(max_length=10, verbose_name="Telefono")
    direccion = models.CharField(max_length=200, verbose_name="direccion")
    logo = models.ImageField(upload_to='logo/%Y/%m/%d', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Comentarios(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre Propietario")
    email = models.EmailField(max_length=200, verbose_name="Email")
    comentario = models.CharField(max_length=150, verbose_name="Comentario")

    def __str__(self):
        return self.nombre
