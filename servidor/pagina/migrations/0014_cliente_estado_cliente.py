# Generated by Django 3.2.8 on 2021-12-17 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0013_ciudad_id_pais'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='estado_cliente',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
