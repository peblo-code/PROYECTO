from django.db import models

# Create your models here.

class usuarios(models.Model):
    id_usuario=models.AutoField(primary_key=True)
    usuario=models.CharField(max_length=10)
    clave=models.CharField(max_length=10)
    nombre_completo=models.CharField(max_length=200)
    tipo_usuario=models.IntegerField(null=True)

class tipo_usuario(models.Model):
    id_tipo_usuario=models.AutoField(primary_key=True)
    descripcion_tipo_usuario=models.CharField(max_length=50)