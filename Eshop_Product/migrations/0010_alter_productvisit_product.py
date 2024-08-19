# Generated by Django 5.1 on 2024-08-19 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop_Product', '0009_productvisit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvisit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='Eshop_Product.product', verbose_name='محصول'),
        ),
    ]
