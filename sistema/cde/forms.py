from django import forms
from django.contrib.auth import authenticate
from .models import PedidoProductoCde
from django.core.exceptions import ValidationError
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

    
class PedidoProductoCdeForm(forms.ModelForm):
    class Meta:
        model = PedidoProductoCde
        fields = ['producto', 'cantidad', 'area', 'evento']  # incluye area
        widgets = {
            'producto': forms.Select(),
            'cantidad': forms.NumberInput(attrs={'min': 1, 'step': '1'}),
            'area': forms.TextInput(attrs={'readonly': 'readonly'}),  # área es solo lectura porque se asigna desde usuario
            'evento': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí no es necesario configurar dinámicamente el campo 'tipo' ya que no lo estamos usando
