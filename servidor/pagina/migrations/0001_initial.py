# Generated by Django 3.2.8 on 2021-12-01 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usuarios',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=10)),
                ('clave', models.CharField(max_length=10)),
                ('nombre_completo', models.CharField(max_length=200)),
            ],
        ),
    ]
