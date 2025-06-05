from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from cafeteria.forms import LoginForm , ProductoForm, ProductosEditForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.paginator import Paginator
import datetime
from .models import Productos
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

from .models import Productos  # Asegúrate de que la ruta sea correcta

def index_caf(request):
    return render(request, 'index_caf/index_caf.html')
# Create your views here.
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
        if form.is_valid():  # Si el formulario es válido
            producto = form.save(commit=False)  # Crear objeto pero no guardar aún
            producto.registrado_por = request.user  # Asignar el usuario que lo registra
            producto.save()  # Guardar el artículo
            return redirect('cafeteria:listar_productos')

  # Redirigir al listado de artículos
    else:
        form = ProductoForm()  # Crear un formulario vacío si es un GET
    
    return render(request, 'productos/crear_producto.html', {'form': form, 'breadcrumbs': breadcrumbs})

def listar_productos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': reverse('cafeteria:index_caf')},
         {'name': 'Crear producto', 'url': reverse('cafeteria:crear_producto')},
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
        'articulos': productos_page,
        'bajo_stock': bajo_stock_caf,
        'nombres_bajo_stock': nombres_bajo_stock,
    })