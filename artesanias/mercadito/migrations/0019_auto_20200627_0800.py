# Generated by Django 3.0.6 on 2020-06-27 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mercadito', '0018_auto_20200627_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='usuario_comprador',
        ),
        migrations.DeleteModel(
            name='Detalle_Orden',
        ),
        migrations.DeleteModel(
            name='Orden',
        ),
    ]
