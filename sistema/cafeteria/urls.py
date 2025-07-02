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
    path('ver_perfil/<int:id>/', views.ver_usuario_caf, name='ver_usuario_caf'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('eliminar_productos/<int:id>/', views.eliminar_producto, name='eliminar_productos'),
    path("editar_producto/<int:producto_id>/", views.editar_producto, name="editar_producto"),
    path("reporte_productos_pdf", views.reporte_productos_pdf, name="reporte_productos_pdf"),
    path("reporte_productos_excel", views.reporte_productos_excel, name="reporte_productos_excel"),
    path('productos/lista_bajo_stock/', views.lista_stock_bajo, name='lista_bajo_stock'),
    path('pedidos_caf/crear/', views.crear_pedido_caf, name='crear_pedido_caf'),
    path('pedidos_caf/mis_pedidos', views.mis_pedidos, name='mis_pedidos'),
    path('pedidos_caf/pendientes/<int:pedido_id>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pedidos_caf/pendientes/', views.pedidos_pendientes, name='pedidos_pendientes'),
    path('pedidos_caf/mis_pedidos_pendientes/', views.mis_pedidos_pendientes, name='mis_pedidos_pendientes'),
    path('pedidos_caf/lista_bajo_stock/', views.lista_stock_bajo, name='lista_bajo_stock'),
    path('pedidos_caf/lista_pedidos/', views.listado_pedidos_caf, name='lista_pedidos_caf'),
    path("reporte_productos_pdf_caf", views.reporte_pedidos_pdf_caf, name="reporte_pedidos_caf_pdf"),
    path("reporte_productos_excel_caf", views.reporte_pedidos_excel_caf, name="reporte_pedidos_caf_xsls"),
    path('timeout/', views.timeouterror, name='timeouterror'),
    path('index_estadistica_caf/', views.index_estadistica_caf, name='index_estadistica_caf'),
    path('graficas_productos/', views.graficas_productos, name='graficas_productos'),
    path('graficas_usuarios_caf/', views.graficas_usuario_caf, name='graficas_usuarios_caf'),
    path('grafica_pedidos_caf/', views.grafica_pedidos_caf, name='grafica_pedidos_caf'),
    path('grafica_estado_pedido_caf/', views.grafica_estado_pedido_caf, name='grafica_estado_pedido_caf'),
    path('grafica_bajoStock_caf/', views.grafica_bajo_Stock_caf, name='grafica_bajoStock_caf'),
]

handler404 = 'cafeteria.views.error_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)