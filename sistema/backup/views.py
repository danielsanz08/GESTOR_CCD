from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Backup
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import crear_backup, restaurar_backup
from datetime import datetime
import os
from django.urls import reverse
from django.db import transaction
from django.core import management
from django.contrib.auth import get_user_model
from django import db

@login_required(login_url='/acceso_denegado/')
def index_backup(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': 'index_backup'}]
    return render(request, 'backup/index.html', {'breadcrumbs': breadcrumbs})

@login_required
def lista_backups(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': 'index_backup'},
        {'name': 'Lista de backups', 'url': 'lista_backups'},
    ]
    
    q = request.GET.get('q', '')
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    
    backups = Backup.objects.all().order_by('-fecha_creacion')
    
    if q:
        backups = backups.filter(
            Q(nombre__icontains=q) |
            Q(fecha_creacion__icontains=q) |
            Q(creado_por__icontains=q) 
        )

    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            backups = backups.filter(fecha_creacion__gte=fecha_inicio)
        except ValueError:
            backups = Backup.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            backups = backups.filter(fecha_creacion__lte=fecha_fin)
        except ValueError:
            backups = Backup.objects.none()
    
    paginator = Paginator(backups, 4)
    page = request.GET.get('page')
    backups_paginados = paginator.get_page(page)
    
    return render(request, 'backup/listar.html', {
        'backups': backups_paginados, 
        'breadcrumbs': breadcrumbs,
        'q': q,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str
    })

@login_required
def crear_nuevo_backup(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Crear backups', 'url': reverse('backup:crear_backup')},
    ]

    if request.method == 'POST':
        try:
            nombre_archivo, ruta_archivo = crear_backup()
            tamano = os.path.getsize(ruta_archivo)
            tamano_mb = round(tamano / (1024 * 1024), 2)
            nombre = request.POST.get('nombre') or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            backup = Backup(
                nombre=nombre,
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="libreria.CustomUser, papeleria.Articulo, papeleria.Pedido, papeleria.PedidoArticulo, cafeteria.Productos, cafeteria.Pedido, cafeteria.PedidoProducto, cde.PedidoCde, cde.PedidoProductoCde",
                creado_por=request.user
            )

            with open(ruta_archivo, 'rb') as f:
                backup.archivo.save(nombre_archivo, f)

            messages.success(request, 'Copia de seguridad creada exitosamente.')
            return redirect('backup:lista_backups')

        except Exception as e:
            messages.error(request, f'Error al crear copia de seguridad: {str(e)}')
            return redirect('backup:crear_backup')

    return render(request, 'backup/crear.html', {'breadcrumbs': breadcrumbs})

@login_required
def restaurar_backup_view(request, id):
    try:
        with transaction.atomic():
            backup = get_object_or_404(Backup, id=id)
            ruta_absoluta = os.path.join(settings.MEDIA_ROOT, backup.archivo.name)

            if not os.path.exists(ruta_absoluta):
                raise Exception(f"El archivo de backup no existe en {ruta_absoluta}")

            user_id = request.user.id
            session_key = request.session.session_key

            db.connections.close_all()

            restaurar_backup(ruta_absoluta)

            User = get_user_model()
            user = User.objects.get(id=user_id)
            request.user = user
            request.session.modified = True

            messages.success(request, 'Copia de seguridad restaurada exitosamente.')
            
    except Exception as e:
        messages.error(request, f'Error al restaurar copia de seguridad: {str(e)}')
        return redirect('backup:lista_backups')

    return HttpResponseRedirect(reverse('backup:lista_backups'))

@login_required
def descargar_backup(request, id):
    backup = get_object_or_404(Backup, id=id)
    try:
        return FileResponse(open(backup.archivo.path, 'rb'), as_attachment=True)
    except Exception as e:
        messages.error(request, f'Error al descargar archivo: {str(e)}')
        return redirect('backup:lista_backups')

@login_required
def eliminar_backup(request, id):
    try:
        backup = get_object_or_404(Backup, id=id)
        if os.path.exists(backup.archivo.path):
            os.remove(backup.archivo.path)
        backup.delete()
        messages.success(request, 'Copia de seguridad eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar copia de seguridad: {str(e)}')

    return redirect('backup:lista_backups')

def exportar_bd(nombre_archivo=None):
    """Función auxiliar para exportar la base de datos completa"""
    if not nombre_archivo:
        nombre_archivo = f"backup_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    ruta_backup = os.path.join(settings.BACKUP_ROOT, nombre_archivo)
    
    try:
        with open(ruta_backup, 'w', encoding='utf-8') as f:
            management.call_command('dumpdata', stdout=f)
        
        return nombre_archivo, ruta_backup
    except Exception as e:
        raise Exception(f"Error al exportar la base de datos: {str(e)}")

@login_required
def exportar(request):
    """Vista para exportar la base de datos completa"""
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Exportar BD', 'url': reverse('backup:exportar')},
    ]
    
    try:
        nombre_archivo, ruta_backup = exportar_bd()

        if not os.path.exists(ruta_backup):
            messages.error(request, 'El archivo de respaldo no se encontró.')
            return redirect('backup:lista_backups')

        # Registrar la exportación en la tabla de backups
        tamano = os.path.getsize(ruta_backup)
        tamano_mb = round(tamano / (1024 * 1024), 2)
        
        backup = Backup(
            nombre=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            tamano=f"{tamano_mb} MB",
            modelos_incluidos="Todos (exportación completa)",
            creado_por=request.user
        )
        
        with open(ruta_backup, 'rb') as f:
            backup.archivo.save(nombre_archivo, f, save=False)
        
        backup.save()

        # Ofrecer el archivo para descargar
        response = FileResponse(open(ruta_backup, 'rb'), as_attachment=True, filename=nombre_archivo)
        messages.success(request, 'Base de datos exportada exitosamente.')
        return response

    except Exception as e:
        messages.error(request, f'Error al exportar la base de datos: {str(e)}')
        return redirect('backup:lista_backups')

@login_required
def importar_backup_view(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Importar backup', 'url': reverse('backup:importar')},
    ]
    
    if request.method == 'POST':
        try:
            archivo_subido = request.FILES['archivo']
            nombre = request.POST.get('nombre', f"backup_importado_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

            carpeta_backups = os.path.join(settings.MEDIA_ROOT, 'backups')
            os.makedirs(carpeta_backups, exist_ok=True)
            
            nombre_archivo = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{archivo_subido.name}"
            ruta_completa = os.path.join(carpeta_backups, nombre_archivo)

            with open(ruta_completa, 'wb+') as destino:
                for chunk in archivo_subido.chunks():
                    destino.write(chunk)

            tamano = os.path.getsize(ruta_completa)
            tamano_mb = round(tamano / (1024 * 1024), 2)

            backup = Backup(
                nombre=nombre,
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="Todos (backup completo)",
                creado_por=request.user
            )
            
            with open(ruta_completa, 'rb') as f:
                backup.archivo.save(nombre_archivo, f, save=False)

            backup.save()

            if 'restaurar' in request.POST:
                try:
                    user_id = request.user.id
                    session_key = request.session.session_key
                    
                    db.connections.close_all()
                    
                    with transaction.atomic():
                        restaurar_backup(backup.archivo.path)
                    
                    User = get_user_model()
                    user = User.objects.get(id=user_id)
                    request.user = user
                    request.session.modified = True
                    
                    messages.success(request, 'Backup importado y restaurado exitosamente.')
                except Exception as e:
                    messages.warning(request, f'Backup importado pero error al restaurar: {str(e)}')
            else:
                messages.success(request, 'Backup importado exitosamente.')

            return HttpResponseRedirect(reverse('backup:lista_backups'))

        except Exception as e:
            messages.error(request, f'Error al importar el backup: {str(e)}')
            return redirect('backup:importar')

    return render(request, 'backup/importar.html', {'breadcrumbs': breadcrumbs})