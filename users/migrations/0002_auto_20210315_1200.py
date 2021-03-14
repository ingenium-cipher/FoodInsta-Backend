# Generated by Django 3.1.7 on 2021-03-15 06:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='contact_no',
            field=models.BigIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(1111111111)]),
        ),
    ]
