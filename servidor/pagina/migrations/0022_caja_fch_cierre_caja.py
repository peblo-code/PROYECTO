# Generated by Django 3.2.6 on 2022-02-04 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0021_caja_detalle_caja_factura_parametros_factura_venta_timbrado_parametros'),
    ]

    operations = [
        migrations.AddField(
            model_name='caja',
            name='fch_cierre_caja',
            field=models.DateField(null=True),
        ),
    ]