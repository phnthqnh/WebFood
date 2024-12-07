# Generated by Django 5.1.3 on 2024-12-07 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0013_discount_paymentmethod_remove_order_magiamgia_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Web.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Web.product')),
            ],
        ),
    ]