from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils import timezone
class Articulo(models.Model):
    nombre = models.CharField(max_length=40, blank=False, null=False)
    marca = models.CharField(max_length=30, blank=False, null=False)
    observacion = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.CharField(max_length=30, blank=True, null=True, default='No establecido')
    precio = models.PositiveBigIntegerField(blank=False, null=False)
    cantidad = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)],  # Límite de 10 dígitos
        blank=False,
        null=False
    )
    proveedor = models.CharField(max_length=40, blank=False, null=False, default='No establecido')
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_registro = models.DateField(auto_now=True)

    def nombre_formateado(self):
        """
        Inserta un salto de línea en el nombre si tiene más de 10 caracteres.
        """
        if len(self.nombre) > 10:
            return self.nombre[:10] + '\n' + self.nombre[10:]
        return self.nombre

    def fecha_formateada(self):
        return self.fecha_registro.strftime('%d-%m-%Y')

    def __str__(self):
        return self.nombre

    def precio_formateado(self):
        """
        Formatea el precio con comas para miles (ejemplo: 1000 -> 1,000).
        """
        return "{:,}".format(self.precio)

class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado', 'Cancelado'),
    ]
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_estado = models.DateTimeField(null=True, blank=True) 
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def fecha_formateada(self):
        return self.fecha_pedido.strftime('%d-%m-%Y')

    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"

class PedidoArticulo(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='articulos', on_delete=models.CASCADE, null=True)
    articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True, default='No establecido')

    def areas_unicas(self):
        return ", ".join(sorted(set(articulo.area.nombre for articulo in self.articulos.all() if articulo.area)))

    def __str__(self):
        return f"{self.articulo.nombre} x {self.cantidad} - {self.tipo}"