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
<<<<<<< HEAD
        fields = ['username', 'email', 'role', 'cargo', 'module', 'password', 'area']
=======
<<<<<<< HEAD
        fields = ['username', 'email', 'role', 'cargo', 'module', 'password', 'area']
=======
        fields = ['username', 'email', 'role', 'cargo', 'password', 'area', 'acceso_pap', 'acceso_caf', 'acceso_cde']
        widgets = {
            'acceso_pap': forms.HiddenInput(),
            'acceso_caf': forms.HiddenInput(),
            'acceso_cde': forms.HiddenInput(),
        }
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        
        # Agregar clases CSS a los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['cargo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cargo'})
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
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
        return user
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'cargo', 'module', 'area']
<<<<<<< HEAD
=======
=======
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
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
        # Hace que los campos sean opcionales
        for field in self.fields:
            self.fields[field].required = False

        # Agrega clases CSS
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['module'].widget.attrs.update({'class': 'form-select'})
<<<<<<< HEAD
=======
=======
        for field in self.fields:
            self.fields[field].required = False

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
        self.fields['cargo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cargo'})
        self.fields['area'].widget.attrs.update({'class': 'form-select'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
<<<<<<< HEAD
        if not email:
            return self.instance.email  # Mantiene el valor anterior si no se cambia
        return email
=======
<<<<<<< HEAD
        if not email:
            return self.instance.email  # Mantiene el valor anterior si no se cambia
        return email
=======
        return email or self.instance.email  # Mantiene el valor anterior si no se cambia

    def clean_role(self):
        new_role = self.cleaned_data.get('role')
        if new_role == 'Administrador':
            admin_exists = CustomUser.objects.filter(role='Administrador', is_active=True).exclude(id=self.instance.id).exists()
            if admin_exists:
                raise forms.ValidationError("Ya existe un usuario con rol de Administrador. No puedes asignar este rol.")
        return new_role

>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)

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