from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
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

            # Crear el pedido principal
            pedido_cde = PedidoCde.objects.create(
                registrado_por=request.user,
                estado=estado,
            )

            productos_ids = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            eventos = request.POST.getlist('evento')  # Cambié el nombre a plural para reflejar que es una lista

            area_usuario = getattr(request.user, 'area', 'No establecido')

            for producto_id, cantidad, evento in zip(productos_ids, cantidades, eventos):
                try:
                    if not producto_id or not cantidad or not evento:
                        continue

                    # Validar que el ID y cantidad sean numéricos
                    producto_id = int(producto_id)
                    cantidad = int(cantidad)

                    producto = Productos.objects.get(id=producto_id)

                    if estado == 'Confirmado' and producto.cantidad < cantidad:
                        pedido_cde.delete()
                        return render(request, 'pedidos_cde/pedidos_cde.html', {
                            'productos': Productos.objects.all(),
                            'error': f"No hay suficiente stock para el producto: {producto.nombre}",
                            'breadcrumbs': breadcrumbs
                        })

                    # Crear el producto del pedido - CORRECCIÓN PRINCIPAL AQUÍ
                    PedidoProductoCde.objects.create(
                        pedido=pedido_cde,  # El campo en el modelo es 'pedido', no 'pedidoCde'
                        producto=producto,
                        cantidad=cantidad,
                        evento=evento,  # Usamos la variable evento de la iteración
                        area=area_usuario,
                    )

                    if estado == 'Confirmado':
                        producto.cantidad -= cantidad
                        producto.save()

                except (ValueError, Productos.DoesNotExist) as e:
                    print(f"Error al procesar producto: {e}")
                    continue

            # Notificar a administradores para pedidos de Empleados y Administradores
            if request.user.role in ['Empleado', 'Administrador']:
                admin_users = User.objects.filter(role='Administrador', is_active=True)
                admin_emails = [admin.email for admin in admin_users if admin.email]

                if admin_emails:
                    subject = "Nuevo pedido registrado por un usuario"
                    message = (
                        f"Hola querido administrador,\n\n"
                        f"Desde el módulo de Papelería te informamos que el usuario '{request.user.username}' "
                        f"ha realizado un nuevo pedido.\n\n"
                        f"Información del pedido:\n"
                        f"Usuario: {request.user.username}\n"
                        f"Rol: {request.user.role}\n"
                        f"ID del pedido: {pedido_cde.id}\n"
                        f"Estado inicial del pedido: {estado}\n\n"
                        f"Por favor revisa y confirma el pedido si corresponde.\n"
                        "\n"
                        f"Gracias por su atención.\n"
                        f"El equipo de Gestor CCD les desea un excelente día."
                    )
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        admin_emails,
                        fail_silently=False,
                    )

            # Redirigir a la vista de pedidos pendientes para todos los roles
            return redirect('cde:mis_pedidos_pendientes_cde')

        except Exception as e:
            print(f"Error al crear pedido: {e}")
            return render(request, 'pedidos_cde/pedidos_cde.html', {
                'productos': Productos.objects.all(),
                'error': "Ocurrió un error al procesar tu pedido. Por favor intenta nuevamente.",
                'breadcrumbs': breadcrumbs
            })

    productos = Productos.objects.all()
    return render(request, 'pedidos_cde/pedidos_cde.html', {
        'productos': productos,
        'breadcrumbs': breadcrumbs
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
        if nuevo_estado in ['Confirmado', 'Cancelado']:
            pedido.estado = nuevo_estado
            pedido.save()
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