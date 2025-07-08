from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.core.mail import send_mail
from cde.forms import LoginForm
from libreria.forms import CustomUserForm
from django.core.mail import EmailMultiAlternatives
from libreria.models import CustomUser
from datetime import datetime

from cafeteria.models import Productos
from django.conf import settings
from django.core.mail import send_mail
from cde.models import PedidoCde, PedidoProductoCde
from cde.forms import PedidoProductoCdeForm, LoginForm
from django.db.models import Q
from django.core.paginator import Paginator
from cafeteria.models import Productos

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

def index_cde(request):
    return render(request, 'index_cde/index_cde.html')

def crear_pedido_cde(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cde:index_cde')},
        {'name': 'Crear pedido CDE', 'url': reverse('cde:crear_pedido_cde')},
    ]

    if request.method == 'POST':
        try:
            estado = 'Confirmado' if request.user.role == 'Administrador' else 'Pendiente'

            pedido_cde = PedidoCde.objects.create(
                registrado_por=request.user,
                estado=estado,
                fecha_estado=timezone.now() if estado == 'Confirmado' else None
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

                    if cantidad <= 0:
                        raise ValueError("Cantidad debe ser mayor a cero")

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

            # Notificar a administradores
            admin_users = CustomUser.objects.filter(role='Administrador', is_active=True)
            admin_emails = [admin.email for admin in admin_users if admin.email]

            if admin_emails:
                admin_url = request.build_absolute_uri(reverse('cde:mis_pedidos_cde'))
                context = {
                    'usuario': request.user,
                    'pedido': pedido_cde,
                    'admin_url': admin_url,
                    'company_name': 'Gestor CCD',
                    'productos': PedidoProductoCde.objects.filter(pedido=pedido_cde),
                    'fecha_pedido': pedido_cde.fecha_pedido.strftime('%d/%m/%Y %H:%M') if pedido_cde.fecha_pedido else '',
                }

                html_message = render_to_string('pedidos_cde/email_notificacion_pedido.html', context)

                text_message = f"""
Hola Administrador,

Se ha registrado un nuevo pedido en el sistema del Centro de Eventos:

Usuario: {request.user.username}
Rol: {request.user.get_role_display()}
Área: {getattr(request.user, 'area', 'No especificada')}
ID del Pedido: {pedido_cde.id}
Estado: {estado}
Fecha: {pedido_cde.fecha_pedido.strftime('%d/%m/%Y %H:%M') if pedido_cde.fecha_pedido else 'N/D'}

Detalle de productos:
{chr(10).join([f"- {pp.producto.nombre} x {pp.cantidad} (Evento: {pp.evento})" for pp in PedidoProductoCde.objects.filter(pedido=pedido_cde)])}

Revisar el pedido: {admin_url}

Este es un mensaje automático, por favor no respondas.
"""

                try:
                    subject = f"Nuevo pedido {'confirmado' if estado == 'Confirmado' else 'pendiente'} - ID: {pedido_cde.id}"
                    msg = EmailMultiAlternatives(
                        subject,
                        text_message,
                        settings.DEFAULT_FROM_EMAIL,
                        admin_emails
                    )
                    msg.attach_alternative(html_message, "text/html")
                    msg.send()
                except Exception as e:
                    print(f"Error enviando correo: {e}")
                    messages.warning(request, "El pedido fue creado, pero no se pudo enviar el correo de notificación.")

            messages.success(request, f"El pedido fue registrado correctamente con estado '{estado}'.")
            return redirect('cde:mis_pedidos_cde')

        except Exception as e:
            print(f"Error al crear pedido: {e}")
            messages.error(request, "Ocurrió un error al procesar tu pedido. Por favor intenta nuevamente.")
            return render(request, 'pedidos_cde/pedidos_cde.html', {
                'productos': Productos.objects.all(),
                'breadcrumbs': breadcrumbs
            })

    productos = Productos.objects.all()
    return render(request, 'pedidos_cde/pedidos_cde.html', {
        'productos': productos,
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



def listado_pedidos_cde(request):
    breadcrumbs = [
        {'name': 'Inicio CDE', 'url': '/index_cde'},
        {'name': 'Listado de pedidos cde', 'url': reverse('cde:lista_pedidos_cde')},
    ]

    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    pedidos = PedidoCde.objects.all().order_by('-fecha_pedido')

    if query:
        pedidos = pedidos.filter(
            Q(id__icontains=query) |
            Q(estado__icontains=query) |
            Q(fecha_pedido__icontains=query) |
            Q(fecha_estado__icontains=query) |
            Q(registrado_por__username__icontains=query) |
            Q(productos__producto__nombre__icontains=query) |
            Q(productos__cantidad__icontains=query) |
            Q(productos__area__icontains=query) |
            Q(productos__evento__icontains=query)
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

#pdf
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
def wrap_text_p(text, max_len=26
                ):
    parts = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for i in range(len(parts) - 1):
        parts[i] += '-'  # Agrega guion al final de todas menos la última
    return '\n'.join(parts)
def get_pedidos_filtrados_caf(request):
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    pedidos = PedidoCde.objects.all()

    if query:
        pedidos = pedidos.filter(
            Q(id__icontains=query) |
            Q(estado__icontains=query) |
            Q(fecha_pedido__icontains=query) |
            Q(fecha_estado__icontains=query) |
            Q(registrado_por__username__icontains=query) |
            Q(productos__producto__nombre__icontains=query) |
            Q(productos__cantidad__icontains=query) |
            Q(productos__area__icontains=query) |
            Q(productos__evento__icontains=query)
        ).distinct()

    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(fecha_pedido__range=[fecha_inicio, fecha_fin])

    return pedidos
def reporte_pedidos_pdf_cde(request):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    doc.title = "Listado de pedidos centro de eventos"
    doc.author = "CCD"
    doc.subject = "Listado de pedidos cde"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    # Título principal
    titulo = Paragraph("REPORTE DE PEDIDOS DE CENTRO DE EVENTOS", styles["Title"])
    elements.append(titulo)

    # Encabezado institucional
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

    # Datos del usuario
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

    # Obtener filtros
    q = request.GET.get('q', '')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Fetch pedidos with prefetch for productos and producto
    pedidos = PedidoCde.objects.prefetch_related('productos__producto').all()

    if q:
        pedidos = pedidos.filter(
            Q(id__icontains=q) |
            Q(estado__icontains=q) |
            Q(fecha_pedido__icontains=q) |
            Q(fecha_estado__icontains=q) |
            Q(registrado_por__username__icontains=q) |
            Q(productos__producto__nombre__icontains=q) |
            Q(productos__cantidad__icontains=q) |
            Q(productos__area__icontains=q) |
            Q(productos__evento__icontains=q)
        ).distinct()

    if fecha_inicio:
        try:
            pedidos = pedidos.filter(fecha_pedido__gte=datetime.strptime(fecha_inicio, '%Y-%m-%d'))
        except ValueError:
            pass  # Handle invalid date format gracefully
    if fecha_fin:
        try:
            pedidos = pedidos.filter(fecha_pedido__lte=datetime.strptime(fecha_fin, '%Y-%m-%d'))
        except ValueError:
            pass  # Handle invalid date format gracefully

    if not pedidos.exists():
        centered_style = ParagraphStyle(
            name="CenteredNormal",
            parent=styles["Normal"],
            alignment=TA_CENTER,
        )
        no_results = Paragraph("No se encontraron pedidos.", centered_style)
        elements.append(no_results)
    else:
        # Encabezado de la tabla
        data_pedidos = [["ID Pedido", "Fecha", "Estado", "Registrado Por", "Productos", "Área"]]

        # Filas de pedidos
        for pedido in pedidos:
            try:
                productos = pedido.productos.all()
                if productos.exists():
                    productos_raw = ", ".join([
                        f"{pa.producto.nombre} x {pa.cantidad}"
                        for pa in productos
                    ])
                    areas = set(pa.area for pa in productos if pa.area and pa.area != 'No establecido')
                    area_raw = ", ".join(areas) if areas else 'No establecido'
                else:
                    productos_raw = 'Sin productos'
                    area_raw = 'Sin área'

                data_pedidos.append([
                    wrap_text_p(str(pedido.id)),
                    wrap_text_p(pedido.fecha_pedido.strftime('%d-%m-%Y')),
                    wrap_text_p(pedido.get_estado_display()),
                    wrap_text_p(pedido.registrado_por.username if pedido.registrado_por else 'No definido'),
                    wrap_text_p(productos_raw),
                    wrap_text_p(area_raw)
                ])
            except Exception as e:
                print(f"Error processing pedido {pedido.id}: {str(e)}")
                data_pedidos.append([
                    wrap_text_p(str(pedido.id)),
                    wrap_text_p(pedido.fecha_pedido.strftime('%d-%m-%Y')),
                    wrap_text_p(pedido.get_estado_display()),
                    wrap_text_p(pedido.registrado_por.username if pedido.registrado_por else 'No definido'),
                    wrap_text_p('Error al cargar productos'),
                    wrap_text_p('Error al cargar área')
                ])

        # Crear la tabla de pedidos
        tabla_productos = Table(data_pedidos, colWidths=[60, 100, 100, 160, 200, 100])
        style_productos = TableStyle([
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
        tabla_productos.setStyle(style_productos)
        elements.append(tabla_productos)

    # Construir el PDF
    doc.build(elements, onFirstPage=draw_table_on_canvas, onLaterPages=draw_table_on_canvas)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Lista_de_pedidos_Gestor_CCD.pdf"'
    return response