# Generated by Django 5.2.1 on 2025-05-12 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cargo',
            field=models.CharField(default='No establecido', max_length=50),
        ),
    ]
