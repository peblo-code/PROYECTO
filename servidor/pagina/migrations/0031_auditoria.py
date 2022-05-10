# Generated by Django 3.2.6 on 2022-02-10 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0030_alter_pagare_cancelados_pagares'),
    ]

    operations = [
        migrations.CreateModel(
            name='auditoria',
            fields=[
                ('id_auditoria', models.AutoField(primary_key=True, serialize=False)),
                ('usuario_creacion', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateField()),
                ('usuario_modificacion', models.CharField(max_length=100, null=True)),
                ('fecha_modificacion', models.DateField(null=True)),
                ('id_cambio', models.IntegerField()),
                ('tabla_cambio', models.IntegerField()),
            ],
        ),
    ]