# Generated by Django 5.1.3 on 2024-12-09 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0020_cart_products_order_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Web.employee'),
        ),
    ]