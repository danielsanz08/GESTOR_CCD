from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from cde.forms import LoginForm
from libreria.forms import CustomUserForm
from libreria.models import CustomUser
from cafeteria.models import Productos
from django.conf import settings
from django.core.mail import send_mail
from cde.models import PedidoCde, PedidoProductoCde
from django.db.models import Q
from django.core.paginator import Paginator
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
# Ejemplo para el login de papelería
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
def error_404_view(request, exception):
    return render(request, 'acceso_denegado.html', status=404)
def login_cde(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active and getattr(user, 'acceso_cde', False):
                login(request, user)
                return redirect('cde:index_cde')
            else:
                messages.error(request, "No tienes permiso para acceder a este módulo.")
        else:
            messages.error(request, "Credenciales inválidas.")

    return render(request, 'login_cde/login_cde.html')

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

def ver_usuario_cde(request, id):
    breadcrumbs = [
        {'name': 'Inicio CDE', 'url': '/index_cde'},
        {'name': 'Ver usuario CDE', 'url': reverse('cde:ver_usuario_cde', kwargs={'id': id})},
    ]
    usuario = get_object_or_404(CustomUser, id=id)
    return render(request, 'usuario_cde/ver_perfil_cde.html', {'usuario': usuario, 'breadcrumbs': breadcrumbs})


def index_cde(request):
    breadcrumbs = [
        {'name': 'Inicio CDE', 'url': '/index_cde'},
    ]
    return render(request, 'index_cde/index_cde.html',{'breadcrumbs': breadcrumbs})

def crear_pedido_cde(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cde:index_cde')},
        {'name': 'Crear pedido cde', 'url': reverse('cde:crear_pedido_cde')},
    ]
    
    if request.method == 'POST':
        try:
            estado = 'Confirmado' if request.user.role == 'Administrador' else 'Pendiente'

            pedido_cde = PedidoCde.objects.create(
                registrado_por=request.user,
                estado=estado,
            )

            productos_ids = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            eventos = request.POST.getlist('evento')

            area_usuario = getattr(request.user, 'area', 'No establecido')

            for producto_id, cantidad, evento in zip(productos_ids, cantidades, eventos):
                try:
                    if not producto_id or not cantidad or not evento:
                        continue

                    producto_id = int(producto_id)
                    cantidad = int(cantidad)

                    producto = Productos.objects.get(id=producto_id)

                    if estado == 'Confirmado' and producto.cantidad < cantidad:
                        pedido_cde.delete()
                        messages.error(request, f"No hay suficiente stock para el producto: {producto.nombre} (disponible: {producto.cantidad}, solicitado: {cantidad})")
                        return redirect('cde:crear_pedido_cde')

                    PedidoProductoCde.objects.create(
                        pedido=pedido_cde,
                        producto=producto,
                        cantidad=cantidad,
                        evento=evento,
                        area=area_usuario,
                    )

                    if estado == 'Confirmado':
                        producto.cantidad -= cantidad
                        producto.save()

                except (ValueError, Productos.DoesNotExist) as e:
                    print(f"Error al procesar producto: {e}")
                    continue

            if request.user.role in ['Empleado', 'Administrador']:
                admin_users = User.objects.filter(role='Administrador', is_active=True)
                admin_emails = [admin.email for admin in admin_users if admin.email]

                if admin_emails:
                    subject = "Nuevo pedido registrado por un usuario"
                    message = (
                        f"Hola querido administrador,\n\n"
                        f"Desde el módulo de Centro de eventos te informamos que el usuario '{request.user.username}' "
                        f"ha realizado un nuevo pedido.\n\n"
                        f"Información del pedido:\n"
                        f"Usuario: {request.user.username}\n"
                        f"Rol: {request.user.role}\n"
                        f"ID del pedido: {pedido_cde.id}\n"
                        f"Estado inicial del pedido: {estado}\n\n"
                        f"Por favor revisa y confirma el pedido si corresponde.\n\n"
                        f"Gracias por su atención.\n"
                        f"El equipo de Gestor CCD les desea un excelente día."
                    )
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            admin_emails,
                            fail_silently=False,
                        )
                    except TimeoutError:
                        messages.error(request, "El pedido fue creado, pero no se pudo enviar el correo de notificación (Timeout).")

            messages.success(request, f"El pedido fue registrado correctamente con estado '{estado}'.")
            return redirect('cde:mis_pedidos_pendientes_cde')

        except Exception as e:
            print(f"Error al crear pedido: {e}")
            messages.error(request, "Ocurrió un error al procesar tu pedido. Por favor intenta nuevamente.")
            return redirect('cde:crear_pedido_cde')

    productos = Productos.objects.all()
    return render(request, 'pedidos_cde/pedidos_cde.html', {
        'productos': productos,
        'breadcrumbs': breadcrumbs,
    })
@login_required
def mis_pedidos_cde(request):
    breadcrumbs = [
        {'name': 'Inicio CDE', 'url': '/index_cde'},
        {'name': 'Mis pedidos cde', 'url': reverse('cde:mis_pedidos_cde')},
    ]
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtra los PEDIDOS (no los productos) por el usuario autenticado
    pedidos = PedidoCde.objects.filter(registrado_por=request.user).order_by('-fecha_pedido')

    if query:
        pedidos = pedidos.filter(
            Q(registrado_por__username__icontains=query) |
            Q(estado__icontains=query) |
            Q(productos__area__icontains=query)  # Accede al área a través de la relación productos
        ).distinct()

    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__gte=fecha_inicio)
        except ValueError:
            pedidos = PedidoCde.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)
        except ValueError:
            pedidos = PedidoCde.objects.none()

    paginator = Paginator(pedidos, 4)
    page_number = request.GET.get('page')
    pedidos_page = paginator.get_page(page_number)

    return render(request, 'pedidos_cde/mis_pedidos_cde.html', {
        'pedidos': pedidos_page, 'breadcrumbs': breadcrumbs
    })
@csrf_exempt
@require_POST
def cambiar_estado_pedido_cde(request, pedido_id):
    pedido = get_object_or_404(PedidoCde, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')

        if nuevo_estado:
            if nuevo_estado == 'Confirmado':
                try:
                    with transaction.atomic():
                        productos_pedido = pedido.productos.select_related('producto').all()
                        productos_sin_stock = []

                        # Verificar stock disponible
                        for item in productos_pedido:
                            producto = item.producto
                            if producto.cantidad < item.cantidad:
                                productos_sin_stock.append(
                                    f"{producto.nombre} (Solicitados: {item.cantidad}, Disponibles: {producto.cantidad})"
                                )

                        if productos_sin_stock:
                            pedido.estado = 'Cancelado'
                            pedido.fecha_estado = timezone.now()
                            pedido.save()
                            messages.error(request, f"Pedido cancelado. Stock insuficiente: {', '.join(productos_sin_stock)}")
                            return redirect('cde:pedidos_pendientes')

                        # Descontar del stock
                        for item in productos_pedido:
                            producto = item.producto
                            producto.cantidad -= item.cantidad
                            producto.save()

                        pedido.estado = 'Confirmado'
                        pedido.fecha_estado = timezone.now()
                        pedido.save()
                        messages.success(request, 'Pedido confirmado correctamente.')

                except Exception as e:
                    messages.error(request, f'Error al confirmar el pedido: {str(e)}')
                    return redirect('cde:pedidos_pendientes')

            else:  # Cancelado u otro estado
                pedido.estado = nuevo_estado
                pedido.fecha_estado = timezone.now()
                pedido.save()
                messages.success(request, f'Estado actualizado a {nuevo_estado}.')

            # (Opcional) Enviar notificación al usuario
            if pedido.registrado_por and pedido.registrado_por.email:
                try:
                    send_mail(
                        f'Estado de tu pedido #{pedido.id} actualizado',
                        f'Tu pedido #{pedido.id} ha sido actualizado a {pedido.estado}.',
                        settings.DEFAULT_FROM_EMAIL,
                        [pedido.registrado_por.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Error enviando email: {str(e)}")

            return redirect('cde:pedidos_pendientes')

    messages.error(request, 'No se pudo actualizar el estado.')
    return redirect('cde:pedidos_pendientes')
def pedidos_pendientes_cde(request):
    breadcrumbs = [
        {'name': 'Inicio CDE', 'url': '/index_cde'},
        {'name': 'Pedidos pendientes cde', 'url': reverse('cde:pedidos_pendientes_cde')},
    ]
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtrar solo pedidos pendientes
    pedidos = PedidoCde.objects.filter(estado='Pendiente').order_by('-fecha_pedido')

    if query:
        pedidos = pedidos.filter(
            Q(registrado_por__username__icontains=query) |
            Q(estado__icontains=query) |
            Q(productos__producto__nombre__icontains=query) |  # Buscar en el nombre del producto
            Q(productos__area__icontains=query) |  # Buscar en el área del PedidoProducto
            Q(productos__lugar__icontains=query)   # Buscar en el lugar del PedidoProducto
        ).distinct()

    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__gte=fecha_inicio)
        except ValueError:
            pass  # No hacer nada si la fecha es inválida

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)
        except ValueError:
            pass  # No hacer nada si la fecha es inválida

    paginator = Paginator(pedidos, 4)
    page_number = request.GET.get('page')
    pedidos_page = paginator.get_page(page_number)

    return render(request, 'pedidos_cde/confirmar_pedido_cde.html', {
        'pedidos': pedidos_page,
        'breadcrumbs': breadcrumbs
    })

def mis_pedidos_pendientes_cde(request):
    breadcrumbs = [
        {'name': 'Inicio CDE', 'url': '/index_cde'},
         {'name': ' Mis Pedidos pendientes cde', 'url': reverse('cde:mis_pedidos_pendientes_cde')},
        
    ]
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtrar solo pedidos pendientes
    pedidos = PedidoCde.objects.filter(estado='pendiente', registrado_por=request.user).order_by('-fecha_pedido')

    if query:
        pedidos = pedidos.filter(
            Q(registrado_por__username__icontains=query) |
            Q(estado__icontains=query) |
            Q(articulos__area__icontains=query)
        ).distinct()

    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__gte=fecha_inicio)
        except ValueError:
            pedidos = PedidoCde.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)
        except ValueError:
            pedidos = PedidoCde.objects.none()

    paginator = Paginator(pedidos, 4)
    page_number = request.GET.get('page')
    pedidos_page = paginator.get_page(page_number)

    return render(request, 'pedidos_cde/mis_pedidos_pendientes_cde.html', {
        'pedidos': pedidos_page,'breadcrumbs': breadcrumbs
    })

def listado_pedidos_cde(request):
    breadcrumbs = [
        {'name': 'Inicio CDE', 'url': '/index_cde'},
        {'name': 'Listado de pedidos cde', 'url': reverse('cde:lista_pedidos_cde')},
    ]

    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtrar solo pedidos del usuario actual
    pedidos = PedidoCde.objects.all().order_by('-fecha_pedido')

    if query:
        pedidos = pedidos.filter(
            Q(registrado_por__username__icontains=query) |
            Q(estado__icontains=query) |
            Q(productos__area__icontains=query)
        ).distinct()

    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__gte=fecha_inicio)
        except ValueError:
            pedidos = PedidoCde.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)
        except ValueError:
            pedidos = PedidoCde.objects.none()

    paginator = Paginator(pedidos, 4)
    page_number = request.GET.get('page')
    pedidos_page = paginator.get_page(page_number)

    return render(request, 'pedidos_cde/lista_pedidos_cde.html', {
        'pedidos': pedidos_page,
        'breadcrumbs': breadcrumbs
    })
