from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
)

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        if not email:
            raise ValueError('El usuario debe tener un email válido')
        
        email = self.normalize_email(email)
        username = username.strip()

        user = self.model(username=username, email=email)
        user.set_password(password)  # ¡Importante! Guarda contraseña hasheada
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        # Puedes asignar acceso total aquí si quieres
        user.acceso_pap = True
        user.acceso_caf = True
        user.acceso_cde = True
        user.save(using=self._db)
        return user
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Empleado', 'Empleado'),
    ]
    AREA = [
        ('Administrativa', 'Administrativa'),
        ('Registros públicos', 'Registros públicos'),
        ('Gestión empresarial', 'Gestión empresarial'),
        ('Competitividad', 'Competitividad'),
        ('Presidencia', 'Presidencia'),
        ('Financiera', 'Financiera'),
    ]
    username = models.CharField(max_length=100, unique=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(max_length=13, choices=ROLES, default='Empleado')
    area = models.CharField(max_length=30, choices=AREA, default='Administrativa')
    cargo = models.CharField(max_length=50, default='No establecido')
    fecha_registro = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Campos para los permisos de módulos
    acceso_pap = models.BooleanField(default=False, verbose_name='Acceso Papelería')
    acceso_caf = models.BooleanField(default=False, verbose_name='Acceso Cafetería')
    acceso_cde = models.BooleanField(default=False, verbose_name='Acceso Centro de Eventos')

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Si el usuario es administrador, se le asignan todos los permisos
        if self.role == 'Administrador':
            self.acceso_pap = True
            self.acceso_caf = True
            self.acceso_cde = True
        super().save(*args, **kwargs)