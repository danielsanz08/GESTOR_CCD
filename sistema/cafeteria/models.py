from django.db import models
from django.conf import settings

class Productos(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Kilogramos', 'Kilogramos'),
        ('Gramos', 'Gramos'),
        ('Litros', 'Litros'),
        ('Mililitros', 'Mililitros'),
        ('Onzas', 'Onzas'),
        ('Unidad', 'Unidad'),
    ]

    nombre = models.CharField(max_length=100, blank=False, null=False)
    marca = models.CharField(max_length=50, blank=False, null=False)
    precio = models.PositiveBigIntegerField(blank=False, null=False)
    cantidad = models.PositiveIntegerField(blank=False, null=False)
    proveedor = models.CharField(max_length=100, blank=False, null=False, default='No establecido')
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    fecha_registro = models.DateField(auto_now=True)
    unidad_medida = models.CharField(
        max_length=15,
        choices=UNIDAD_MEDIDA_CHOICES,
        default='Unidad',
        blank=True,
        null=False
    )
    presentacion = models.CharField(max_length=50, blank=True, null=False, default='No establecido')

    def fecha_formateada(self):
        return self.fecha_registro.strftime('%d-%m-%Y')

    def __str__(self):
        return self.nombre

    def presentacion_formateada(self, longitud=10):
        if not self.presentacion:
            return ""
        texto = self.presentacion.strip()
        return '\n'.join(texto[i:i + longitud] for i in range(0, len(texto), longitud))

    def precio_formateado(self):
        return "{:,}".format(self.precio)


class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado', 'Cancelado'),
    ]

    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name='cafeteria_pedidos',
        default=1
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Pendiente',
        blank=False,
        null=False
    )

    def fecha_formateada(self):
        return self.fecha_pedido.strftime('%d-%m-%Y')

    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='productos',
        blank=False,
        null=False
    )
    producto = models.ForeignKey(
        Productos,
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    cantidad = models.PositiveIntegerField(default=1, blank=False, null=False)
    area = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default='No establecido'
    )
    lugar = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        default='CCD'
    )

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
