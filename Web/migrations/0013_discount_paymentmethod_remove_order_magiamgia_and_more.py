# Generated by Django 5.1.3 on 2024-12-06 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0012_employee_alter_user_phone_number_alter_user_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('discountvalue', models.PositiveSmallIntegerField()),
                ('minimum', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('methodname', models.CharField(choices=[('COD', 'COD'), ('MOMO', 'MOMO')], default='COD', max_length=20)),
                ('QRcode', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='magiamgia',
        ),
        migrations.AddField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Web.employee'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Chờ xác nhận', 'Chờ xác nhận'), ('Đang chuẩn bị', 'Đang chuẩn bị'), ('Đang giao', 'Đang giao'), ('Hoàn thành', 'Hoàn thành'), ('Hủy', 'Hủy')], default='Chờ xác nhận', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Web.discount'),
        ),
        migrations.AddField(
            model_name='order',
            name='Payment Method',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Web.paymentmethod'),
            preserve_default=False,
        ),
    ]