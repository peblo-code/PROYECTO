# Generated by Django 3.2.6 on 2022-01-28 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0016_auto_20220127_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='direccion_proveedor',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='telefono_proveedor',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
