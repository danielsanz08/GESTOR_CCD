from django.db import models
from django.conf import settings
# Create your models here.
class Articulo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50, null=False, blank=False)
    observacion = models.TextField(max_length=30,blank=True, null=True)
    tipo = models.CharField(max_length=50, null=True, blank=True, default='No establecido')
    precio = models.PositiveBigIntegerField(null=False, blank=False)
    cantidad = models.PositiveIntegerField()
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    fecha_registro = models.DateField(auto_now=True)

    def fecha_formateada(self):
        return self.fecha_registro.strftime('%d-%m-%Y')
    def __str__(self):
        return self.nombre
    def observacion_formateada(self, longitud=10):
        if not self.observacion:
            return ""
        texto = self.observacion.strip()
        return '\n'.join(texto[i:i + longitud] for i in range(0, len(texto), longitud))

    def precio_formateado(self):
        """
        Formatea el precio con comas para miles (ejemplo: 1000 -> 1,000).
        """
        return "{:,}".format(self.precio)
class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
    ]
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    def fecha_formateada(self):
        return self.fecha_pedido.strftime('%d-%m-%Y')
    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"

class PedidoArticulo(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='articulos', on_delete=models.CASCADE, null=True)  # Make nullable
    articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=50, null=True, blank=True, default='No establecido')

    def __str__(self):
        return f"{self.articulo.nombre} x {self.cantidad} - {self.tipo}"
