# Generated by Django 3.0.6 on 2020-06-27 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercadito', '0015_auto_20200627_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='avatar',
            field=models.ImageField(default=270620, upload_to='avatar'),
            preserve_default=False,
        ),
    ]
