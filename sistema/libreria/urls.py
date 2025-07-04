from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'libreria'

urlpatterns = [
    path('papeleria/', include(('papeleria.urls', 'papeleria'), namespace='papeleria')),
    path('cafeteria/', include(('cafeteria.urls', 'cafeteria'), namespace='cafeteria')),
    path('cde/', include(('cde.urls', 'cde'), namespace='cde')),

    path('', views.inicio, name='inicio'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('ver_usuario/<int:user_id>/', views.ver_usuario, name='ver_usuario'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('cambiar-estado-usuario/<int:user_id>/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    # RESTABLECER CONTRASEÑA 
    path("reset_password/", views.password_reset_request, name="password_reset"),
    path("reset_password/done/", views.password_reset_done, name="password_reset_done"),
    path("reset_password/confirm/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("reset_password/done/", views.password_reset_done, name="password_reset_done"),

    path('validar_datos/', views.validar_datos, name='validar_datos'),
    path('api/validate-password/', views.validate_password, name='validate_password'),
    path('reporte_usuario_pdf/', views.reporte_usuario_pdf, name='reporte_usuario_pdf'),
    path('reporte_usuario_excel/', views.reporte_usuario_excel, name='reporte_usuario_excel'),
    #estadisticas
    path('graficas_usuarios_activos/', views.graficas_usuarios_activos, name='graficas_usuarios_activos'),
    path('sesion_expirada/', views.sesion_expirada, name='sesion_expirada'),
    path('manual de usuario/', views.manual_usuario_view, name='manual_usuario'),
    path('timeout/', views.timeouterror, name='timeouterror'),
     path('verificar-usuarios/', views.verificar_usuario, name='verificar_usuario'),

]

handler404 = 'libreria.views.error_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)