from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.utils.timezone import now
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from papeleria.models import Articulo, PedidoArticulo, Pedido
from papeleria.forms import LoginForm, ArticuloForm, ArticuloEditForm, PedidoArticuloForm
from libreria.models import CustomUser
from io import BytesIO
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.drawing.image import Image
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa
User = get_user_model()
#ACCESO DENEGADO
def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')
#INDEX DE PAPELERIA
@never_cache
@login_required(login_url='/acceso_denegado/')
def index_pap(request):
    breadcrumbs = [{'name': 'Inicio', 'url': '/index_pap'}]
    return render(request, 'index_pap/index_pap.html', {'breadcrumbs': breadcrumbs})

#LOGIN  Y LOGOUT DE PAPELERIA
def login_papeleria(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if not user.is_active:  # Check if the user is inactive
                    messages.error(request, "Tu usuario está inactivo.")
                elif user.module == 'Papeleria':  # Verify the user belongs to Papelería
                    login(request, user)
                    messages.success(request, "Sesión iniciada correctamente en Papelería.")
                    return redirect('papeleria:index_pap')  # Redirect to Papelería homepage
                else:
                    messages.error(request, "No tienes acceso a este módulo.")
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'login_pap/login_pap.html', {'form': form})

@never_cache
@login_required(login_url='/acceso_denegado/')
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect(reverse('libreria:inicio'))

#VIEWS DE ARTICULOS
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

def lista_stock_bajo(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Stock bajo', 'url': reverse('papeleria:lista_bajo_stock')}, 
    ]

    query = request.GET.get('q', '').strip()

    # Filtrar solo artículos con cantidad menor a 10
    articulos_bajo_stock = Articulo.objects.filter(cantidad__lt=10)

    if query:
        articulos_bajo_stock = articulos_bajo_stock.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(tipo__icontains=query)
        )

    bajo_stock = articulos_bajo_stock.exists()
    nombres_bajo_stock = [art.nombre for art in articulos_bajo_stock]

    paginator = Paginator(articulos_bajo_stock, 4)
    page_number = request.GET.get('page')
    articulos_page = paginator.get_page(page_number)

    return render(request, 'articulo/bajo_stock.html', {
        'articulos': articulos_page,
        'bajo_stock': bajo_stock,
        'nombres_bajo_stock': nombres_bajo_stock,
        'breadcrumbs': breadcrumbs
    })
#VIEWS DE PEDIDOS
@login_required
def crear_pedido(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Realizar pedidos', 'url': reverse('papeleria:crear_pedido')}, 
    ] 

    if request.method == 'POST':
        # Determina el estado del pedido dependiendo del rol del usuario
        if request.user.role == 'Administrador':
            estado = 'confirmado'
        else:
            estado = 'pendiente'

        # Crear el pedido
        pedido = Pedido.objects.create(registrado_por=request.user, estado=estado)

        # Obtener los artículos y cantidades seleccionadas
        articulos = request.POST.getlist('articulo')
        cantidades = request.POST.getlist('cantidad')

        for articulo_id, cantidad in zip(articulos, cantidades):
            if articulo_id and cantidad:
                cantidad = int(cantidad)
                articulo = Articulo.objects.get(id=articulo_id)

                # Obtener el área desde la info del usuario
                area_usuario = getattr(request.user, 'area', 'No establecido')

                # Crear la relación entre el pedido y los artículos, agregando area
                PedidoArticulo.objects.create(
                    pedido=pedido,
                    articulo=articulo,
                    cantidad=cantidad,
                    area=area_usuario,
                )

                # Si el pedido está confirmado, verificar el stock de los artículos
                if estado == 'confirmado':
                    if articulo.cantidad >= cantidad:
                        articulo.cantidad -= cantidad
                        articulo.save()
                    else:
                        pedido.delete()
                        return render(request, 'pedidos/pedidos.html', {
                            'articulos': Articulo.objects.all(),
                            'breadcrumbs': breadcrumbs,
                            'error': f"No hay suficiente stock para el artículo: {articulo.nombre}"
                        })

        # Enviar correo a administradores del módulo "Papelería"
        admin_users = User.objects.filter(role='Administrador', module='Papeleria', is_active=True)
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
                f"Módulo: {request.user.module}\n"
                f"ID del pedido: {pedido.id}\n"
                f"Estado inicial del pedido: {estado}\n\n"
                f"Por favor revisa y confirma el pedido si corresponde.\n\n"
                f"Gracias por su atención.\n"
                f"El equipo de Gestor CCD les desea un excelente día."
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                list(admin_emails),
                fail_silently=False,
            )

        # Redirigir dependiendo del rol del usuario
        if request.user.role == 'Empleado':
            return redirect('papeleria:pedidos_pendientes')
        else:
            return redirect('papeleria:listado_pedidos')

    # Si la solicitud es GET, mostrar los artículos disponibles
    articulos = Articulo.objects.all()
    return render(request, 'pedidos/pedidos.html', {'articulos': articulos, 'breadcrumbs': breadcrumbs})

def listado_pedidos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Listado de pedidos', 'url': reverse('papeleria:listado_pedidos')},
    ]
    
    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Obtiene pedidos del usuario actual ordenados por fecha_pedido descendente
    pedidos = Pedido.objects.filter(registrado_por=request.user).order_by('-fecha_pedido')

    if query:
        pedidos = pedidos.filter(
            Q(registrado_por__username__icontains=query) |
            Q(estado__icontains=query) |
            Q(articulos__area__icontains=query)  # filtro por area en modelo relacionado
        ).distinct()  # distinct para evitar duplicados por joins

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

    return render(request, 'pedidos/lista_pedidos.html', {
        'pedidos': pedidos_page,
        'breadcrumbs': breadcrumbs
    })

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

    query = request.GET.get('q', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    # Filtrar solo pedidos pendientes
    pedidos = Pedido.objects.filter(estado='pendiente').order_by('-fecha_pedido')

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

    return render(request, 'pedidos/confirmar_pedido.html', {
        'pedidos': pedidos_page,
        'breadcrumbs': breadcrumbs,
    })
#VALIDAR DATOS
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

#ESTADISTICAS 
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
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Estadisticas', 'url': reverse('papeleria:index_estadistica')}, 
        {'name': 'Grafico de usuarios activos e inactivos', 'url': reverse('papeleria:graficas_usuarios')}, 
    ]
    activos = CustomUser.objects.filter(is_active=True).count()
    inactivos = CustomUser.objects.filter(is_active=False).count()

    nombres = ['Activos', 'Inactivos']
    cantidades = [activos, inactivos] 
    return render(request, 'estadisticas/grafica_usuarios.html', {'nombres':nombres,
                                                                  'cantidades': cantidades,
                                                                  'breadcrumbs': breadcrumbs})
def grafica_pedidos(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Estadisticas', 'url': reverse('papeleria:index_estadistica')}, 
        {'name': 'Grafico de estado de pedidos', 'url': reverse('papeleria:grafica_pedidos')}, 
    ]
    pendientes = Pedido.objects.filter(estado='Pendiente').count()
    confirmados = Pedido.objects.filter(estado='Confirmado').count()
    cancelados = Pedido.objects.filter(estado= 'Cancelado').count()

    nombres = ['Pendiente', 'Confirmado', 'Cancelado']
    cantidades = [pendientes, confirmados, cancelados]
    return render(request, 'estadisticas/grafica_estado_pendiente.html',{'nombres':nombres,
                                                                         'cantidades':cantidades,
                                                                'breadcrumbs': breadcrumbs} )

def grafica_pedidos_area(request):
    # Agrupar por área de los artículos en los pedidos
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Estadisticas', 'url': reverse('papeleria:index_estadistica')}, 
        {'name': 'Grafico de pedidos por áreas', 'url': reverse('papeleria:pedidos_area')}, 
    ]
    pedidos_por_area = Pedido.objects.values('articulos__area').annotate(total=Count('id')).order_by('articulos__area')

    nombres = []
    cantidades = []

    for item in pedidos_por_area:
        nombres.append(item['articulos__area'] or 'Sin área')
        cantidades.append(item['total'])

    return render(request, 'estadisticas/grafico_pedido_area.html', {
        'nombres': nombres,
        'cantidades': cantidades,
        'breadcrumbs': breadcrumbs
    })

def grafica_bajo_Stock(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Estadisticas', 'url': reverse('papeleria:index_estadistica')}, 
        {'name': 'Grafico de bajo stock', 'url': reverse('papeleria:grafica_bajoStock')}, 
    ]
    articulos = Articulo.objects.filter(cantidad__lt=10)
    nombres = [art.nombre for art in articulos]
    cantidades = [art.cantidad for art in articulos]
    return render(request, 'estadisticas/grafica_bajoStock.html', {
        'nombres': nombres,
        'cantidades': cantidades,
        'breadcrumbs': breadcrumbs
    })

#EXPORTAR A PDFS
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
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    articulos = Articulo.objects.all()

    if query:
        articulos = articulos.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(tipo__icontains=query)
        )

    if fecha_inicio and fecha_fin:
        articulos = articulos.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    return articulos

def reporte_articulo_bajo_stock_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)

    doc.title = "Listado de Artículos CCD - Bajo Stock"
    doc.author = "CCD"
    doc.subject = "Listado de artículos con bajo stock"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    # Título
    titulo = Paragraph("REPORTE DE ARTÍCULOS CON BAJO STOCK", styles["Title"])
    elements.append(titulo)

    # Encabezado empresa
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    encabezado_data = [
        ["GESTOR CCD", "Lista de artículos con bajo stock", "Correo:", f"Fecha: {fecha_actual}"],
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

    # Info usuario
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

    # Aplicar filtro bajo stock (por ejemplo <= 5)
    # También puedes filtrar con base en parámetros del request si tienes función para eso.
    stock_minimo = 5
    articulos_bajo_stock = Articulo.objects.filter(cantidad__lte=stock_minimo).order_by('nombre')

    # Tabla de artículos bajo stock
    data_articulos = [["ID", "Nombre", "Marca", "Tipo", "Precio", "Cantidad", "Observación"]]
    for articulo in articulos_bajo_stock:
        data_articulos.append([
            articulo.id,
            articulo.nombre,
            articulo.marca,
            articulo.tipo,
            f"${articulo.precio:,.2f}",
            articulo.cantidad,
            articulo.observacion or "",
        ])

    tabla_articulos = Table(data_articulos, colWidths=[50, 130, 100, 90, 90, 70, 180])
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

    # Generar PDF
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="articulos_bajo_stock.pdf"'
    return response

def get_pedidos_filtrados(request):
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    pedidos = Pedido.objects.all()

    if query:
        pedidos = pedidos.filter(
            Q(id__icontains=query) |
            Q(estado__icontains=query) |
            Q(registrado_por__username__icontains=query) |
            Q(articulos__articulo__nombre__icontains=query)
        ).distinct()

    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(fecha_pedido__range=[fecha_inicio, fecha_fin])

    return pedidos

def reporte_pedidos_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter),
                            leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)

    doc.title = "Listado de pedidos CCD"
    doc.author = "CCD"
    doc.subject = "Listado de pedidos"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()

    titulo = Paragraph("REPORTE DE PEDIDOS", styles["Title"])
    elements.append(titulo)

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

    pedidos = Pedido.objects.prefetch_related('articulos__articulo').all()

    if q:
        pedidos = pedidos.filter(
            Q(id__icontains=q) |
            Q(articulos__articulo__nombre__icontains=q) |
            Q(registrado_por__username__icontains=q)
        ).distinct()

    if fecha_inicio:
        pedidos = pedidos.filter(fecha_pedido__gte=fecha_inicio)
    if fecha_fin:
        pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin)

    data_pedidos = [["ID Pedido", "Fecha", "Estado", "Registrado Por", "Artículos"]]

    for pedido in pedidos:
        articulos_text = "\n".join([
            f"{pa.articulo.nombre} x {pa.cantidad} (Tipo: {pa.tipo}, Área: {pa.area})"
            for pa in pedido.articulos.all()
        ]) or 'Sin artículos'

        data_pedidos.append([
            str(pedido.id),
            pedido.fecha_pedido.strftime('%d-%m-%Y'),
            pedido.get_estado_display(),
            pedido.registrado_por.username if pedido.registrado_por else 'No definido',
            articulos_text
        ])

    tabla_articulos = Table(data_pedidos, colWidths=[60, 140, 120, 180, 400])
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

    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Lista_de_pedidos_Gestor_CCD.pdf"'
    return response

def obtener_articulos_bajo_stock(filtro_marca=None, filtro_tipo=None):
    queryset = Articulo.objects.filter(cantidad__lt=10)
    if filtro_marca:
        queryset = queryset.filter(marca__icontains=filtro_marca)
    if filtro_tipo:
        queryset = queryset.filter(tipo__icontains=filtro_tipo)
    return queryset

def reporte_articulo_bajo_stock_pdf(request):
    # Captura los filtros GET
    marca = request.GET.get('marca', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    nombre = request.GET.get('nombre', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()

    print(f"Filtros recibidos: marca={marca}, tipo={tipo}, nombre={nombre}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}")

    articulos = Articulo.objects.filter(cantidad__lt=10)

    if marca:
        articulos = articulos.filter(marca__icontains=marca)
        print(f"Filtrado por marca: {marca}")
    if tipo:
        articulos = articulos.filter(tipo__icontains=tipo)
        print(f"Filtrado por tipo: {tipo}")
    if nombre:
        articulos = articulos.filter(nombre__icontains=nombre)
        print(f"Filtrado por nombre: {nombre}")
    if fecha_inicio:
        fecha_inicio_obj = parse_date(fecha_inicio)
        if fecha_inicio_obj:
            articulos = articulos.filter(fecha_registro__gte=fecha_inicio_obj)
            print(f"Filtrado por fecha_inicio: {fecha_inicio_obj}")
    if fecha_fin:
        fecha_fin_obj = parse_date(fecha_fin)
        if fecha_fin_obj:
            articulos = articulos.filter(fecha_registro__lte=fecha_fin_obj)
            print(f"Filtrado por fecha_fin: {fecha_fin_obj}")

    print(f"Cantidad de artículos después de filtro: {articulos.count()}")

    # ... Código para crear PDF igual que antes ...

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)

    doc.title = "Listado de Artículos bajos en stock CCD"
    doc.author = "CCD"

    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("REPORTE DE ARTÍCULOS BAJOS EN STOCK", styles["Title"]))

    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    encabezado_data = [
        ["GESTOR CCD", "Lista de usuarios", "Correo: gestorccd@gmail.com", f"Fecha: {fecha_actual}"],
        ["Cámara de comercio de Duitama", "Nit: 123456789", "(Correo de la camara)", "Teléfono: (tel. camara)"],
    ]
    tabla_encabezado = Table(encabezado_data, colWidths=[180, 180, 180, 180])
    tabla_encabezado.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(tabla_encabezado)

    usuario = request.user
    data_usuario = [["Usuario:", "Email:", "Rol:", "Cargo:"]]
    data_usuario.append([
        usuario.username,
        usuario.email,
        getattr(usuario, 'role', 'No definido'),
        getattr(usuario, 'cargo', 'No definido'),
    ])
    table_usuario = Table(data_usuario, colWidths=[180, 180, 180, 180])
    table_usuario.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table_usuario)

    elements.append(Paragraph("<br/><br/>", styles["Normal"]))

    data_articulos = [["ID", "Nombre", "Marca", "Tipo", "Precio", "Cantidad", "Observación"]]
    for articulo in articulos:
        data_articulos.append([
            articulo.id,
            articulo.nombre,
            articulo.marca,
            articulo.tipo,
            articulo.precio,
            articulo.cantidad,
            articulo.observacion or "",
        ])

    tabla_articulos = Table(data_articulos, colWidths=[70, 100, 100, 90, 90, 90, 180])
    tabla_articulos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#5564eb")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(tabla_articulos)

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Listado_bajos_stock_CCD.pdf"'
    return response

def obtener_pedidos_pendientes(filtro_fecha=None, filtro_area=None, filtro_tipo=None):
    queryset = Pedido.objects.filter(estado='Pendiente')

    if filtro_fecha:
        queryset = queryset.filter(fecha_pedido=filtro_fecha)

    if filtro_area:
        queryset = queryset.filter(articulos__area__icontains=filtro_area)

    if filtro_tipo:
        queryset = queryset.filter(articulos__tipo__icontains=filtro_tipo)

    return queryset.distinct()
def reporte_pedidos_pendientes_pdf(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    doc.title = "Listado de pedidos pendientes CCD"
    doc.author = "CCD"
    doc.subject = "Listado de pedidos pendientes"
    doc.creator = "Sistema de Gestión CCD"

    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("REPORTE DE PEDIDOS PENDIENTES", styles["Title"]))

    # Encabezado empresa
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    encabezado_data = [
        ["GESTOR CCD", "Lista de usuarios", "Correo: gestorccd@gmail.com", f"Fecha: {fecha_actual}"],
        ["Cámara de comercio de Duitama", "Nit: 123456789", "(Correo de la camara)", "Teléfono: (tel. camara)"],
    ]
    tabla_encabezado = Table(encabezado_data, colWidths=[180, 180, 180, 180])
    tabla_encabezado.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A5275')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(tabla_encabezado)

    # Tabla de usuario
    usuario = request.user
    data_usuario = [["Usuario:", "Email:", "Rol:", "Cargo:"], [
        usuario.username,
        usuario.email,
        getattr(usuario, 'role', 'No definido'),
        getattr(usuario, 'cargo', 'No definido'),
    ]]
    tabla_usuario = Table(data_usuario, colWidths=[180, 180, 180, 180])
    tabla_usuario.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DDEEFF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(tabla_usuario)

    # Filtros desde el request
    filtro_fecha = request.GET.get('fecha')
    filtro_area = request.GET.get('area')
    filtro_tipo = request.GET.get('tipo')

    pedidos = obtener_pedidos_pendientes(filtro_fecha, filtro_area, filtro_tipo)

    # Tabla de pedidos
    data_pedidos = [["ID Pedido", "Fecha", "Estado", "Registrado Por", "Artículos"]]

    for pedido in pedidos:
        articulos_text = "\n".join([
            f"{pa.articulo.nombre} x {pa.cantidad} (Tipo: {pa.tipo}, Área: {pa.area})"
            for pa in pedido.articulos.all()
        ])
        data_pedidos.append([
            str(pedido.id),
            pedido.fecha_pedido.strftime('%d-%m-%Y'),
            pedido.get_estado_display(),
            pedido.registrado_por.username if pedido.registrado_por else 'No definido',
            articulos_text or 'Sin artículos'
        ])

    tabla_pedidos = Table(data_pedidos, colWidths=[60, 140, 120, 180, 440])
    tabla_pedidos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(tabla_pedidos)

    doc.build(elements, onFirstPage=draw_table_on_canvas, onLaterPages=draw_table_on_canvas)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="Lista de pedidos pendientes Gestor CCD.pdf"'
    })
import importlib.resources
#EXPORTAR A EXCEL
def reporte_articulo_excel(request):
    # Parámetros de búsqueda
    q = request.GET.get('q', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    marca = request.GET.get('marca', '').strip()  # ejemplo filtro extra, cambia o quita si no quieres

    # Queryset base
    articulos = Articulo.objects.all()

    # Aplicar filtros si existen
    if q:
        articulos = articulos.filter(nombre__icontains=q)
    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            articulos = articulos.filter(fecha_registro__gte=fecha_inicio_dt)
        except ValueError:
            pass
    if fecha_fin:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            articulos = articulos.filter(fecha_registro__lte=fecha_fin_dt)
        except ValueError:
            pass

    if marca:
        articulos = articulos.filter(marca__icontains=marca)

    # Crear archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Listado de Artículos CCD"

    # Configuración columnas y filas (sin logo)
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 40
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 30
    ws.column_dimensions['E'].width = 20
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 33

    ws.row_dimensions[1].height = 60
    ws.row_dimensions[2].height = 30

    # Título principal y subtítulo
    ws.merge_cells('A1:G1')
    ws['A1'] = "GESTOR CCD"
    ws['A1'].font = Font(size=24, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A2:G2')
    ws['A2'] = "Listado de Artículos"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    # Encabezados
    headers = ["ID", "Nombre", "Marca", "Tipo", "Precio", "Cantidad", "Observación"]
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
    for articulo in articulos:
        precio_formateado = f"${articulo.precio:,.2f}" if articulo.precio else "-"
        ws.append([
            articulo.id,
            articulo.nombre,
            articulo.marca,
            articulo.tipo,
            precio_formateado,
            articulo.cantidad,
            articulo.observacion or "",
        ])

    # Aplicar estilos a celdas de datos
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row, min_col=1, max_col=7):
        for i, cell in enumerate(row, 1):
            cell.border = border
            # Alineación centrada excepto la columna Observación
            if i < 7:
                cell.alignment = Alignment(horizontal='center', vertical='center')
            else:
                cell.alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')

    # Preparar respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Reporte_articulos_filtrados.xlsx"'
    wb.save(response)
    return response
def get_pedidos_filtrados(request, user=None):
    query = request.GET.get('q', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    pedidos = Pedido.objects.all()

    if user:
        pedidos = pedidos.filter(registrado_por=user)

    if query:
        pedidos = pedidos.filter(
            Q(registrado_por__username__icontains=query) |
            Q(estado__icontains=query) |
            Q(articulos__area__icontains=query)
        ).distinct()

    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__gte=fecha_inicio_dt)
        except ValueError:
            return Pedido.objects.none()

    if fecha_fin:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            pedidos = pedidos.filter(fecha_pedido__lte=fecha_fin_dt)
        except ValueError:
            return Pedido.objects.none()

    return pedidos.order_by('-fecha_pedido')
def reporte_pedidos_excel(request):
    # Obtener los pedidos filtrados (de todos o del usuario actual)
    pedidos = get_pedidos_filtrados(request)  # Puedes pasar user=request.user si quieres limitar

    # Crear libro Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Pedidos CCD"

    # Ancho de columnas
    columnas = ['A', 'B', 'C', 'D', 'E', 'F']
    for col in columnas:
        ws.column_dimensions[col].width = 25

    # Altura de filas
    ws.row_dimensions[1].height = 50
    ws.row_dimensions[2].height = 30

    # Título
    ws.merge_cells('A1:F1')
    ws['A1'] = "GESTOR CCD"
    ws['A1'].font = Font(size=24, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A2:F2')
    ws['A2'] = "Listado de Pedidos"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    # Encabezados
    headers = ['ID', 'Fecha', 'Estado', 'Registrado Por', 'Total de Artículos', 'Áreas (Resumen)']
    ws.append(headers)

    header_fill = PatternFill(start_color="FF0056B3", end_color="FF0056B3", fill_type="solid")

    # Aplicar estilos a la fila 3 (encabezados)
    for row in ws.iter_rows(min_row=3, max_row=3, min_col=1, max_col=6):
        for cell in row:
            cell.fill = header_fill
            cell.font = Font(color="FFFFFF", bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')

    # Agregar filtro al rango A3:F3
    ws.auto_filter.ref = "A3:F3"

    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Agregar datos
    for pedido in pedidos:
        total_articulos = pedido.articulos.count()
        resumen_areas = ", ".join(set([a.area for a in pedido.articulos.all()])) or "-"
        ws.append([
            pedido.id,
            pedido.fecha_pedido.strftime('%Y-%m-%d'),
            pedido.estado,
            pedido.registrado_por.username if pedido.registrado_por else 'No definido',
            total_articulos,
            resumen_areas,
        ])

    # Aplicar bordes y alineación a los datos
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row, min_col=1, max_col=6):
        for cell in row:
            cell.border = border
            cell.alignment = Alignment(horizontal='center', vertical='center')

    # Respuesta HTTP para descargar archivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Reporte_pedidos.xlsx"'
    wb.save(response)
    return response
def reporte_articulo_bajo_stock_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Artículos Bajo Stock CCD"

    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 25
    ws.row_dimensions[1].height = 90

    logo_path = finders.find('imagen/logo.png')
    if logo_path:
        img = Image(logo_path)
        img.height = 80
        img.width = 200
        ws.add_image(img, 'A1')
    ws.merge_cells('A1:B1')

    ws.merge_cells('C1:G1')
    ws['C1'] = "GESTOR CCD"
    ws['C1'].font = Font(size=24, bold=True)
    ws['C1'].alignment = Alignment(horizontal='center', vertical='center')

    ws.merge_cells('A2:G2')
    ws['A2'] = "Listado de Artículos Bajo en Stock"
    ws['A2'].font = Font(size=18)
    ws['A2'].alignment = Alignment(horizontal='center', vertical='center')

    headers = ["ID", "Nombre", "Marca", "Tipo", "Precio", "Cantidad", "Observación"]
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

    articulos = Articulo.objects.filter(cantidad__lt=10)

    for articulo in articulos:
        ws.append([
            articulo.id,
            articulo.nombre,
            articulo.marca,
            articulo.tipo,
            f"${articulo.precio:.2f}",
            articulo.cantidad,
            articulo.observacion or '',
        ])

    column_widths = [10, 25, 25, 20, 15, 15, 40]
    for i, width in enumerate(column_widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = width

    for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=1, max_col=7):
        for i, cell in enumerate(row, 1):
            cell.border = border
            if i < 7:
                cell.alignment = Alignment(horizontal='center', vertical='center')
        row[6].alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')

    ws.row_dimensions[1].height = 60
    ws.row_dimensions[2].height = 30

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="Articulos_bajo_stock.xlsx"'
    wb.save(response)
    return response