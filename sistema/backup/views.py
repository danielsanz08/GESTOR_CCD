from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Backup
from .utils import crear_backup, restaurar_backup
from datetime import datetime
import subprocess
import os


@login_required(login_url='/acceso_denegado/')
def index_backup(request):
    return render(request, 'backup/index.html')


@login_required
def lista_backups(request):
    backups = Backup.objects.all().order_by('-fecha_creacion')
    return render(request, 'backup/listar.html', {'backups': backups})

from django.core.files import File
@login_required
def crear_nuevo_backup(request):
    if request.method == 'POST':
        try:
            nombre_archivo, ruta_archivo = crear_backup()

            tamano = os.path.getsize(ruta_archivo)
            tamano_mb = round(tamano / (1024 * 1024), 2)

            nombre = request.POST.get('nombre', f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

            backup = Backup(
                nombre=nombre,
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="libreria.CustomUser, papeleria.Articulo, papeleria.Pedido, papeleria.PedidoArticulo",
                creado_por=request.user
            )
            with open(ruta_archivo, 'rb') as f:
                django_file = File(f)
                backup.archivo.save(nombre_archivo, django_file)

            backup.save()

            messages.success(request, 'Copia de seguridad creada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear copia de seguridad: {str(e)}')

        return redirect('backup:lista_backups')

    return render(request, 'backup/crear.html')

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
    if request.method == 'POST':
        try:
            archivo_subido = request.FILES['archivo']
            nombre = request.POST.get('nombre', f"backup_importado_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

            os.makedirs(settings.BACKUP_ROOT, exist_ok=True)

            nombre_archivo = f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{archivo_subido.name}"
            ruta_completa = os.path.join(settings.BACKUP_ROOT, nombre_archivo)

            with open(ruta_completa, 'wb+') as destino:
                for chunk in archivo_subido.chunks():
                    destino.write(chunk)

            tamano = os.path.getsize(ruta_completa)
            tamano_mb = round(tamano / (1024 * 1024), 2)

            backup = Backup(
                nombre=nombre,
                archivo=os.path.join('backups', nombre_archivo),
                tamano=f"{tamano_mb} MB",
                modelos_incluidos="Todos (backup completo)",
                creado_por=request.user
            )
            backup.save()

            if 'restaurar' in request.POST:
                try:
                    from django import db
                    db.connections.close_all()
                    restaurar_backup(ruta_completa)
                    messages.success(request, 'Backup importado y restaurado exitosamente.')
                except Exception as e:
                    messages.warning(request, f'Backup importado pero error al restaurar: {str(e)}')
            else:
                messages.success(request, 'Backup importado exitosamente.')

            return redirect('backup:lista_backups')

        except Exception as e:
            messages.error(request, f'Error al importar el backup: {str(e)}')
            return redirect('backup:importar')

    return render(request, 'backup/importar.html')
