from django.db import models
from cafeteria.models import Productos
from django.conf import settings
# Create your models here.
class PedidoCde(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado' , 'Cancelado'),
    ]
    registrado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    related_name='cde_pedidos'
)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    def fecha_formateada(self):
        return self.fecha_pedido.strftime('%d-%m-%Y')
    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"

class PedidoProductoCde(models.Model):
    pedido = models.ForeignKey(PedidoCde, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    area = models.CharField(max_length=50, null=True, blank=True, default='No establecido')
    evento = models.CharField(max_length=100, null=False, blank=False, default='CCD')
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"


