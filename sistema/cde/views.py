from django.shortcuts import render
from cde.forms import LoginForm, CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from libreria.models import CustomUser
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def login_cde(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.module == 'Centro de eventos':  # Verifica que el usuario pertenece a CDE
                    login(request, user)
                    messages.success(request, "Sesión iniciada correctamente en CDE.")
                    return redirect('cde:index_cde')  # Redirige a la página de inicio de CDE
                else:
                    messages.error(request, "No tienes acceso a este módulo.")
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'login_cde/login_cde.html', {'form': form})

def logout_cde(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(reverse('libreria:inicio'))
User = get_user_model()

def index_cde(request):
    return render(request, 'index_cde/index_cde.html')

def crear_usuario_cde(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Crear usuario', 'url': '/crear_usuario'},
    ]
    admin_exists = CustomUser.objects.exists()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                module = user.module
                role = user.role

                # Verificar el número de administradores en cada módulo
                if role == 'Administrador':
                    admin_count = CustomUser.objects.filter(
                        role='Administrador', module=module, is_active=True
                    ).count()

                    limits = {'Papeleria': 3, 'Cafeteria': 2, 'Centro de eventos': 1}
                    if module in limits and admin_count >= limits[module]:
                        messages.error(
                            request,
                            f"Ya existen {limits[module]} administradores en el módulo {module}."
                        )
                        return redirect('crear_usuario')

                # Guardar el usuario
                user.save()

                # Enviar correo a los administradores del mismo módulo
                admin_emails = CustomUser.objects.filter(
                    role='Administrador', module=module, is_active=True
                ).values_list('email', flat=True)

                cargo = request.POST.get("cargo", "").strip()
                email = user.email  # Se obtiene directamente del objeto user

                if admin_emails:
                    subject = f"Nuevo usuario creado en {module}"
                    message = (
                        f"Hola querido usuario,\n\n"
                        f"Por parte de Gestor CCD, te informamos que se ha creado un nuevo usuario.\n\n"
                        f"Información:\n\n"
                        f"Nombre: {user.username}\n"
                        f"Rol: {role}\n"
                        f"Módulo: {module}\n"
                        f"Cargo: {cargo}\n"
                        f"Email: {email}\n\n"
                        f"En caso de ser infiltrado, por favor te invitamos a desactivarlo.\n\n"
                        f"Muchas gracias por su atención.\n"
                        f"El director de Gestor CCD te desea un feliz día."
                    )
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            list(admin_emails),
                            fail_silently=False,
                        )
                        print("Correo enviado correctamente.")
                    except Exception as e:
                        messages.error(request, f"No se pudo enviar el correo: {e}")

                messages.success(request, f"Usuario '{user.username}' creado exitosamente.")
                return redirect('libreria:inicio')

            except Exception as e:
                messages.error(request, f"Hubo un error al crear el usuario: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserForm()

    return render(request, 'usuario_cde/crear_usuario_cde.html', {
        'form': form,
        'admin_exists': admin_exists,
        'breadcrumbs': breadcrumbs
    })
