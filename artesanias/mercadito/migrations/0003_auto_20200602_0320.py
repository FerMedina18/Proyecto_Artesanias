# Generated by Django 3.0.6 on 2020-06-02 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercadito', '0002_auto_20200602_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_orden',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='producto',
            name='existencia',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
