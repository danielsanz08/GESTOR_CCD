from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Backup
from django.core.paginator import Paginator
from django.db.models import Q
from .utils import crear_backup, restaurar_backup
from datetime import datetime
import subprocess
import os
from django.core import serializers
from django.urls import reverse

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
    fecha_inicio = None
    fecha_fin = None
    backups = Backup.objects.all().order_by('-fecha_creacion')
    # Filtrado por texto
    if q:
        backups = backups.filter(
            Q(nombre__icontains=q) |
            Q(fecha_creacion__icontains=q) |
            Q(creado_por__icontains=q) 
        )

    # Filtrado por fecha
    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            backups = backups.filter(fecha_registro__gte=fecha_inicio)
        except ValueError:
            backups = Backup.objects.none()

    if fecha_fin_str:
        try:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            backups = backups.filter(fecha_registro__lte=fecha_fin)
        except ValueError:
            backups = Backup.objects.none()
    #paginacion
    paginator = Paginator(backups, 4)
    page = request.GET.get('page')
    Backups = paginator.get_page(page)
    return render(request, 'backup/listar.html', {'backups': backups, 'breadcrumbs': breadcrumbs})

from django.core.files import File
@login_required
def crear_nuevo_backup(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Crear backups', 'url': reverse('backup:crear_backup')},
    ]

    if request.method == 'POST':
        try:
            # Crear el archivo de backup
            nombre_archivo, ruta_archivo = crear_backup()

            # Calcular tamaño en MB
            tamano = os.path.getsize(ruta_archivo)
            tamano_mb = round(tamano / (1024 * 1024), 2)

            # Nombre del backup (personalizado o automático)
            nombre = request.POST.get('nombre') or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Crear instancia de Backup
            backup = Backup(
                nombre=nombre,
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="libreria.CustomUser, papeleria.Articulo, papeleria.Pedido, papeleria.PedidoArticulo",
                creado_por=request.user
            )

            # Guardar el archivo al campo FileField
            with open(ruta_archivo, 'rb') as f:
                django_file = File(f)
                backup.archivo.save(nombre_archivo, django_file)

            backup.save()

            messages.success(request, 'Copia de seguridad creada exitosamente.')

        except Exception as e:
            messages.error(request, f'Error al crear copia de seguridad: {str(e)}')

        return redirect('backup:lista_backups')

    return render(request, 'backup/crear.html', {'breadcrumbs': breadcrumbs})

from django.contrib.sessions.middleware import SessionInterrupted

@login_required
def restaurar_backup_view(request, id):
    backup = get_object_or_404(Backup, id=id)
    try:
        ruta_absoluta = os.path.join(settings.MEDIA_ROOT, backup.archivo.name)

        if not os.path.exists(ruta_absoluta):
            raise Exception(f"El archivo de backup no existe en {ruta_absoluta}")

        restaurar_backup(ruta_absoluta)
        messages.success(request, 'Copia de seguridad restaurada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al restaurar copia de seguridad: {str(e)}')

    return redirect('backup:lista_backups')

@login_required
def descargar_backup(request, id):
    backup = get_object_or_404(Backup, id=id)
    try:
        return FileResponse(open(backup.archivo.path, 'rb'), as_attachment=True)
    except FileNotFoundError:
        messages.error(request, 'Archivo no encontrado.')
        return redirect('backup:lista_backups')


@login_required
def eliminar_backup(request, id):
    backup = get_object_or_404(Backup, id=id)
    try:
        if os.path.exists(backup.archivo.path):
            os.remove(backup.archivo.path)
        backup.delete()
        messages.success(request, 'Copia de seguridad eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar copia de seguridad: {str(e)}')

    return redirect('backup:lista_backups')

from django.core import management
def exportar_bd(nombre_archivo=None):
    if not nombre_archivo:
        nombre_archivo = f"backup_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    ruta_backup = os.path.join(settings.BACKUP_ROOT, nombre_archivo)
    
    try:
        # Capturar la salida de dumpdata en un archivo
        with open(ruta_backup, 'w', encoding='utf-8') as f:
            management.call_command('dumpdata', stdout=f)
        
        return nombre_archivo, ruta_backup
    except Exception as e:
        raise Exception(f"Error al exportar la base de datos: {str(e)}")


@login_required
def exportar(request):
    try:
        nombre_archivo, ruta_backup = exportar_bd()

        if not os.path.exists(ruta_backup):
            messages.error(request, 'El archivo de respaldo no se encontró.')
            return redirect('backup:lista_backups')

        return FileResponse(open(ruta_backup, 'rb'), as_attachment=True, filename=nombre_archivo)

    except Exception as e:
        messages.error(request, f'Error al exportar la base de datos: {str(e)}')
        return redirect('backup:lista_backups')


@login_required
def importar_backup_view(request):
    breadcrumbs = [
        {'name': 'Inicio', 'url': '/index_pap'},
        {'name': 'Backup', 'url': reverse('backup:index_backup')},
        {'name': 'Crear backups', 'url': reverse('backup:crear_backup')},
    ]
    if request.method == 'POST':
        try:
            archivo_subido = request.FILES['archivo']
            # Nombre “legible” para el backup en la base de datos
            nombre = request.POST.get(
                'nombre',
                f"backup_importado_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )

            # 1) Carpeta física donde guardaremos el JSON/SQL importado:
            carpeta_backups = os.path.join(settings.MEDIA_ROOT, 'backups')
            os.makedirs(carpeta_backups, exist_ok=True)

            # 2) Decidir el nombre del fichero en disco
            #    (aquí le anteponemos timestamp para evitar colisiones,
            #     pero podrías usar solo archivo_subido.name si prefieres)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"{ts}_{archivo_subido.name}"
            ruta_completa = os.path.join(carpeta_backups, nombre_archivo)

            # 3) Guardar físicamente el archivo en MEDIA_ROOT/backups/
            with open(ruta_completa, 'wb+') as destino:
                for chunk in archivo_subido.chunks():
                    destino.write(chunk)

            # 4) Obtener tamaño en MB (para mostrar en la tabla)
            tamano = os.path.getsize(ruta_completa)
            tamano_mb = round(tamano / (1024 * 1024), 2)

            # 5) Crear el registro en la tabla Backup, usando archivo.save()
            backup = Backup(
                nombre=nombre,
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="Todos (backup completo)",
                creado_por=request.user
            )
            # Al hacer backup.archivo.save(), el FileField guardará
            # 'backups/<nombre_archivo>' en backup.archivo.name y
            # físicamente el fichero estará en MEDIA_ROOT/backups/<nombre_archivo>
            with open(ruta_completa, 'rb') as f:
                backup.archivo.save(nombre_archivo, f, save=False)

            backup.save()

            # 6) Si el formulario incluyó el botón “restaurar”…
            if 'restaurar' in request.POST:
                try:
                    # Cerrar conexiones antes de restaurar
                    from django import db
                    db.connections.close_all()

                    # Restauramos a partir de la misma ruta física
                    from .utils import restaurar_backup
                    restaurar_backup(backup.archivo.path)

                    messages.success(request, 'Backup importado y restaurado exitosamente.')
                except Exception as e:
                    messages.warning(request, f'Backup importado pero error al restaurar: {str(e)}')
            else:
                messages.success(request, 'Backup importado exitosamente.')

            return redirect('backup:lista_backups')

        except Exception as e:
            messages.error(request, f'Error al importar el backup: {str(e)}')
            return redirect('backup:importar')

    return render(request, 'backup/importar.html', {'breadcrumbs': breadcrumbs})