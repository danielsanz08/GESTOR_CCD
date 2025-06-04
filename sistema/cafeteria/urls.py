from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'cafeteria'
urlpatterns = [
    path('index_caf/', views.index_caf, name='index_caf'),
    path('login/cafeteria/', views.login_cafeteria, name='login_cafeteria'),
    path('logout_caf/', views.logout_caf, name='logout_caf'),
    path('crear_productos/', views.crear_producto, name='crear_producto'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('eliminar_productos/<int:id>/', views.eliminar_producto, name='eliminar_productos'),
     path("editar_producto/<int:producto_id>/", views.editar_producto, name="editar_producto"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
