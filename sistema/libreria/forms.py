from django import forms
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'cargo', 'password', 'area', 'acceso_pap', 'acceso_caf', 'acceso_cde']
        widgets = {
            'acceso_pap': forms.HiddenInput(),
            'acceso_caf': forms.HiddenInput(),
            'acceso_cde': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        
        # Agregar clases CSS a los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['cargo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cargo'})
        self.fields['area'].widget.attrs.update({'class': 'form-select'})

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hashea la contraseña antes de guardar
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'cargo', 'area']

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)

        # Hace que los campos sean opcionales
        for field in self.fields:
            self.fields[field].required = False

        # Agrega clases CSS
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['cargo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cargo'})
        self.fields['area'].widget.attrs.update({'class': 'form-select'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return self.instance.email  # Mantiene el valor anterior si no se cambia
        return email

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        # Puedes personalizar los atributos de los campos si quieres
        self.fields['old_password'].widget.attrs.update({'class': 'form-input0'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control1'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control2'})

    def clean(self):
        # Corrige el error tipográfico: 'clena' -> 'clean'
        cleaned_data = super().clean()  # Llamada correcta a 'clean'
        
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("Las contraseñas no coinciden")

        if old_password and new_password1 and old_password == new_password1:
            raise ValidationError("La nueva contraseña no puede ser igual a la anterior")

        return cleaned_data