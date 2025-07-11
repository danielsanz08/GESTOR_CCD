# Generated by Django 5.1.7 on 2025-06-14 23:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cafeteria', '0005_remove_pedidoproducto_tipo_pedidoproducto_pedido'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoCde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Confirmado', 'Confirmado'), ('Cancelado', 'Cancelado')], default='Pendiente', max_length=20)),
                ('registrado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cde_pedidos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoProductoCde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('area', models.CharField(blank=True, default='No establecido', max_length=50, null=True)),
                ('evento', models.CharField(default='CCD', max_length=100)),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='cde.pedidocde')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafeteria.productos')),
            ],
        ),
    ]
