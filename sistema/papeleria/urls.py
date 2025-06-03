from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

app_name = 'papeleria'
urlpatterns = [
    
   path('index_pap/', views.index_pap, name='index_pap'),
   path('login/papeleria/', views.login_papeleria, name='login_papeleria'),
   path('logout_view/', views.logout_view, name='logout_view'),
   path("crear_articulo/", views.crear_articulo, name="crear_articulo"),
   path("editar_articulo/<int:articulo_id>/", views.editar_articulo, name="editar_articulo"),
   path("listar_articulo/", views.listar_articulo,name="listar_articulo"),
    path('buscar_articulo/', views.buscar_articulo, name='buscar_articulo'),
    path('eliminar_articulo/<int:id>', views.eliminar_articulo, name='eliminar_articulo'),
    
    path('verificar-nombre-articulo/', views.verificar_nombre_articulo, name='verificar_nombre_articulo'),
    path('validar_datos/', views.validar_datos, name='validar_datos'),
    path('acceso_denegado/', lambda request: render(request, 'acceso_denegado.html'), name='acceso_denegado'),
    
    
     path('reporte_articulo_pdf/', views.reporte_articulo_pdf, name='reporte_articulo_pdf'),
    path('reporte_articulo_excel/', views.reporte_articulo_excel, name='reporte_articulo_excel'),
    
     path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/lista/', views.listado_pedidos, name='listado_pedidos'),
    path('pedidos/pendientes/<int:pedido_id>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pedidos/pendientes/', views.pedidos_pendientes, name='pedidos_pendientes'),
    path('pedidos/lista_bajo_stock/', views.lista_stock_bajo, name='lista_bajo_stock'),
    path('index_estadistica/', views.index_estadistica, name='index_estadistica'),
     path('estadisticas/articulos/', views.estadisticas_articulos, name='estadisticas_articulos'),
     path('graficas_articulos/', views.graficas_articulos, name='graficas_articulos'),
     path('graficas_usuarios/', views.graficas_usuario, name='graficas_usuarios'),
     path('grafica_bajoStock/', views.grafica_bajo_Stock, name='grafica_bajoStock'),
     path('grafica_pedidos/', views.grafica_pedidos, name='grafica_pedidos'),
     path('pedidos_administrativa/', views.grafica_pedidos_administrativa, name='pedidos_administrativa'),
     path('pedidos_rues/', views.grafica_pedidos_rues, name='pedidos_rues'),
     path('pedidos_presidencia/', views.grafica_pedidos_presidencia, name='pedidos_presidencia'),
     path('pedidos_financiera/', views.grafica_pedidos_presidencia, name='pedidos_financiera'),
     path('pedidos_gestion_empresarial/', views.grafica_pedidos_gestion_empresarial, name='pedidos_gestion_empresarial'),
     path('pedidos_competitividad/', views.grafica_pedidos_competitividad, name='pedidos_competitividad'),
     path('reporte_pedidos_pdf/', views.reporte_pedidos_pdf, name='reporte_pedidos_pdf'),
     path('reporte_pedidos_excel/', views.reporte_pedidos_excel, name='reporte_pedidos_excel'),
     path('reporte_bajo_stock_pdf/', views.reporte_articulo_bajo_stock_pdf, name='reporte_articulo_bajo_stock_pdf'),
     path('reporte_articulo_bajo_stock_excel/', views.reporte_articulo_bajo_stock_excel, name='reporte_articulo_bajo_stock_excel'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
