# Generated by Django 3.2.9 on 2021-11-15 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='tipo_usuario',
            field=models.IntegerField(default=2, max_length=10),
            preserve_default=False,
        ),
    ]
