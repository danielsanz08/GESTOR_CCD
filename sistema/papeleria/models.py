from django.db import models
from django.conf import settings
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
# Create your models here.
class Articulo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50, null=False, blank=False)
    observacion = models.TextField(max_length=30,blank=True, null=True)
    tipo = models.CharField(max_length=50, null=True, blank=True, default='No establecido')
    precio = models.PositiveBigIntegerField(null=False, blank=False)
    cantidad = models.PositiveIntegerField()
    proveedor = models.CharField(max_length=100, null=False, blank=False, default='No establecido')
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    fecha_registro = models.DateField(auto_now=True)

<<<<<<< HEAD
=======
=======
from django.core.validators import MaxValueValidator
# Create your models here.
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
            # Inserta un salto de línea después de los primeros 10 caracteres
            return self.nombre[:10] + '\n' + self.nombre[10:]
        return self.nombre
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
    def fecha_formateada(self):
        return self.fecha_registro.strftime('%d-%m-%Y')
    def __str__(self):
        return self.nombre
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
    def observacion_formateada(self, longitud=10):
        if not self.observacion:
            return ""
        texto = self.observacion.strip()
        return '\n'.join(texto[i:i + longitud] for i in range(0, len(texto), longitud))
<<<<<<< HEAD
=======
=======
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)

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
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    def fecha_formateada(self):
        return self.fecha_pedido.strftime('%d-%m-%Y')
    def __str__(self):
        return f"Pedido {self.id} - {self.get_estado_display()}"
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)

class PedidoArticulo(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='articulos', on_delete=models.CASCADE, null=True)  # Make nullable
    articulo = models.ForeignKey('Articulo', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
<<<<<<< HEAD
    tipo = models.CharField(max_length=50, null=True, blank=True, default='No establecido')
    area = models.CharField(max_length=50, null=True, blank=True, default='No establecido')

=======
<<<<<<< HEAD
    tipo = models.CharField(max_length=50, null=True, blank=True, default='No establecido')
    area = models.CharField(max_length=50, null=True, blank=True, default='No establecido')

=======
    tipo = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True, default='No establecido')
    def areas_unicas(self):
        return ", ".join(sorted(set(articulo.area.nombre for articulo in self.articulos.all() if articulo.area)))
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
    def __str__(self):
        return f"{self.articulo.nombre} x {self.cantidad} - {self.tipo}"

