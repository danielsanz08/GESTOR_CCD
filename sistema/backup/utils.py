import os
import json
from django.core import serializers
from django.conf import settings
from datetime import datetime
from libreria.models import CustomUser
from papeleria.models import Articulo, Pedido, PedidoArticulo

def crear_backup():
    # Modelos a incluir en la copia
    modelos = [
        CustomUser,
        Articulo,
        Pedido,
        PedidoArticulo
    ]
    
    # Serializar datos
    data = {}
    for modelo in modelos:
        nombre_modelo = modelo._meta.label
        objetos = modelo.objects.all()
        data[nombre_modelo] = serializers.serialize('json', objetos)
    
    # Crear nombre de archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f'backup_{timestamp}.json'
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'backups', nombre_archivo)
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    
    # Guardar archivo
    with open(ruta_archivo, 'w') as f:
        json.dump(data, f)
    
    return nombre_archivo, ruta_archivo

def restaurar_backup(archivo):
    with open(archivo.path, 'r') as f:
        data = json.load(f)
    
    for nombre_modelo, datos_serializados in data.items():
        # Limpiar modelo existente
        modelo = get_model(nombre_modelo)
        modelo.objects.all().delete()
        
        # Cargar datos
        for obj in serializers.deserialize('json', datos_serializados):
            obj.save()

def get_model(model_name):
    from django.apps import apps
    return apps.get_model(model_name)