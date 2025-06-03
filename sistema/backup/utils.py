import os
import json
from django.core import serializers
from django.conf import settings
from datetime import datetime
from django.core import management
import subprocess
from django.apps import apps

def crear_backup():
    # Modelos a incluir en la copia
    modelos = [
        'libreria.CustomUser',
        'papeleria.Articulo',
        'papeleria.Pedido',
        'papeleria.PedidoArticulo'
    ]
    
    # Serializar datos
    data = {}
    for model_name in modelos:
        modelo = apps.get_model(model_name)
        objetos = modelo.objects.all()
        data[model_name] = serializers.serialize('json', objetos)
    
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

def restaurar_backup_json(ruta_archivo):  # Definición movida antes de restaurar_backup
    """Para backups en formato JSON"""
    try:
        # Primero limpiamos la base de datos
        management.call_command('flush', interactive=False)
        
        # Cargamos los datos
        with open(ruta_archivo, 'r') as f:
            data = json.load(f)
        
        for model_name, model_data in data.items():
            # Guardamos temporalmente los datos en un archivo
            temp_file = os.path.join(settings.MEDIA_ROOT, 'temp.json')
            with open(temp_file, 'w') as tf:
                tf.write(model_data)
            
            # Cargamos los datos
            management.call_command('loaddata', temp_file)
            
            # Eliminamos el archivo temporal
            os.remove(temp_file)
            
    except Exception as e:
        raise Exception(f"Error al restaurar JSON: {str(e)}")

def restaurar_backup_sql(ruta_archivo):
    """Para backups SQL"""
    db = settings.DATABASES['default']
    
    try:
        if db['ENGINE'] == 'django.db.backends.mysql':
            comando = f"mysql -u {db['USER']} -p{db['PASSWORD']} {db['NAME']} < {ruta_archivo}"
        elif db['ENGINE'] == 'django.db.backends.postgresql':
            comando = f"psql -U {db['USER']} -d {db['NAME']} -f {ruta_archivo}"
        else:
            raise Exception("Motor de base de datos no soportado")
        
        subprocess.run(comando, shell=True, check=True)
    except Exception as e:
        raise Exception(f"Error al restaurar SQL: {str(e)}")

def restaurar_backup(ruta_archivo):
    """Función principal de restauración que detecta el tipo de archivo"""
    if ruta_archivo.endswith('.json'):
        return restaurar_backup_json(ruta_archivo)
    elif ruta_archivo.endswith('.sql'):
        return restaurar_backup_sql(ruta_archivo)
    else:
        raise ValueError("Formato de archivo no soportado")