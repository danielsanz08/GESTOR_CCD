from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from cafeteria.forms import LoginForm , ProductoForm, ProductosEditForm, PedidoProductoForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.paginator import Paginator
import datetime
from django.core.mail import send_mail
from django.conf import settings
from libreria.models import CustomUser
from .models import Productos, PedidoProducto, Pedido
from django.shortcuts import get_object_or_404, redirect
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.contrib.staticfiles import finders
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Productos  # Asegúrate de que la ruta sea correcta
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
@login_required(login_url='/acceso_denegado/')
def index_caf(request):
    es_cafeteria = True
    mostrar_alerta = True  # Nueva variable

    context = {
        'es_cafeteria': es_cafeteria,
        'mostrar_alerta': mostrar_alerta,
    }

    return render(request, 'index_caf/index_caf.html', context)

# Create your views here.
def ver_usuario_caf(request, id):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_caf'},
        {'name': 'Ver usuario', 'url': reverse('cafeteria:ver_usuario_caf', kwargs={'id': id})},
    ]
    usuario = get_object_or_404(CustomUser, id=id)
    return render(request, 'usuario_caf/ver_perfil_caf.html', {'usuario': usuario, 'breadcrumbs': breadcrumbs})


def login_cafeteria(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active and getattr(user, 'acceso_caf', False):
                login(request, user)
                return redirect('cafeteria:index_caf')
            else:
                messages.error(request, "No tienes permiso para acceder a este módulo.")
        else:
            messages.error(request, "Credenciales inválidas.")

    return render(request, 'login_caf/login_caf.html')
def crear_producto(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
        {'name': 'Crear producto', 'url': reverse('cafeteria:crear_producto')},
    ]

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.registrado_por = request.user
            producto.save()
            messages.success(request, '¡Producto creado exitosamente!')
            return redirect('cafeteria:listar_productos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductoForm()

    return render(request, 'productos/crear_producto.html', {
        'form': form,
        'breadcrumbs': breadcrumbs
    })
def listar_productos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
         {'name': 'Listado de cafeteria y aseo', 'url': reverse('cafeteria:listar_productos')},
    ]

    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    productos = Productos.objects.select_related('registrado_por').all()

    # Búsqueda por texto
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(presentacion__icontains=query) |
            Q(unidad_medida__icontains=query) |
            Q(precio__icontains=query) |
            Q(proveedor__icontains=query) |
            Q(cantidad__icontains=query) |
            Q(registrado_por__username__icontains=query)
        )

    # Filtrado por rango de fechas
    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            productos = productos.filter(fecha_registro__gte=fecha_inicio)
        except ValueError:
            # Manejo del error: ignorar filtro o asignar un queryset vacío
            productos = Productos.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            productos = productos.filter(fecha_registro__lte=fecha_fin)
        except ValueError:
            productos = Productos.objects.none()

    # Paginación
    paginator = Paginator(productos, 4)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    return render (request, 'productos/listar_productos.html', {'productos': productos,
        'breadcrumbs': breadcrumbs})
def eliminar_producto(request, id):
    producto = get_object_or_404(Productos, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('cafeteria:listar_productos')
    # En caso de que sea GET u otro método, redirige o muestra algo
    return redirect('cafeteria:listar_productos')
# CERRAR SESIÓN

def editar_producto(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    if request.method== 'POST':
        form = ProductosEditForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('cafeteria:listar_productos')
    else:
            form = ProductosEditForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})
@login_required(login_url='/acceso_denegado/')
def logout_caf(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(reverse('libreria:inicio'))
User = get_user_model()
def wrap_text(text, max_len=20):
    parts = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for i in range(len(parts) - 1):
        parts[i] += '-'  # Agrega guion al final de todas menos la última
    return '\n'.join(parts)
#PDF DE PRODUCTOS
def obtener_productos(request):
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    productos = Productos.objects.all()  

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(presentacion__icontains=query) |
            Q(unidad_medida__icontains=query) |
            Q(precio__icontains=query) |
            Q(proveedor__icontains=query) |
            Q(cantidad__icontains=query) |
            Q(registrado_por__username__icontains=query)
        )

    if fecha_inicio and fecha_fin:
        productos = productos.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    return productos
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
def reporte_productos_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)

    doc.title = "Listado de productos de cafeteria CCD"
    doc.author = "Gestor CCD"
    doc.subject = "Listado de productos de cafeteria CCD"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    # Título
    titulo = Paragraph("REPORTE DE CCAFETERIA CCD ", styles["Title"])
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
    usuarios_filtrados = obtener_productos(request)

    # Tabla artículos (usuarios)
    data_productos = [["ID", "Nombre", "Marca", "Precio", "Cantidad","Unidad de medida","Proveedor", "Presentación"]]
    for producto in usuarios_filtrados:
        data_productos.append([
            wrap_text(str(producto.id)),
            wrap_text(producto.nombre),
            wrap_text(producto.marca),
            wrap_text("{:,}".format(producto.precio)),
            wrap_text(str(producto.cantidad)),
            wrap_text(str(producto.unidad_medida)),
            wrap_text(producto.proveedor),
            wrap_text(producto.presentacion),
])

    tabla_productos = Table(data_productos, colWidths=[30, 100, 100, 70, 100, 110, 105])
    style_productos = TableStyle([
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
    tabla_productos.setStyle(style_productos)
    elements.append(tabla_productos)

    # Construir el PDF
    doc.build(elements, onFirstPage=draw_table_on_canvas, onLaterPages=draw_table_on_canvas)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Listado de cafeteria CCD.pdf"'
    return response

def reporte_productos_excel(request):
    # Parámetros de búsqueda
    q = request.GET.get('q', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    marca = request.GET.get('marca', '').strip()

    # Queryset base
    productos = Productos.objects.all()

    # Aplicar filtros
    if q:
        productos = productos.filter(nombre__icontains=q)
    if fecha_inicio:
        try:
            productos = productos.filter(fecha_registro__gte=datetime.strptime(fecha_inicio, '%Y-%m-%d'))
        except ValueError:
            pass
    if fecha_fin:
        try:
            productos = productos.filter(fecha_registro__lte=datetime.strptime(fecha_fin, '%Y-%m-%d'))
        except ValueError:
            pass
    if marca:
        productos = productos.filter(marca__icontains=marca)

    # Crear Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Listado de cafeteria CCD"

    # Borde común
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Tamaño columnas
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 20
    ws.column_dimensions['E'].width = 20
    ws.column_dimensions['F'].width = 22
    ws.column_dimensions['G'].width = 23
    ws.column_dimensions['H'].width = 23

    ws.row_dimensions[1].height = 60
    ws.row_dimensions[2].height = 30

    # Título
    ws.merge_cells('A1:H1')
    ws['A1'] = "GESTOR CCD"
    ws['A1'].font = Font(size=24, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    # Subtítulo
    ws.merge_cells('A2:H2')
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    ws['A2'] = f"Listado de cafeteria {fecha_actual}"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    # Borde A1:H2
    for row in [1, 2]:
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            ws[f"{col}{row}"].border = border
            ws[f"{col}{row}"].alignment = Alignment(horizontal='center', vertical='center')

    # Encabezados
    headers = ["ID", "Nombre", "Marca", "Precio", "Cantidad", "Unidad de medida", "Proveedor", "Presentación"]
    ws.append(headers)
    header_fill = PatternFill(start_color="FF0056B3", end_color="FF0056B3", fill_type="solid")

    # Estilo encabezados fila 3
    for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        cell = ws[f"{col}3"]
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

    # Aplicar filtro a A3:H3
    ws.auto_filter.ref = "A3:H3"

    # Agregar datos
    for producto in productos:
        ws.append([
            wrap_text(str(producto.id)),
            wrap_text(producto.nombre),
            wrap_text(producto.marca),
            wrap_text("${:,}".format(producto.precio)),
            wrap_text(str(producto.cantidad)),
            wrap_text(str(producto.unidad_medida)),
            wrap_text(producto.proveedor),
            wrap_text(producto.presentacion),
        ])

    # Estilo de celdas de datos (A4:Hn con bordes, centrado y wrap_text)
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row, min_col=1, max_col=8):
        for cell in row:
            cell.border = border
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Exportar
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Listado de cafeteria CCD.xlsx"'
    wb.save(response)
    return response

def lista_stock_bajo(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
        {'name': 'Bajo Stock', 'url': reverse('cafeteria:lista_bajo_stock')},
    ]
    query = request.GET.get('q', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtrar solo artículos con cantidad menor a 10
    productos_bajo_stock = Productos.objects.filter(cantidad__lt=10)

    # Filtro por búsqueda de texto
    if query:
        productos_bajo_stock = productos_bajo_stock.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(presentacion__icontains=query) |
            Q(unidad_medida__icontains=query) |
            Q(precio__icontains=query) |
            Q(proveedor__icontains=query) |
            Q(cantidad__icontains=query) |
            Q(registrado_por__username__icontains=query)
        )

    # Filtro por rango de fechas en fecha_registro
    if fecha_inicio:
        productos_bajo_stock = productos_bajo_stock.filter(fecha_registro__gte=fecha_inicio)
    if fecha_fin:
        productos_bajo_stock = productos_bajo_stock.filter(fecha_registro__lte=fecha_fin)

    bajo_stock_caf = productos_bajo_stock.exists()
    nombres_bajo_stock = [art.nombre for art in productos_bajo_stock]

    paginator = Paginator(productos_bajo_stock, 4)
    page_number = request.GET.get('page')
    productos_page = paginator.get_page(page_number)

    return render(request, 'productos/bajo_stock.html', {
        'productos': productos_page,
        'bajo_stock': bajo_stock_caf,
        'nombres_bajo_stock': nombres_bajo_stock,
        'breadcrumbs': breadcrumbs
    })

def crear_pedido_caf(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
        {'name': 'Crear pedido', 'url': reverse('cafeteria:crear_pedido_caf')},
    ]
    
    if request.method == 'POST':
        try:
            estado = 'Confirmado' if request.user.role == 'Administrador' else 'Pendiente'

            productos_ids = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            lugares = request.POST.getlist('lugar')

            area_usuario = getattr(request.user, 'area', 'No establecido')

            # Validar stock antes de crear el pedido
            for producto_id, cantidad in zip(productos_ids, cantidades):
                if not producto_id or not cantidad:
                    continue
                try:
                    producto_id = int(producto_id)
                    cantidad = int(cantidad)
                    producto = Productos.objects.get(id=producto_id)
                    if estado == 'Confirmado' and producto.cantidad < cantidad:
                        messages.error(request, f"No hay suficiente stock para el producto: {producto.nombre}. Stock disponible: {producto.cantidad}.")
                        return redirect('cafeteria:crear_pedido_caf')
                except (ValueError, Productos.DoesNotExist):
                    messages.error(request, "Producto inválido o cantidad no válida.")
                    return redirect('cafeteria:crear_pedido_caf')

            # Crear el pedido principal
            pedido = Pedido.objects.create(
                registrado_por=request.user,
                estado=estado,
            )

            for producto_id, cantidad, lugar in zip(productos_ids, cantidades, lugares):
                try:
                    if not producto_id or not cantidad or not lugar:
                        continue

                    producto_id = int(producto_id)
                    cantidad = int(cantidad)

                    producto = Productos.objects.get(id=producto_id)

                    PedidoProducto.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        lugar=lugar,
                        area=area_usuario,
                    )

                    if estado == 'Confirmado':
                        producto.cantidad -= cantidad
                        producto.save()

                except (ValueError, Productos.DoesNotExist) as e:
                    print(f"Error al procesar producto: {e}")
                    continue

            # Notificar a administradores
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
                        f"ID del pedido: {pedido.id}\n"
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

            messages.success(request, f"Pedido creado exitosamente con estado: {estado}.")
            return redirect('cafeteria:mis_pedidos')

        except Exception as e:
            print(f"Error al crear pedido: {e}")
            messages.error(request, "Ocurrió un error al procesar tu pedido. Por favor intenta nuevamente.")
            return redirect('cafeteria:crear_pedido_caf')

    productos = Productos.objects.all()
    return render(request, 'pedidos/pedidos_caf.html', {
        'productos': productos,
        'breadcrumbs': breadcrumbs
    })
@login_required
def mis_pedidos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
        {'name': 'Mis pedidos', 'url': reverse('cafeteria:mis_pedidos')},
    ]
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtra los PEDIDOS (no los productos) por el usuario autenticado
    pedidos = Pedido.objects.filter(registrado_por=request.user).order_by('-fecha_pedido')

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
            pedidos = Pedido.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)
        except ValueError:
            pedidos = Pedido.objects.none()

    paginator = Paginator(pedidos, 4)
    page_number = request.GET.get('page')
    pedidos_page = paginator.get_page(page_number)

    return render(request, 'pedidos/mis_pedidos_caf.html', {
        'pedidos': pedidos_page, 'breadcrumbs': breadcrumbs
    })
@csrf_exempt
@require_POST
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['Confirmado', 'Cancelado']:
            pedido.estado = nuevo_estado
            pedido.save()
    return redirect('cafeteria:pedidos_pendientes')

def pedidos_pendientes(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
        {'name': 'Pedidos pendientes', 'url': reverse('cafeteria:pedidos_pendientes')},
    ]
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtrar solo pedidos pendientes
    pedidos = Pedido.objects.filter(estado='Pendiente').order_by('-fecha_pedido')

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

    return render(request, 'pedidos/confirmar_pedido_caf.html', {
        'pedidos': pedidos_page,
        'breadcrumbs': breadcrumbs
    })
def mis_pedidos_pendientes(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
         {'name': ' Mis Pedidos pendientes', 'url': reverse('cafeteria:mis_pedidos_pendientes')},
        
    ]
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtrar solo pedidos pendientes
    pedidos = Pedido.objects.filter(estado='pendiente', registrado_por=request.user).order_by('-fecha_pedido')

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
            pedidos = Pedido.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)
        except ValueError:
            pedidos = Pedido.objects.none()

    paginator = Paginator(pedidos, 4)
    page_number = request.GET.get('page')
    pedidos_page = paginator.get_page(page_number)

    return render(request, 'pedidos/mis_pedidos_pendientes.html', {
        'pedidos': pedidos_page,'breadcrumbs': breadcrumbs
    })
def listado_pedidos_caf(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_caf'},
        {'name': 'Listado de pedidos', 'url': reverse('cafeteria:lista_pedidos_caf')},
    ]

    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtrar solo pedidos del usuario actual
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')

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
            pedidos = Pedido.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)
        except ValueError:
            pedidos = Pedido.objects.none()

    paginator = Paginator(pedidos, 4)
    page_number = request.GET.get('page')
    pedidos_page = paginator.get_page(page_number)

    return render(request, 'pedidos/lista_pedidos_caf.html', {
        'pedidos': pedidos_page,
        'breadcrumbs': breadcrumbs
    })


def get_pedidos_filtrados_caf(request):
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    pedidos = Pedido.objects.all()

    if query:
        pedidos = pedidos.filter(
            Q(id__icontains=query) |
            Q(estado__icontains=query) |
            Q(registrado_por__username__icontains=query) |
            Q(productos__producto__nombre__icontains=query)
        ).distinct()

    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(fecha_pedido__range=[fecha_inicio, fecha_fin])

    return pedidos
def wrap_text_p(text, max_len=26
                ):
    parts = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for i in range(len(parts) - 1):
        parts[i] += '-'  # Agrega guion al final de todas menos la última
    return '\n'.join(parts)

def reporte_pedidos_pdf_caf(request):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    doc.title = "Listado de pedidos de cafeteria y aseo CCD"
    doc.author = "CCD"
    doc.subject = "Listado de pedidos"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    # Título principal
    titulo = Paragraph("REPORTE DE PEDIDOS DE CAFETERIA Y ASEO", styles["Title"])
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
    pedidos = Pedido.objects.prefetch_related('productos__producto').all()

    if q:
        pedidos = pedidos.filter(
            Q(id__icontains=q) |
            Q(productos__producto__nombre__icontains=q) |
            Q(registrado_por__username__icontains=q) |
            Q(estado__icontains=q)
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

    # Encabezado de la tabla
    data_pedidos = [["ID Pedido", "Fecha", "Estado", "Registrado Por", "Productos", "Área"]]

    # Filas de pedidos
    for pedido in pedidos:
        try:
            # Fetch all products for the order
            productos = pedido.productos.all()
            if productos.exists():
                productos_raw = ", ".join([
                    f"{pa.producto.nombre} x {pa.cantidad}"  # Removed pa.tipo as it might not exist
                    for pa in productos
                ])
                # Get unique areas from all products, excluding None or empty
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
            # Log any errors for debugging
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
def reporte_pedidos_excel_caf(request):
    # Obtener todos los pedidos ordenados por fecha descendente
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')

    # Crear libro Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Pedidos CCD"

    # Ajustar ancho de columnas
    columnas_anchos = {
        'A': 10,   # ID
        'B': 15,   # Fecha
        'C': 15,   # Estado
        'D': 25,   # Registrado por
        'E': 50,   # Artículos
        'F': 30    # Áreas
    }
    for col, width in columnas_anchos.items():
        ws.column_dimensions[col].width = width

    # Ajustar altura de título y subtítulo
    ws.row_dimensions[1].height = 50
    ws.row_dimensions[2].height = 30

    # Título principal
    ws.merge_cells('A1:F1')
    ws['A1'] = "GESTOR CCD"
    ws['A1'].font = Font(size=24, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    # Subtítulo
    ws.merge_cells('A2:F2')
    ws['A2'] = "Listado de Pedidos"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    # Bordes para los títulos A1:F1 y A2:F2
    
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
        )
    for row in ws.iter_rows(min_row=1, max_row=2, min_col=1, max_col=6):
        for cell in row:
            cell.border = thin_border

    # Encabezados de tabla
    headers = ['ID', 'Fecha', 'Estado', 'Registrado Por', 'Productos', 'Áreas']
    ws.append(headers)

    # Estilo para encabezados
    header_fill = PatternFill(start_color="FF0056B3", end_color="FF0056B3", fill_type="solid")
    for cell in ws[3]:
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Aplicar filtro
    ws.auto_filter.ref = "A3:F3"

    # Estilo de bordes
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # Agregar datos de los pedidos
    for pedido in pedidos:
        # Artículos en una sola línea, separados por comas
        productos_raw = ", ".join([
            f"{pa.producto.nombre} x {pa.cantidad} ({pa.tipo})"
            for pa in pedido.productos.all()
        ]) or 'Sin artículos'

        # Áreas únicas, separadas por comas
        areas_raw = ", ".join(set([
            str(pa.area) for pa in pedido.productos.all()
        ])) or 'Sin área'

        # Usuario
        usuario = pedido.registrado_por.username if pedido.registrado_por else 'No definido'

        # Añadir fila
        ws.append([
            pedido.id,
            pedido.fecha_pedido.strftime('%Y-%m-%d'),
            pedido.get_estado_display(),
            usuario,
            productos_raw,
            areas_raw,
        ])

    # Aplicar bordes y alineación a todas las celdas de A3:F...
    for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=1, max_col=6):
        for i, cell in enumerate(row, start=1):
            cell.border = thin_border
            cell.alignment = Alignment(
                horizontal='center',
                vertical='center',
                wrap_text=True if i in [4, 5, 6] else False  # Wrap en usuario, artículos, áreas
        )


    # Ajustar altura de filas para mejor legibilidad
    for i in range(4, ws.max_row + 1):
        ws.row_dimensions[i].height = 60

    # Generar y devolver el archivo Excel como descarga
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Reporte_pedidos.xlsx"'
    wb.save(response)
    return response
