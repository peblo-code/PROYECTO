from django.db import models
from django.db.models.aggregates import Max

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

class marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    descripcion_marca = models.CharField(max_length=50)

class modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    id_marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    descripcion_modelo = models.CharField(max_length=50)

class color(models.Model):
    id_color = models.AutoField(primary_key=True)
    descripcion_color = models.CharField(max_length=50)

class vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    id_modelo = models.ForeignKey(modelo, on_delete=models.CASCADE, null=True)
    id_color = models.ForeignKey(color, on_delete=models.CASCADE)
    transmision_vehiculo = models.CharField(max_length=50)
    motor_vehiculo = models.IntegerField()
    anio_vehiculo = models.IntegerField()
    nro_chassis_vehiculo = models.CharField(max_length=100)
    precio_costo = models.IntegerField()
    precio_venta = models.IntegerField()
    estado_vehiculo = models.IntegerField()

class tipo_documento(models.Model):
    id_tipo_documento = models.AutoField(primary_key=True)
    descripcion_tipo_documento = models.CharField(max_length=30)

class pais(models.Model):
    id_pais = models.AutoField(primary_key=True)
    descripcion_pais = models.CharField(max_length=50)

class ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    id_pais = models.ForeignKey(pais, on_delete=models.CASCADE, null=True)
    descripcion_ciudad = models.CharField(max_length=50)

class cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    documento_cliente = models.CharField(max_length=10)
    nombre_cliente = models.CharField(max_length=50)
    apellido_cliente = models.CharField(max_length=50)
    telefono_cliente = models.CharField(max_length=20)
    genero_cliente = models.IntegerField()
    estado_cliente = models.IntegerField()
    id_tipo_documento = models.ForeignKey(tipo_documento, on_delete=models.CASCADE)
    id_pais = models.ForeignKey(pais, on_delete=models.CASCADE, null=True)
    id_ciudad = models.ForeignKey(ciudad, on_delete=models.CASCADE, null=True)

class proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    ruc_proveedor = models.CharField(max_length=20)
    razon_social_proveedor = models.CharField(max_length=50)
    telefono_proveedor = models.CharField(max_length=50)
    direccion_proveedor = models.CharField(max_length=100, null=True)
    estado_proveedor = models.IntegerField()

class timbrado(models.Model):
    nro_timbrado = models.IntegerField(primary_key=True)
    id_proveedor = models.ForeignKey(proveedor, on_delete=models.CASCADE)
    fch_vencimiento_timbrado = models.DateField()

class factura_compra(models.Model):
    id_factura_compra = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(proveedor, on_delete=models.CASCADE)
    nro_timbrado = models.ForeignKey(timbrado, on_delete=models.CASCADE)
    id_vehiculo = models.ForeignKey(vehiculo, on_delete=models.CASCADE)
    nro_factura_compra = models.IntegerField()
    fch_factura_compra = models.DateField()
    condicion_factura_compra = models.IntegerField()

class factura_parametros(models.Model):
    id_factura_parametros = models.AutoField(primary_key=True)
    nro_inicio_factura_parametros = models.IntegerField()
    nro_actual_factura_parametros = models.IntegerField()
    nro_fin_factura_parametros = models.IntegerField()

class timbrado_parametros(models.Model):
    nro_timbrado_parametros = models.IntegerField(primary_key=True)
    id_factura_parametros = models.ForeignKey(factura_parametros, on_delete=models.CASCADE)
    fch_vencimiento_parametros = models.DateField()

class factura_venta(models.Model):
    id_factura_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    nro_timbrado_parametros = models.ForeignKey(timbrado_parametros, on_delete=models.CASCADE)
    id_vehiculo = models.ForeignKey(vehiculo, on_delete=models.CASCADE)
    nro_factura_venta = models.IntegerField()
    fch_factura_venta = models.DateField()
    condicion_factura_venta = models.IntegerField()

class caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    fch_apertura_caja = models.DateField()
    inicio_caja = models.IntegerField()
    fch_cierre_caja = models.DateField(null=True)
    cierre_caja = models.IntegerField(null=True)
    
class detalle_caja(models.Model):
    id_detalle_caja = models.AutoField(primary_key=True)
    id_caja = models.ForeignKey(caja, on_delete=models.CASCADE)
    tipo_movimiento_detalle_caja = models.IntegerField()
    descripcion_detalle_caja = models.CharField(max_length=100)
    monto_detalle_caja = models.IntegerField()