# Generated by Django 3.2.6 on 2022-02-09 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0027_auto_20220209_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagare',
            name='cancelados_pagares',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]