from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from libreria.models import CustomUser
from .models import Productos, PedidoProducto, Pedido

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            
            if user is None:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
            
            if not user.is_active:
                raise forms.ValidationError("Tu cuenta está inactiva, contacta al administrador.")
        
        return cleaned_data

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['nombre', 'marca', 'presentacion', 'precio', 'cantidad', 'unidad_medida', 'proveedor']

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

class ProductosEditForm(forms.ModelForm):    
    class Meta:
        model = Productos
        fields = ['nombre', 'marca', 'presentacion', 'precio', 'cantidad', 'unidad_medida', 'proveedor']
    
    def __init__(self, *args,**kwargs):
        super(ProductosEditForm, self).__init__(*args, **kwargs)
        # Hace que los campos sean opcionales
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del producto'})
        self.fields['marca'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Marca del producto'})
        self.fields['presentacion'].widget.attrs.update({'class':'form-control', 'placeholder': 'Presentacion' })
        self.fields['precio'].widget.attrs.update({'class':'form-control', 'placeholder': 'Precio del  producto'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cantidad de producto'})
        self.fields['proveedor'].widget.attrs.update({'class':'form-control', 'placeholder': 'Proveedor'})
        self.fields['unidad_medida'].widget.attrs.update({'class': 'form-select'})
    
class PedidoProductoForm(forms.ModelForm):
    class Meta:
        model = PedidoProducto
        fields = ['producto', 'cantidad', 'area', 'lugar']  # incluye area
        widgets = {
            'producto': forms.Select(),
            'cantidad': forms.NumberInput(attrs={'min': 1, 'step': '1'}),
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),  # área es solo lectura porque se asigna desde usuario
            'lugar': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí no es necesario configurar dinámicamente el campo 'tipo' ya que no lo estamos usando