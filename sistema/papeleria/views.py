from django.shortcuts import render
from papeleria.models import Articulo, PedidoArticulo, Pedido
from libreria.models import CustomUser
from papeleria.forms import LoginForm, ArticuloForm, ArticuloEditForm, PedidoArticuloForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import get_template
from django.utils.timezone import now
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()
def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')

@never_cache
@login_required(login_url='/acceso_denegado/')
def index_pap(request):
    breadcrumbs = [{'name': 'Inicio', 'url': '/index_pap'}]
    return render(request, 'index_pap/index_pap.html', {'breadcrumbs': breadcrumbs})

# Vista de login (login_papeleria)

def login_papeleria(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.module == 'Papeleria':  # Verifica que el usuario pertenece a Papelería
                    login(request, user)
                    messages.success(request, "Sesión iniciada correctamente en Papelería.")
                    return redirect('papeleria:index_pap')  # Redirige a la página de inicio de Papelería
                else:
                    messages.error(request, "No tienes acceso a este módulo.")
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'login_pap/login_pap.html', {'form': form})

# Vista para cerrar sesión
@never_cache
@login_required(login_url='/acceso_denegado/')
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(reverse('libreria:inicio'))

@login_required
def crear_articulo(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
         {'name': 'Crear artículo', 'url': reverse('papeleria:crear_articulo')},
        
    ]
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():  # Si el formulario es válido
            articulo = form.save(commit=False)  # Crear objeto pero no guardar aún
            articulo.registrado_por = request.user  # Asignar el usuario que lo registra
            articulo.save()  # Guardar el artículo
            return redirect('papeleria:listar_articulo')  # Redirigir al listado de artículos
    else:
        form = ArticuloForm()  # Crear un formulario vacío si es un GET
    
    return render(request, 'articulo/crear_articulo.html', {'form': form, 'breadcrumbs': breadcrumbs})
def editar_articulo(request, articulo_id):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
         {'name': 'Listar artículos', 'url': reverse('papeleria:listar_articulo')}, 
         {'name': 'Editar artículo', 'url': reverse('papeleria:editar_articulo', kwargs={'articulo_id': articulo_id})},
        
    ]
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method== 'POST':
        form = ArticuloEditForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('papeleria:listar_articulo')
    else:
            form = ArticuloEditForm(instance=articulo)
    return render(request, 'articulo/editar_articulo.html', {'form': form, 'articulo': articulo, 'breadcrumbs': breadcrumbs})


def listar_articulo(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Listar artículos', 'url': reverse('papeleria:listar_articulo')},
    ]

    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    articulos = Articulo.objects.select_related('registrado_por').all()

    # Búsqueda por texto
    if query:
        articulos = articulos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(observacion__icontains=query) |
            Q(tipo__icontains=query) |
            Q(precio__icontains=query) |
            Q(proveedor__icontains=query) |
            Q(cantidad__icontains=query) |
            Q(registrado_por__username__icontains=query)
        )

    # Filtrado por rango de fechas
    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            articulos = articulos.filter(fecha_registro__gte=fecha_inicio)
        except ValueError:
            # Manejo del error: ignorar filtro o asignar un queryset vacío
            articulos = Articulo.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            articulos = articulos.filter(fecha_registro__lte=fecha_fin)
        except ValueError:
            articulos = Articulo.objects.none()

    # Paginación
    paginator = Paginator(articulos, 4)
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)

    return render(request, 'articulo/listar_articulo.html', {
        'articulos': articulos,
        'breadcrumbs': breadcrumbs
    })
def buscar_articulo(request):
    query = request.GET.get('q', '').strip()
    if query:
        articulos = Articulo.objects.filter(nombre__icontains=query).values(
            'id', 'nombre', 'marca', 'observacion', 'precio', 'registrado_por', 'fecha_formateada', 'proveedor'
        )
        return JsonResponse(list(articulos), safe=False)
    return JsonResponse([], safe=False)

def eliminar_articulo(request, id):
    articulo = Articulo.objects.get(id=id)
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, "Artículo eliminado correctamente.")
    return redirect('papeleria:listar_articulo')


def validar_datos(request):
    email = request.GET.get('email', None)
    
    errores = {}

    # Validar correo electrónico
    if email and CustomUser.objects. filter(email=email).exists():
        errores['email'] = 'El email ya está en uso.'

    # Retornar los errores (si los hay) o una respuesta de validación exitosa
    return JsonResponse(errores if errores else {'valid': True})
def verificar_nombre_articulo(request):
    nombre = request.GET.get('nombre', '')
    existe = Articulo.objects.filter(nombre=nombre).exists()
    return JsonResponse({'existe': existe})
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
def get_articulos_filtrados(request):
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    articulos = Articulo.objects.select_related('registrado_por').all()

    if query:
        articulos = articulos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(observacion__icontains=query) |
            Q(tipo__icontains=query) |
            Q(precio__icontains=query) |
            Q(proveedor__icontains=query) |
            Q(cantidad__icontains=query) |
            Q(registrado_por__username__icontains=query)
        )

    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            articulos = articulos.filter(fecha_registro__gte=fecha_inicio)
        except ValueError:
            articulos = Articulo.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            articulos = articulos.filter(fecha_registro__lte=fecha_fin)
        except ValueError:
            articulos = Articulo.objects.none()

    return articulos
def reporte_articulo_pdf(request):
    buffer = BytesIO()

    # Crear documento
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)

    # Metadatos
    doc.title = "Listado de Artículos CCD"
    doc.author = "CCD"
    doc.subject = "Listado de artículos"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    # Título
    titulo = Paragraph("REPORTE DE ARTÍCULOS", styles["Title"])
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
    data_articulos = [["ID", "Nombre", "Marca", "Tipo", "Precio", "Cantidad", "Observación"]]
    for articulo in Articulo.objects.all():
        data_articulos.append([
            articulo.id,
            articulo.nombre,
            articulo.marca,
            articulo.tipo,
            articulo.precio,
            articulo.cantidad,
            articulo.observacion
        ])
    tabla_articulos = Table(data_articulos, colWidths=[70, 100, 100, 90, 90, 90, 180])
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

    # Construir documento con marca de agua
    doc.build(elements, onFirstPage=draw_table_on_canvas, onLaterPages=draw_table_on_canvas)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="articulos.pdf"'
    return response
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl import Workbook
from openpyxl.drawing.image import Image

def reporte_articulo_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Artículos"

    # Ajustar el ancho de columnas A y B para que quepa el logo
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 25

    # Ajustar la altura de la fila 1 para el logo
    ws.row_dimensions[1].height = 90

    # Agregar el logo
    logo_path = finders.find('imagen/logo.png')
    img = Image(logo_path)
    img.height = 80
    img.width = 200
    ws.add_image(img, 'A1')

    # Fusionar celdas A1 y B1 para que el logo ocupe espacio visualmente
    ws.merge_cells('A1:B1')

    # Título principal
    ws.merge_cells('C1:F1')
    ws['C1'] = "GESTOR CCD"
    ws['C1'].font = Font(size=24, bold=True)
    ws['C1'].alignment = Alignment(horizontal='center', vertical='center')

    # Subtítulo
    ws.merge_cells('A2:G2')
    ws['A2'] = "Listado de Artículos"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    # Encabezados de la tabla
    headers = ["ID", "Nombre", "Marca", "Tipo", "Precio", "Cantidad", "Observación"]
    ws.append(headers)

    # Estilo para los encabezados
    header_fill = PatternFill(start_color="FF0056B3", end_color="FF0056B3", fill_type="solid")

    for cell in ws[3]:
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Bordes
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Agregar datos
    articulos = Articulo.objects.all()
    for articulo in articulos:
        precio = f"${articulo.precio:,.2f}"
        ws.append([
            articulo.id,
            articulo.nombre,
            articulo.marca,
            articulo.tipo,
            precio,
            articulo.cantidad,
            articulo.observacion,
        ])

    # Ajustar ancho de columnas
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 30

    # Aplicar estilo a celdas de datos
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row, min_col=1, max_col=7):
        for cell in row:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border

    # Altura de filas para los títulos
    ws.row_dimensions[1].height = 60
    ws.row_dimensions[2].height = 30

    # Preparar la respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Reporte_articulos.xlsx"'
    wb.save(response)
    return response


@login_required
def crear_pedido(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Realizar pedidos', 'url': reverse('papeleria:crear_pedido')}, 
    ] 

    if request.method == 'POST':
        estado = 'confirmado' if request.user.role == 'Administrador' else 'pendiente'
        area_usuario = request.user.area

        pedido = Pedido.objects.create(registrado_por=request.user, estado=estado)
        articulos = request.POST.getlist('articulo')
        cantidades = request.POST.getlist('cantidad')
        tipos_seleccionados = request.POST.getlist('tipo_articulo')

        resumen_articulos = []  # Para el correo

        for idx, (articulo_id, cantidad, tipo_id) in enumerate(zip(articulos, cantidades, tipos_seleccionados)):
            if articulo_id and cantidad and tipo_id:
                if articulo_id != tipo_id:
                    pedido.delete()
                    return render(request, 'pedidos/pedidos.html', {
                        'articulos': Articulo.objects.all(),
                        'breadcrumbs': breadcrumbs,
                        'error': f"Error en la línea {idx + 1}: El artículo y el tipo seleccionado no coinciden."
                    })

                try:
                    cantidad = int(cantidad)
                    articulo = Articulo.objects.get(id=articulo_id)

                    if estado == 'confirmado' and articulo.cantidad < cantidad:
                        pedido.delete()
                        return render(request, 'pedidos/pedidos.html', {
                            'articulos': Articulo.objects.all(),
                            'breadcrumbs': breadcrumbs,
                            'error': f"No hay suficiente stock para el artículo: {articulo.nombre}"
                        })

                    PedidoArticulo.objects.create(
                        pedido=pedido,
                        articulo=articulo,
                        cantidad=cantidad,
                        area=area_usuario
                    )

                    if estado == 'confirmado':
                        articulo.cantidad -= cantidad
                        articulo.save()

                    resumen_articulos.append(f"- {articulo.nombre} × {cantidad}")

                except (ValueError, Articulo.DoesNotExist):
                    pedido.delete()
                    return render(request, 'pedidos/pedidos.html', {
                        'articulos': Articulo.objects.all(),
                        'breadcrumbs': breadcrumbs,
                        'error': f"Error al procesar el artículo en la línea {idx + 1}."
                    })

        # Enviar correo a administradores del módulo "Papelería"
        admin_users = User.objects.filter(role='Administrador', module='Papeleria', is_active=True)
        admin_emails = [admin.email for admin in admin_users if admin.email]

        if admin_emails:
            articulos_str = '\n'.join(resumen_articulos)
            subject = "Nuevo pedido registrado por un usuario"
            message = (
                f"Hola querido administrador,\n\n"
                f"Desde el módulo de Papelería te informamos que el usuario '{request.user.username}' "
                f"ha realizado un nuevo pedido.\n\n"
                f"Información del pedido:\n"
                f"Usuario: {request.user.username}\n"
                f"Rol: {request.user.role}\n"
                f"Área: {request.user.area}\n"
                f"Módulo: {request.user.module}\n"
                f"ID del pedido: {pedido.id}\n"
                f"Estado inicial del pedido: {estado}\n\n"
                f"Artículos solicitados:\n"
                f"{articulos_str}\n\n"
                f"Por favor revisa y confirma el pedido si corresponde.\n\n"
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

        if request.user.role == 'Empleado':
            return redirect('papeleria:pedidos_pendientes')
        else:
            return redirect('papeleria:listado_pedidos')

    # Si la solicitud es GET
    articulos = Articulo.objects.all()
    return render(request, 'pedidos/pedidos.html', {
        'articulos': articulos,
        'breadcrumbs': breadcrumbs
    })

def listado_pedidos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Listado de pedidos', 'url': reverse('papeleria:listado_pedidos')},
    ]
    
    # Usamos el campo correcto del modelo
    pedidos = Pedido.objects.filter(registrado_por=request.user).order_by('-fecha_pedido')

    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos, 'breadcrumbs': breadcrumbs})
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
@require_POST
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado:
            if nuevo_estado == 'confirmado':
                articulos_del_pedido = pedido.articulos.all()
                for articulo_pedido in articulos_del_pedido:
                    articulo = articulo_pedido.articulo
                    cantidad_pedida = articulo_pedido.cantidad

                    if articulo.cantidad >= cantidad_pedida:
                        articulo.cantidad -= cantidad_pedida
                        articulo.save()
                    else:
                        messages.error(request, f"No hay suficiente stock de {articulo.nombre}.")
                        return redirect('papeleria:pedidos_pendientes')

            pedido.estado = nuevo_estado
            pedido.save()

            usuario = pedido.registrado_por
            if usuario and usuario.email:
                estado_legible = nuevo_estado.capitalize()
                send_mail(
                    'Actualización de tu pedido',
                    f"Hola {usuario.username}, este correo es para avisarte que tu pedido fue {estado_legible.lower()}.",
                    settings.DEFAULT_FROM_EMAIL,
                    [usuario.email],
                    fail_silently=False,
                )

            messages.success(request, 'Estado del pedido actualizado correctamente.')
            return redirect('papeleria:pedidos_pendientes')

    messages.error(request, 'No se pudo actualizar el estado' \
    ' del pedido.')
    return redirect('papeleria:pedidos_pendientes')
    
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
@require_POST
def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado:
            if nuevo_estado == 'confirmado':
                articulos_del_pedido = pedido.articulos.all()
                for articulo_pedido in articulos_del_pedido:
                    articulo = articulo_pedido.articulo
                    cantidad_pedida = articulo_pedido.cantidad

                    if articulo.cantidad >= cantidad_pedida:
                        articulo.cantidad -= cantidad_pedida
                        articulo.save()
                    else:
                        messages.error(request, f"No hay suficiente stock de {articulo.nombre}.")
                        return redirect('papeleria:pedidos_pendientes')

            pedido.estado = nuevo_estado
            pedido.save()

            usuario = pedido.registrado_por
            if usuario and usuario.email:
                estado_legible = nuevo_estado.capitalize()
                send_mail(
                    'Actualización de tu pedido',
                    f"Hola {usuario.username}, este correo es para avisarte que tu pedido fue {estado_legible.lower()}.",
                    settings.DEFAULT_FROM_EMAIL,
                    [usuario.email],
                    fail_silently=False,
                )

            messages.success(request, 'Estado del pedido actualizado correctamente.')
            return redirect('papeleria:pedidos_pendientes')

    messages.error(request, 'No se pudo actualizar el estado' \
    ' del pedido.')
    return redirect('papeleria:pedidos_pendientes')

def pedidos_pendientes(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Pedidos pendientes', 'url': reverse('papeleria:pedidos_pendientes')}, 
    ]
    pedidos = Pedido.objects.filter(estado='pendiente')
    return render(request, 'pedidos/confirmar_pedido.html', {'pedidos': pedidos, 'breadcrumbs': breadcrumbs})

def lista_stock_bajo(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Stock bajo', 'url': reverse('papeleria:lista_bajo_stock')}, 
    ]
    articulo_bajo_stock= Articulo.objects.filter(cantidad__lt=10)
    bajo_stock = articulo_bajo_stock.exists()
    nombres_bajo_stock = [art.nombre for art in articulo_bajo_stock]

    return render(request, 'articulo/bajo_stock.html', {
       'articulos': articulo_bajo_stock,  # Corregir el error de comillas
        'bajo_stock': bajo_stock,
        'nombres_bajo_stock': nombres_bajo_stock,
         'breadcrumbs': breadcrumbs
    })
from django.db.models import Sum
def index_estadistica(request):
    breadcrumbs = [
    {'name': 'Inicio', 'url': '/index_pap'},
    {'name': 'Estadisticas', 'url': '/index_estadistica/'},  # URL fija
]

    return render(request, 'estadisticas/index_estadistica.html', {'breadcrumbs': breadcrumbs})

def estadisticas_articulos(request):
    articulos = Articulo.objects.all().order_by('-cantidad')  # Puedes ordenar por cantidad, nombre, etc.
    total_cantidad = articulos.aggregate(total=Sum('cantidad'))['total'] or 0
    return render(request, 'estadisticas/estadisticas_articulos.html', {
        'articulos': articulos,
        'total_cantidad': total_cantidad,
    })
#GRAFIC DE CANTIDAD DE ARTICULOS
def graficas_articulos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Estadisticas', 'url': reverse('papeleria:index_estadistica')}, 
        {'name': 'Grafico de articulos', 'url': reverse('papeleria:graficas_articulos')}, 
    ]
    articulos = Articulo.objects.all()
    nombres = [art.nombre for art in articulos]
    cantidades = [art.cantidad for art in articulos]

    return render(request, 'estadisticas/grafica_articulos.html', {
        'nombres': nombres,
        'cantidades': cantidades,
        'breadcrumbs': breadcrumbs
    })
#grafica de usuario

def graficas_usuario(request):
    activos = CustomUser.objects.filter(is_active=True).count()
    inactivos = CustomUser.objects.filter(is_active=False).count()

    nombres = ['Activos', 'Inactivos']
    cantidades = [activos, inactivos] 
    return render(request, 'estadisticas/grafica_usuarios.html', {'nombres':nombres,
                                                                  'cantidades': cantidades})