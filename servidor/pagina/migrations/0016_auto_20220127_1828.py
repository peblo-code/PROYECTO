# Generated by Django 3.2.6 on 2022-01-27 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0015_proveedor_timbrado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='direccion_proveedor',
        ),
        migrations.AddField(
            model_name='proveedor',
            name='estado_proveedor',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
