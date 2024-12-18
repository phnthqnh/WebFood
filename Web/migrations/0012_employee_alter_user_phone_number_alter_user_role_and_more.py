# Generated by Django 5.1.3 on 2024-12-06 15:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0011_alter_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='semployee_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employee',
                'db_table': 'employee',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('employee', 'Employee'), ('manager', 'Manager')], default='manager', max_length=10),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tracking_number', models.CharField(editable=False, max_length=10, unique=True)),
                ('status', models.CharField(choices=[('Chờ xác nhận', 'Chờ xác nhận'), ('Đang chuẩn bị', 'Đang chuẩn bị'), ('Đang giao', 'Đang giao'), ('Hoàn thành', 'Hoàn thành'), ('Hủy', 'Hủy')], default='Đang chờ xác nhận', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hovaten', models.CharField(max_length=200)),
                ('sdt', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=255)),
                ('diachi', models.CharField(max_length=255)),
                ('magiamgia', models.CharField(blank=True, max_length=20, null=True)),
                ('tongtien', models.FloatField(default=0.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Web.customer')),
            ],
        ),
        migrations.DeleteModel(
            name='Staff',
        ),
    ]
