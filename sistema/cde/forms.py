from django import forms
from django.contrib.auth import authenticate
<<<<<<< HEAD
from django.core.exceptions import ValidationError
from libreria.models import CustomUser
=======
<<<<<<< HEAD
from django.core.exceptions import ValidationError
from libreria.models import CustomUser
=======
from .models import PedidoProductoCde
from django.core.exceptions import ValidationError
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
    
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'cargo', 'module', 'password', 'area']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        
        # Agregar clases CSS a los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['cargo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cargo'})
        self.fields['module'].widget.attrs.update({'class': 'form-select'})
        self.fields['area'].widget.attrs.update({'class': 'form-select'})

        # Si el usuario ya existe, deshabilitar el campo 'module' (no puede cambiar su módulo)
        if self.instance.pk:
            self.fields['module'].widget.attrs['disabled'] = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("La contraseña es obligatoria.")
        return password

    def clean_module(self):
        """Si el usuario ya existe, evitar que se cambie el módulo."""
        module = self.cleaned_data.get('module')
        if self.instance.pk:  # Si el usuario ya está registrado
            return self.instance.module  # Mantener el módulo original
        return module

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encripta la contraseña

        if commit:
            user.save()
<<<<<<< HEAD
        return user
=======
        return user
=======

    
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
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
