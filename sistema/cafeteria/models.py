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