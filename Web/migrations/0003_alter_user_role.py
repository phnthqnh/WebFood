# Generated by Django 5.1.3 on 2024-12-02 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('staff', 'Staff'), ('manager', 'Manager')], default='manager', max_length=10),
        ),
    ]
