from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
app_name = 'cde'
urlpatterns = [
    path('index_cde/', views.index_cde, name='index_cde'),
    path('login_cde/', views.login_cde, name='login_cde'),
    path('logout_cde/', views.logout_cde, name='logout_cde'),
     path('pedidos_cde/crear/', views.crear_pedido_cde, name='crear_pedido_cde'),
    path('pedidos_cde/mis_pedidos', views.mis_pedidos_cde, name='mis_pedidos_cde'),
    path('pedidos_cde/pendientes/<int:pedido_id>/', views.cambiar_estado_pedido_cde, name='cambiar_estado_pedido_cde'),
    path('pedidos_cde/pendientes_cde/', views.pedidos_pendientes_cde, name='pedidos_pendientes_cde'),
    path('pedidos_cde/mis_pedidos_pendientes_cde/', views.mis_pedidos_pendientes_cde, name='mis_pedidos_pendientes_cde'),
    path('pedidos_caf/lista_pedidos_cde/', views.listado_pedidos_cde, name='lista_pedidos_cde'),
    path('ver_perfil_cde/<int:id>/', views.ver_usuario_cde, name='ver_usuario_cde'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
