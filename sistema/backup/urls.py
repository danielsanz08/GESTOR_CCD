# backup/urls.py
from django.urls import path
from . import views

app_name = 'backup'

urlpatterns = [
    path('index_backup', views.index_backup, name='index_backup'),
    path('lista_backups', views.lista_backups, name='lista_backups'),
    path('crear/', views.crear_nuevo_backup, name='crear_backup'),
    path('restaurar/<int:id>/', views.restaurar_backup_view, name='restaurar_backup'),
    path('descargar/<int:id>/', views.descargar_backup, name='descargar_backup'),
    path('eliminar/<int:id>/', views.eliminar_backup, name='eliminar_backup'),
    path('importar/', views.importar_backup_view, name='importar'),

    # ✅ CORRECTO: apunta a la vista que maneja el request
    path('exportar/', views.exportar, name='exportar_backup'),
]
