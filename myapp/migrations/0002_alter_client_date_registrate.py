# Generated by Django 5.0.3 on 2024-05-04 08:20

import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_registrate',
            field=models.DateTimeField(validators=[myapp.models.check_date_created], verbose_name='date_registrate'),
        ),
    ]
