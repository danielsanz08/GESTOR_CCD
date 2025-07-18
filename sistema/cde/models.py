from django.db import models
from cafeteria.models import Productos
from django.conf import settings
from django.utils import timezone

class PedidoCde(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado', 'Cancelado'),
    ]

    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # evita que se borre un usuario que tenga pedidos
        null=False,
        blank=False,
        related_name='cde_pedidos',
        default=1 
    )
    fecha_pedido = models.DateTimeField(default=timezone.now)
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Pendiente',
        null=False,
        blank=False
    )

    def fecha_formateada(self):
        return self.fecha_pedido.strftime('%d-%m-%Y')

    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"


class PedidoProductoCde(models.Model):
    pedido = models.ForeignKey(
        PedidoCde,
        on_delete=models.CASCADE,
        related_name='productos',
        blank=False,
        null=False
    )
    producto = models.ForeignKey(
        Productos,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    cantidad = models.PositiveIntegerField(default=1, null=False, blank=False)
    area = models.CharField(max_length=50, null=False, blank=False, default='No establecido')
    evento = models.CharField(max_length=100, null=False, blank=False, default='CCD')

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"