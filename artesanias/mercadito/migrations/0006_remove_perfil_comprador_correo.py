# Generated by Django 3.0.6 on 2020-06-23 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mercadito', '0005_auto_20200623_0226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil_comprador',
            name='correo',
        ),
    ]