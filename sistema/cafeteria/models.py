from django.db import models
from django.conf import settings
# Create your models here.
class Productos(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Kilogramos', 'Kilogramos'),
        ('Gramos', 'Gramos'),
        ('Litros', 'Litros'),
        ('Mililitros', 'Mililitros'),
        ('Onzas', 'Onzas'),
        ('Unidad', 'Unidad'),
    ]
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50, null=False, blank=False)
    precio = models.PositiveBigIntegerField(null=False, blank=False)
    cantidad = models.PositiveIntegerField()
    proveedor = models.CharField(max_length=100, null=False, blank=False, default='No establecido')
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    fecha_registro = models.DateField(auto_now=True)
    unidad_medida = models.CharField(max_length=15, choices=UNIDAD_MEDIDA_CHOICES, default='unidad')
    presentacion = models.CharField(max_length=50, null=False, blank=False, default='No establecido')
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
        """
        Formatea el precio con comas para miles (ejemplo: 1000 -> 1,000).
        """
        return "{:,}".format(self.precio)
    
class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Cancelado' , 'Cancelado'),
    ]
    registrado_por = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    related_name='cafeteria_pedidos'
)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    def fecha_formateada(self):
        return self.fecha_pedido.strftime('%d-%m-%Y')
    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"

class PedidoProducto(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True, default='No establecido')
    lugar = models.CharField(max_length=100, null=False, blank=False, default='CCD')
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} - {self.tipo}"


