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
