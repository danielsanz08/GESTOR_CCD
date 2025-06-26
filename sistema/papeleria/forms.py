from django import forms
from papeleria.models import Articulo, PedidoArticulo
from django.forms import formset_factory
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
from django import forms
from papeleria.models import Articulo
from django import forms
from papeleria.models import Articulo

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadimos class y placeholder + maxlength en HTML
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre del artículo',
            'maxlength': '40'
        })
        self.fields['marca'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Marca del artículo',
            'maxlength': '30'
        })
        self.fields['observacion'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Observación',
            'maxlength': '30'
        })
        self.fields['precio'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Precio del artículo'
        })
        self.fields['cantidad'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Cantidad del artículo'
        })
        self.fields['tipo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tipo del artículo',
            'maxlength': '30'
        })
        self.fields['proveedor'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Proveedor',
            'maxlength': '40'
        })
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '') or ''
        return nombre[:40]  # Trunca a 40 caracteres
    
    def clean_marca(self):
        marca = self.cleaned_data.get('marca', '') or ''
        return marca[:30]  # Trunca a 30 caracteres
    
    def clean_observacion(self):
        observacion = self.cleaned_data.get('observacion', '') or ''
        return observacion[:30]  # Trunca a 30 caracteres
    
    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo', '') or ''
        return tipo[:30]  # Trunca a 30 caracteres
    
    def clean_proveedor(self):
        proveedor = self.cleaned_data.get('proveedor', '') or ''
        return proveedor[:40]  # Trunca a 40 caracteres
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
