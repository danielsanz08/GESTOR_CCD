from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
from django.db import IntegrityError
from django.core.exceptions import ValidationError
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
from django.conf import settings
from django.contrib.auth import authenticate, login
from libreria.forms import CustomUserForm, CustomUserEditForm, CustomPasswordChangeForm
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
# Create your views here.
# Página de inicio
User = get_user_model()

def inicio(request):
    return render(request, 'index/index.html')


<<<<<<< HEAD
=======
=======
from django.http import HttpResponse
from openpyxl import Workbook
import os
from django.http import FileResponse, Http404
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
# Create your views here.
# Página de inicio
User = get_user_model()
def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')
def error_404_view(request, exception):
    return render(request, 'acceso_denegado.html', status=404)
def timeouterror(request):
    try:
        # Simulación de una operación que puede causar un TimeoutError
        # Aquí va tu lógica real, como una conexión a red, base de datos externa, etc.
        raise TimeoutError("Error de tiempo de espera")  # Simulación

        # Si no ocurre error, puedes devolver otro template si lo deseas
        return render(request, 'exito.html')

    except TimeoutError:
        # Solo captura TimeoutError y redirige a lan_error.html
        return render(request, 'lan_error.html')
    
def inicio(request):
    return render(request, 'index/index.html')

def manual_usuario_view(request):
    pdf_path = os.path.join(settings.BASE_DIR, 'libreria', 'static', 'manual','manual_usuario_papeleria.pdf')
    try:
        return FileResponse(open(pdf_path, 'rb'),
    content_type='application/pdf')
    except FileNotFoundError:
        raise Http404("Manual no encontrado")
    
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
def crear_usuario(request):
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
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
<<<<<<< HEAD
=======
=======
                role = user.role

                # Validación para administradores
                if role == 'Administrador':
                    admin_count = CustomUser.objects.filter(
                        role='Administrador',
                        is_active=True
                    ).count()

                    limit = 1
                    if admin_count >= limit:
                        messages.error(
                            request,
                            "Límite de administradores alcanzado. Solo puede haber un administrador activo en el sistema."
                        )
                        return redirect('libreria:crear_usuario')

                    # Asignar permisos a administradores
                    user.acceso_pap = True
                    user.acceso_caf = True
                    user.acceso_cde = True
                else:
                    # Restringir permisos para empleados
                    user.acceso_pap = False
                    user.acceso_caf = False
                    user.acceso_cde = False

                user.save()

                # Notificación a administradores
                admin_emails = CustomUser.objects.filter(
                    role='Administrador',
                    is_active=True
                ).exclude(pk=user.pk).values_list('email', flat=True)

                cargo = request.POST.get("cargo", "").strip()
                email_nuevo = user.email

                if admin_emails:
                    subject = "Nuevo usuario registrado en Gestor CCD"
                    message = (
                        f"Detalles del nuevo usuario:\n\n"
                        f"• Nombre de usuario: {user.username}\n"
                        f"• Rol: {role}\n"
                        f"• Cargo: {cargo}\n"
                        f"• Email: {email_nuevo}\n\n"
                        f"Permisos asignados:\n"
                        f"• Papelería: {'Sí' if user.acceso_pap else 'No'}\n"
                        f"• Cafetería: {'Sí' if user.acceso_caf else 'No'}\n"
                        f"• Centro de Eventos: {'Sí' if user.acceso_cde else 'No'}\n\n"
                        f"Este usuario requiere su aprobación para acceder al sistema.\n\n"
                        f"Saludos cordiales,\n"
                        f"Equipo de Gestor CCD"
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
                    )
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            list(admin_emails),
                            fail_silently=False,
                        )
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
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
<<<<<<< HEAD
=======
=======
                    except Exception as e:
                        messages.warning(request, "El usuario se creó correctamente, pero no se pudo enviar la notificación a los administradores.")

                messages.success(request, f"Usuario '{user.username}' registrado exitosamente.")
                return redirect('libreria:inicio')

            except IntegrityError:
                messages.error(request, "Error: El nombre de usuario o correo electrónico ya existe en el sistema.")
            except ValidationError as e:
                messages.error(request, f"Error de validación: {', '.join(e.messages)}")
            except Exception as e:
                messages.error(request, f"Error inesperado al crear el usuario: {str(e)}")
        else:
            # Mensajes de error específicos por campo
            for field, errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields else field
                
                if 'username' in field:
                    for error in errors:
                        if 'unique' in error:
                            messages.error(request, "Este nombre de usuario ya está en uso. Por favor elija otro.")
                        else:
                            messages.error(request, f"Nombre de usuario: {error}")
                
                elif 'email' in field:
                    for error in errors:
                        if 'unique' in error:
                            messages.error(request, "Este correo electrónico ya está registrado.")
                        elif 'invalid' in error:
                            messages.error(request, "Ingrese una dirección de correo electrónico válida.")
                        else:
                            messages.error(request, f"Correo electrónico: {error}")
                
                elif 'password' in field:
                    for error in errors:
                        if 'too short' in error.lower():
                            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
                        elif 'too common' in error.lower():
                            messages.error(request, "La contraseña es demasiado común o insegura.")
                        else:
                            messages.error(request, f"Contraseña: {error}")
                
                else:
                    for error in errors:
                        messages.error(request, f"{field_label}: {error}")
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
    else:
        form = CustomUserForm()

    return render(request, 'usuario/crear_usuario.html', {
        'form': form,
        'admin_exists': admin_exists,
        'breadcrumbs': breadcrumbs
    })

def ver_usuario(request, user_id):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Ver usuario', 'url': reverse('libreria:ver_usuario', kwargs={'user_id': user_id})},
    ]
    usuario = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'usuario/ver_perfil.html', {'usuario': usuario, 'breadcrumbs': breadcrumbs})

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)

def editar_usuario(request, user_id):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Ver usuario', 'url': reverse('libreria:ver_usuario', kwargs={'user_id': user_id})},
        {'name': 'Editar usuario', 'url': reverse('libreria:editar_usuario', kwargs={'user_id': user_id})},
    ]
    usuario = get_object_or_404(CustomUser, id=user_id)
<<<<<<< HEAD
=======
=======
from django.urls import NoReverseMatch
@login_required(login_url='/acceso_denegado/')
def editar_usuario(request, user_id):
    usuario = get_object_or_404(CustomUser, id=user_id)

    try:
        ver_usuario_url = reverse('libreria:ver_usuario', kwargs={'user_id': user_id})
    except NoReverseMatch:
        ver_usuario_url = '#'
        messages.warning(request, "No se pudo generar el enlace a 'Ver usuario'.")

    try:
        editar_usuario_url = reverse('libreria:editar_usuario', kwargs={'user_id': user_id})
    except NoReverseMatch:
        editar_usuario_url = '#'
        messages.warning(request, "No se pudo generar el enlace a 'Editar usuario'.")

    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Ver usuario', 'url': ver_usuario_url},
        {'name': 'Editar usuario', 'url': editar_usuario_url},
    ]
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            return redirect('libreria:lista_usuarios')

=======
<<<<<<< HEAD
            return redirect('libreria:lista_usuarios')

=======
            messages.success(request, "Usuario actualizado correctamente.")
            logout(request)
            return redirect('libreria:inicio')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
    else:
        form = CustomUserEditForm(instance=usuario)

    return render(request, 'usuario/editar_usuario.html', {
        'form': form,
        'usuario': usuario,
        'breadcrumbs': breadcrumbs
    })
<<<<<<< HEAD


=======
<<<<<<< HEAD


=======
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
def lista_usuarios(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Listado de usuarios', 'url': '/lista_usuarios'},
    ]
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
    query = request.GET.get('q', '').strip()
    usuarios_lista = CustomUser.objects.filter(module='papeleria')  # Ordenar por ID

    if query:
        usuarios_lista = usuarios_lista.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query) |
            Q(cargo__icontains=query) |
            Q(is_active__icontains=query)
        )

    paginator = Paginator(usuarios_lista, 5)  # Muestra 10 usuarios por página
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)

    return render(request, 'usuario/lista_usuarios.html', {'usuarios': usuarios, 'breadcrumbs': breadcrumbs})


def cambiar_estado_usuario(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = 'is_active' in request.POST
        user.save()
        return redirect(reverse("libreria:lista_usuarios"))  # Redirige a la página de login

<<<<<<< HEAD
=======
=======
    q = request.GET.get('q', '')
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    fecha_inicio = None
    fecha_fin = None

    usuarios = CustomUser.objects.all()

    # Filtrado por texto
    if q:
        usuarios = usuarios.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(role__icontains=q) |
            Q(area__icontains=q) |
            Q(cargo__icontains=q)
        )

    # Filtrado por fecha
    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            usuarios = usuarios.filter(fecha_registro__gte=fecha_inicio)
        except ValueError:
            usuarios = CustomUser.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            usuarios = usuarios.filter(fecha_registro__lte=fecha_fin)
        except ValueError:
            usuarios = CustomUser.objects.none()

    # Procesar actualización de permisos si es POST
    if request.method == 'POST' and 'actualizar_permisos' in request.POST:
        usuario_id = request.POST.get('usuario_id')
        try:
            usuario = CustomUser.objects.get(id=usuario_id)
            if usuario.role != 'Administrador':  # Solo actualizar si no es admin
                usuario.acceso_pap = 'acceso_pap' in request.POST
                usuario.acceso_caf = 'acceso_caf' in request.POST
                usuario.acceso_cde = 'acceso_cde' in request.POST
                usuario.save()
                messages.success(request, f"Permisos de {usuario.username} actualizados correctamente.")
            else:
                messages.info(request, "Los administradores tienen todos los permisos por defecto.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
        return redirect('libreria:lista_usuarios')

    # Paginación
    paginator = Paginator(usuarios, 4)
    page = request.GET.get('page')
    usuarios = paginator.get_page(page)

    return render(request, 'usuario/lista_usuarios.html', {
        'usuarios': usuarios,
        'breadcrumbs': breadcrumbs
    })
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import CustomUser

@login_required
def cambiar_estado_usuario(request, user_id):
    if request.method == 'POST':
        usuario = get_object_or_404(CustomUser, id=user_id)
        estado_anterior = usuario.is_active
        nuevo_estado = 'is_active' in request.POST

        # Evita que el usuario se desactive a sí mismo
        if request.user.id == usuario.id and not nuevo_estado:
            messages.error(request, "Error: No puedes desactivar tu propio usuario mientras estás autenticado.")
        elif estado_anterior != nuevo_estado:
            usuario.is_active = nuevo_estado
            usuario.save()

            if nuevo_estado:
                messages.success(request, f"Éxito: El usuario '{usuario.username}' ha sido activado correctamente.")
            else:
                messages.error(request, f"Advertencia: El usuario '{usuario.username}' ha sido desactivado.")
        else:
            messages.error(request, f"Información: El estado del usuario '{usuario.username}' no cambió.")

    return redirect(reverse("libreria:lista_usuarios"))
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
def cambiar_contraseña(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Cambiar Contraseña', 'url': reverse('libreria:cambiar_contraseña')},
    ]
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('libreria:inicio')  # Redirige después de cambiar la contraseña
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'usuario/cambiar_contraseña.html', {'form': form, 'breadcrumbs': breadcrumbs})
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.conf import settings

# Obtener el modelo de usuario personalizado
User = get_user_model()

>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse("libreria:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)

            subject = "Restablecer tu contraseña"
            message = render_to_string("password_reset_email.html", {"reset_link": reset_link})

            # Aquí NO capturamos errores de red
            send_mail(subject, message, "noreply@tuweb.com", [user.email])

            return redirect(reverse("libreria:password_reset_done") + "?sent=true")

        except User.DoesNotExist:
            return redirect(reverse("libreria:password_reset_done") + "?sent=false")

    return render(request, "password_reset.html")


def password_reset_done(request):
    return render(request, "password_reset_done.html")

<<<<<<< HEAD
=======
=======
            
            # Contexto para el template del email
            context = {
                'user': user,
                'reset_link': reset_link,
                'site_name': 'Gestor CCD',
                'company_name': 'Gestor CCD',
            }
            
            subject = "Restablecer tu contraseña - Gestor CCD"
            html_message = render_to_string("password_reset_email.html", context)
            
            # Crear mensaje de texto plano como respaldo
            text_message = f"""
Hola {user.username},

Recibimos una solicitud para restablecer la contraseña de tu cuenta en Gestor CCD.

Para restablecer tu contraseña, copia y pega el siguiente enlace en tu navegador:
{reset_link}

Si no solicitaste este cambio, puedes ignorar este mensaje.

El enlace será válido por 24 horas.

Saludos,
El equipo de Gestor CCD
            """
            
            try:
                # Crear email con HTML y texto plano
                msg = EmailMultiAlternatives(
                    subject,
                    text_message,  # Mensaje de texto plano
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
                msg.attach_alternative(html_message, "text/html")  # Versión HTML
                msg.send()
                
                return redirect(reverse("libreria:password_reset_done") + "?sent=true")
            except Exception as e:
                # Log del error pero no mostrar detalles al usuario por seguridad
                print(f"Error enviando email: {e}")
                return redirect(reverse("libreria:password_reset_done") + "?sent=error")
                
        except User.DoesNotExist:
            # Por seguridad, redirigir igual pero con parámetro diferente
            return redirect(reverse("libreria:password_reset_done") + "?sent=notfound")
    
    return render(request, "password_reset.html")

def password_reset_done(request):
    sent_status = request.GET.get('sent', 'unknown')
    context = {
        'sent_status': sent_status,
        'show_success': sent_status == 'true',
        'show_error': sent_status == 'error',
        'show_not_found': sent_status == 'notfound'
    }
    return render(request, "password_reset_done.html", context)
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
    
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse("libreria:password_reset_complete"))
        else:
            form = SetPasswordForm(user)
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
        return render(request, "password_reset_confirm.html", {"form": form})
    else:
        return render(request, "password_reset_confirm.html", {"error": "El enlace no es válido o ha expirado."})


def password_reset_complete(request):
    return render(request, "password_reset_complete.html")

<<<<<<< HEAD
=======
=======
        return render(request, "password_reset_confirm.html", {
            "form": form, 
            "user": user,
            "valid_link": True
        })
    else:
        return render(request, "password_reset_confirm.html", {
            "error": "El enlace no es válido o ha expirado.",
            "valid_link": False
        })

def password_reset_complete(request):
    return render(request, "password_reset_complete.html")
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
#VALIDAR INFORMACION

def validar_datos(request):
    email = request.GET.get('email', None)
    
    errores = {}

    # Validar correo electrónico
    if email and CustomUser.objects.filter(email=email).exists():
        errores['email'] = 'El email ya está en uso.'

    # Retornar los errores (si los hay) o una respuesta de validación exitosa
    return JsonResponse(errores if errores else {'valid': True})

def validate_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        password = data.get('password')
        user = request.user
        valid = user.check_password(password)
        return JsonResponse({'valid': valid})
    return JsonResponse({'valid': False})

from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.contrib.staticfiles import finders
from papeleria.models import Articulo
def draw_table_on_canvas(canvas, doc):
    # Marca de agua
    watermark_path = finders.find('imagen/LOGO.png')
    if watermark_path:
        canvas.saveState()
        canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.3))
        canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.3))
        canvas.drawImage(watermark_path,
                         x=(doc.pagesize[0] - 600) / 2,
                         y=(doc.pagesize[1] - 600) / 2,
                         width=600, height=600, mask='auto')
        canvas.restoreState()

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b659cb3 (Sexagésimo commit)
def reporte_usuario_pdf(request):
    buffer = BytesIO()

    # Crear documento
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)

    # Metadatos
    doc.title = "Listado de usuarios CCD"
    doc.author = "CCD"
    doc.subject = "Listado de usuarios"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    # Título
    titulo = Paragraph("REPORTE DE USUARIOS", styles["Title"])
    elements.append(titulo)

    # Encabezado empresa
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    encabezado_data = [
        ["GESTOR CCD", "Lista de usuarios", "Correo: gestorccd@gmail.com", f"Fecha: {fecha_actual}"],
        ["Cámara de comercio de Duitama", "Nit: 123456789", "(Correo de la camara)", "Teléfono: (tel. camara)"],
    ]
    tabla_encabezado = Table(encabezado_data, colWidths=[180, 180, 180, 180])
    estilo_encabezado = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabla_encabezado.setStyle(estilo_encabezado)
    elements.append(tabla_encabezado)

    # Tabla usuario
    usuario = request.user
    data_usuario = [["Usuario:", "Email:", "Rol:", "Cargo:"]]
    data_usuario.append([
        usuario.username,
        usuario.email,
        getattr(usuario, 'role', 'No definido'),
        getattr(usuario, 'cargo', 'No definido'),
    ])
    table_usuario = Table(data_usuario, colWidths=[180, 180, 180, 180])
    style_usuario = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table_usuario.setStyle(style_usuario)
    elements.append(table_usuario)

    # Tabla artículos
    data_usuarios = [["ID", "Usuario", "Rol", "correo", "Cargo", "Área", "Estado"]]
    estado = "Activo" if usuario.is_active else "Inactivo"
    for usuario in CustomUser.objects.all():
        data_usuarios.append([
            usuario.id,
            usuario.username,
            usuario.role,
            usuario.email,
            usuario.cargo,
            usuario.area,
             "Activo" if usuario.is_active else "Inactivo"
        ])
    tabla_articulos = Table(data_usuarios, colWidths=[20, 100, 80, 180, 220, 80, 40])
    style_articulos = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabla_articulos.setStyle(style_articulos)
    elements.append(tabla_articulos)

    # Construir documento con marca de agua
    doc.build(elements, onFirstPage=draw_table_on_canvas, onLaterPages=draw_table_on_canvas)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Lista de usuarios Gestor CCD.pdf"'
    return response

from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl import Workbook
from openpyxl.drawing.image import Image

def reporte_usuario_excel(request):
    # Crear un nuevo libro de trabajo de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Artículos"

    # Ajustar el ancho de las columnas A y B para que quepa el logo
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 25

    # Ajustar la altura de la fila 1 para el logo
    ws.row_dimensions[1].height = 90

    # Estilo de borde delgado
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
# Agregar el logo
    logo_path = finders.find('imagen/logo.png')  # Ajustar ruta según ubicación real
    if logo_path:
        img = Image(logo_path)
        img.height = 80
        img.width = 200
        ws.add_image(img, 'A1')
        ws.merge_cells('A1:B1')

    # Aplicar bordes a las celdas del logo (A1 y B1)
    for col in ['A', 'B']:
        cell = ws[f'{col}1']
        cell.border = border


    # Título principal
    ws.merge_cells('C1:G1')
    ws['C1'] = "GESTOR CCD"
    ws['C1'].font = Font(size=24, bold=True)
    ws['C1'].alignment = Alignment(horizontal='center', vertical='center')

    # Aplicar borde a las celdas del título
    for col in ['C', 'D', 'E', 'F', 'G']:
        cell = ws[f'{col}1']
        cell.border = border

   # Subtítulo
    ws.merge_cells('A2:G2')
    ws['A2'] = "Listado de usuarios Gestor CCD"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

# Aplicar borde a las celdas del subtítulo
    for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        cell = ws[f'{col}2']
        cell.border = border

    # Encabezados de la tabla
    headers = ["ID", "Usuario", "Rol", "Correo", "Cargo", "Área", "Estado"]
    ws.append(headers)

    # Estilo para los encabezados
    header_fill = PatternFill(start_color="FF0056B3", end_color="FF0056B3", fill_type="solid")
    for cell in ws[3]:
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

    # Agregar datos de los usuarios
    for usuario in CustomUser.objects.all():
        estado = "Activo" if usuario.is_active else "Inactivo"
        ws.append([
            usuario.id,
            usuario.username,
            usuario.role,
            usuario.email,
            usuario.cargo,
            usuario.area,
            estado
        ])

    # Ajustar el ancho de las columnas
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 40
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 40
    ws.column_dimensions['E'].width = 50
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 15


    # Aplicar estilo a las filas de datos
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row, min_col=1, max_col=7):
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

    # Ajustar la altura de las filas del encabezado y subtítulo
    ws.row_dimensions[1].height = 60
    ws.row_dimensions[2].height = 30

    # Preparar la respuesta para descargar el archivo
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Lista de usuarios Gestor CCD.xlsx"'

    # Guardar el archivo en la respuesta
    wb.save(response)
    return response
<<<<<<< HEAD
=======
=======

>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
#GRAFICAS
def graficas_usuarios_activos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Estadísticas', 'url': reverse('libreria:index_estadistica')}, 
        {'name': 'Gráfico de usuarios activos', 'url': reverse('libreria:graficas_usuarios_activos')}, 
    ]
    
    activos = CustomUser.objects.filter(is_active=True).count()
    inactivos = CustomUser.objects.filter(is_active=False).count()

    nombres = ['Activos', 'Inactivos']
    cantidades = [activos, inactivos]

    return render(request, 'estadisticas/grafica_usuarios.html', {
        'nombres': nombres,
        'cantidades': cantidades,
        'breadcrumbs': breadcrumbs
<<<<<<< HEAD
    })
=======
<<<<<<< HEAD
    })
=======
    })



def sesion_expirada(request):
    return render(request, 'sesion_expirada.html')

#PDF Y XSLS DE BAJO STOCK
def obtener_usuarios(request):
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    usuarios = CustomUser.objects.all()  # mejor nombrar 'usuarios' para que coincida

    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query) |
            Q(area__icontains=query) |
            Q(cargo__icontains=query)
        )

    if fecha_inicio and fecha_fin:
        usuarios = usuarios.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    return usuarios

def wrap_text(text, max_len=20):
    parts = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for i in range(len(parts) - 1):
        parts[i] += '-'  # Agrega guion al final de todas menos la última
    return '\n'.join(parts)

def reporte_usuario_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)

    doc.title = "Listado de usuarios CCD"
    doc.author = "Gestor CCD"
    doc.subject = "Listado de usuarios CCD"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    # Título
    titulo = Paragraph("REPORTE DE USUARIOS CCD ", styles["Title"])
    elements.append(titulo)

    # Encabezado empresa
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    encabezado_data = [
        ["GESTOR CCD", "Lista de artículos", "Correo:", f"Fecha: {fecha_actual}"],
        ["Cámara de comercio de Duitama", "Nit: 123456789", "contacto@gestorccd.com", "Teléfono: (123) 456-7890"],
    ]
    tabla_encabezado = Table(encabezado_data, colWidths=[180, 180, 180, 180])
    estilo_encabezado = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabla_encabezado.setStyle(estilo_encabezado)
    elements.append(tabla_encabezado)

    # Tabla usuario
    usuario = request.user
    data_usuario = [["Usuario", "Email", "Rol", "Cargo"]]

    if usuario.is_authenticated:
        data_usuario.append([
            usuario.username,
            usuario.email,
            getattr(usuario, 'role', 'No definido'),
            getattr(usuario, 'cargo', 'No definido'),
        ])
    else:
        data_usuario.append(["Invitado", "-", "-", "-"])

    table_usuario = Table(data_usuario, colWidths=[180, 180, 180, 180])
    style_usuario = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table_usuario.setStyle(style_usuario)
    elements.append(table_usuario)

    # Aquí asumo que tienes una función para obtener usuarios filtrados
    usuarios_filtrados = obtener_usuarios(request)

    # Tabla artículos (usuarios)
    data_usuarios = [["ID", "Usuario", "Rol", "Correo", "Cargo", "Área", "Estado"]]
    for u in usuarios_filtrados:
        data_usuarios.append([
            wrap_text(str(u.id)),
            wrap_text(u.username),
            wrap_text(u.role),
            wrap_text(u.email),
            wrap_text(u.cargo),
            wrap_text(getattr(u, 'area', 'No definido')),
            wrap_text("Activo" if u.is_active else "Inactivo")
])

    tabla_articulos = Table(data_usuarios, colWidths=[30, 100, 100, 160, 160, 100
                                                      , 70])
    style_articulos = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabla_articulos.setStyle(style_articulos)
    elements.append(tabla_articulos)

    # Construir el PDF
    doc.build(elements, onFirstPage=draw_table_on_canvas, onLaterPages=draw_table_on_canvas)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Listado de usuarios CCD.pdf"'
    return response

def reporte_usuario_excel(request):
    # Obtener artículos filtrados usando la función reutilizable
    usuarios = obtener_usuarios(request)

    # Crear archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Listado de Artículos CCD"

    # Configuración columnas y filas (sin logo)
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 30
    ws.column_dimensions['F'].width = 20
    ws.column_dimensions['G'].width = 15

    ws.row_dimensions[1].height = 60
    ws.row_dimensions[2].height = 30

    # Título principal y subtítulo
    ws.merge_cells('A1:G1')
    ws['A1'] = "GESTOR CCD"
    ws['A1'].font = Font(size=24, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A2:G2')
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    ws['A2'] = f"Listado de Artículos - {fecha_actual}"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    # Encabezados
    headers = ["ID", "Usuario", "Rol", "Correo", "Cargo", "Área", "Estado"]
    ws.append(headers)

    header_fill = PatternFill(start_color="FF0056B3", end_color="FF0056B3", fill_type="solid")
    for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        cell = ws[f"{col}3"]
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Agregar datos
    for usuario in usuarios:
        estado = "Activo" if usuario.is_active else "Inactivo"
        ws.append([
            usuario.id,
            wrap_text(usuario.username),
            wrap_text(usuario.role),
            wrap_text(usuario.email),
            wrap_text(usuario.cargo),
            wrap_text(usuario.area),
            wrap_text(estado)
        ])

    # Aplicar bordes y alineación a filas 1 y 2 (título y subtítulo)
    for row in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col=7):
        for cell in row:
            cell.border = border
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Aplicar bordes y alineación a filas 3 hasta el final (encabezados y datos)
    for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=1, max_col=7):
        for cell in row:
            cell.border = border
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Filtros en la fila 3 (encabezados)
    ws.auto_filter.ref = "A3:G3"

    # Preparar respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Listado de usuarios CCD.xlsx"'
    wb.save(response)
    return response
>>>>>>> 3797db6 (Sexagésimo tercer commit)
>>>>>>> b659cb3 (Sexagésimo commit)
