from django import forms
from papeleria.models import Articulo, PedidoArticulo,Devolucion, Pedido
from django.forms import formset_factory
import re
from django.db.models import Sum
import django.db.models as models
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombre', 'marca', 'observacion', 'precio', 'cantidad', 'tipo', 'proveedor']

    def clean_precio(self):
        # Limpiar las comas solo si 'precio' es una cadena
        precio = self.cleaned_data['precio']
        if isinstance(precio, str):  # Asegurarse de que es una cadena
            precio = precio.replace(',', '')  # Eliminar las comas
            try:
                return int(precio)  # Asegurarse de que sea un número entero
            except ValueError:
                raise forms.ValidationError('El precio debe ser un número válido.')
        return precio

class ArticuloEditForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = [
            'nombre',
            'marca',
            'observacion',
            'precio',
            'cantidad',
            'tipo',
            'proveedor'
        ]
        labels = {
            'nombre': 'Nombre del Artículo',
            'marca': 'Marca',
            'observacion': 'Observación',
            'precio': 'Precio Unitario',
            'cantidad': 'Cantidad en Stock',
            'tipo': 'Tipo de Producto',
            'proveedor': 'Proveedor'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuración de widgets y atributos
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: Cuaderno cuadriculado',
            'maxlength': '40'
        })
        
        self.fields['marca'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: Norma',
            'maxlength': '30'
        })
        
        self.fields['observacion'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Opcional',
            'maxlength': '50'
        })
        
        self.fields['tipo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: Papelería',
            'maxlength': '30'
        })
        
        self.fields['proveedor'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ej: Distribuidora XYZ',
            'maxlength': '40'
        })
        
        self.fields['cantidad'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Máximo 10 dígitos',
            'maxlength': '13',
            'title': 'Ingrese solo números (hasta 10 dígitos)'
        })
        
        self.fields['precio'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Máximo 14 dígitos',
            'maxlength': '18',
            'title': 'Formato: 1000.00'
        })

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        
        # Expresión regular mejorada para aceptar más caracteres especiales
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s.,;:¡!¿?\"\'()\/\-–—°²³µ¼½¾×÷+=_@#%&*\[\]{}|\\<>°²³µ¼½¾g\/m²]*$', nombre):
            raise forms.ValidationError("Contiene caracteres inválidos.")
            
        if re.search(r'(.)\1{2,}', nombre):
            raise forms.ValidationError("No repita un mismo carácter más de 2 veces.")
            
        return nombre[:40].capitalize()

    def clean_marca(self):
        marca = self.cleaned_data.get('marca', '').strip()
        if len(marca) < 2:
            raise forms.ValidationError("La marca debe tener al menos 2 caracteres.")
            
        # Expresión regular más permisiva para marcas
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s.\-\/°²³]+$', marca):
            raise forms.ValidationError("Contiene caracteres inválidos en la marca.")
            
        return marca[:30].capitalize()

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        
        if cantidad is None:
            raise forms.ValidationError("Este campo es requerido.")
            
        # Manejar tanto string como números
        if isinstance(cantidad, str):
            cantidad_str = cantidad.strip().replace('.', '').replace(',', '')
        else:
            cantidad_str = str(cantidad).strip()
        
        if not cantidad_str.isdigit():
            raise forms.ValidationError("Ingrese solo números enteros positivos.")
        
        cantidad_int = int(cantidad_str)
        
        if cantidad_int < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
            
        if cantidad_int > 9999999999:  # Límite de 10 dígitos
            raise forms.ValidationError("Máximo permitido: 9,999,999,999")
            
        return cantidad_int

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        
        if precio is None:
            raise forms.ValidationError("Este campo es requerido.")
            
        # Manejar diferentes formatos de entrada
        if isinstance(precio, str):
            precio_str = precio.strip().replace(',', '')
        else:
            precio_str = str(precio).strip()
        
        try:
            precio_float = float(precio_str)
            precio_int = int(round(precio_float))
        except ValueError:
            raise forms.ValidationError("Ingrese un valor numérico válido.")
        
        if precio_float < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
            
        if precio_int > 99999999999999:  # Límite de 14 dígitos
            raise forms.ValidationError("Máximo permitido: 99,999,999,999,999")
            
        return precio_float  # Devolver como float para mantener decimales

    def clean_observacion(self):
        observacion = self.cleaned_data.get('observacion', '').strip()
        if not observacion:
            return ''
            
        if len(observacion) < 3:
            raise forms.ValidationError("Mínimo 3 caracteres si desea agregar una observación.")
            
        # Misma expresión regular mejorada que para nombre
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s.,;:¡!¿?\"\'()\/\-–—°²³µ¼½¾×÷+=_@#%&*\[\]{}|\\<>°²³µ¼½¾g\/m²]*$', observacion):
            raise forms.ValidationError("Contiene caracteres inválidos.")
            
        return observacion[:50].capitalize()

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo', '').strip()
        if not tipo:
            return ''
            
        if len(tipo) < 3:
            raise forms.ValidationError("Mínimo 3 caracteres si especifica el tipo.")
            
        # Expresión regular similar a marca
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s.\-\/°²³]+$', tipo):
            raise forms.ValidationError("Contiene caracteres inválidos en el tipo.")
            
        return tipo[:30].capitalize()

    def clean_proveedor(self):
        proveedor = self.cleaned_data.get('proveedor', '').strip()
        if len(proveedor) < 3:
            raise forms.ValidationError("El proveedor debe tener al menos 3 caracteres.")
            
        # Expresión regular similar a nombre pero un poco más restrictiva
        if not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúñÑ0-9\s.,\-&]+$', proveedor):
            raise forms.ValidationError("Contiene caracteres inválidos en el proveedor.")
            
        return proveedor[:40].capitalize()

class PedidoArticuloForm(forms.ModelForm):
    class Meta:
        model = PedidoArticulo
        fields = ['articulo', 'cantidad', 'area']  # incluye area
        widgets = {
            'articulo': forms.Select(),
            'cantidad': forms.NumberInput(attrs={'min': 1, 'step': '1'}),
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),  # área es solo lectura porque se asigna desde usuario
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí no es necesario configurar dinámicamente el campo 'tipo' ya que no lo estamos usando

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion
        fields = ['pedido', 'articulo', 'cantidad_devuelta', 'razon']

    def __init__(self, *args, **kwargs):
        pedido_id = kwargs.pop('pedido_id', None)
        super().__init__(*args, **kwargs)

        if pedido_id:
            articulos_ids = PedidoArticulo.objects.filter(pedido_id=pedido_id).values_list('articulo_id', flat=True)
            self.fields['articulo'].queryset = self.fields['articulo'].queryset.filter(id__in=articulos_ids)
            self.fields['pedido'].initial = pedido_id
            self.fields['pedido'].widget = forms.HiddenInput()