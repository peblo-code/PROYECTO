# Generated by Django 3.2.6 on 2022-01-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0017_auto_20220128_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='telefono_proveedor',
            field=models.CharField(max_length=50),
        ),
    ]
