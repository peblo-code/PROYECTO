# Generated by Django 3.2.6 on 2022-02-09 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0028_pagare_cancelados_pagares'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagare',
            name='total_pagares',
            field=models.IntegerField(null=True),
        ),
    ]
