# Generated by Django 3.2.6 on 2022-02-08 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0023_auto_20220208_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura_venta',
            name='fch_cobrado_factura_venta',
            field=models.DateField(null=True),
        ),
    ]
