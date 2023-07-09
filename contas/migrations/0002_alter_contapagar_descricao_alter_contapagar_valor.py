# Generated by Django 4.2.3 on 2023-07-09 18:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contapagar',
            name='descricao',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='contapagar',
            name='valor',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
    ]