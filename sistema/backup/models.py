from django.db import models
from django.core import serializers
import json
import os
from datetime import datetime
from django.conf import settings

class Backup(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='backups/')  # Esto guardará en MEDIA_ROOT/backups/
    tamano = models.CharField(max_length=100)
    modelos_incluidos = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nombre
