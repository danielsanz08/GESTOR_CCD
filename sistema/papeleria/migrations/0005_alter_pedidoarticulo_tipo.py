# Generated by Django 5.1.7 on 2025-04-27 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papeleria', '0004_rename_pedido_articulo_pedidoarticulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidoarticulo',
            name='tipo',
            field=models.CharField(blank=True, default='Null', max_length=100),
        ),
    ]
