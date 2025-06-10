from .models import Articulo

def bajo_stock_papeleria_alert(request):
    """
    Procesador de contexto EXCLUSIVO para alertas de Papelería
    Compatible con tu template actual que usa:
    - mostrar_alerta
    - bajo_stock
    """
    # Valores por defecto
    context = {
        'mostrar_alerta': False,
        'bajo_stock': False
    }

    # Solo activar en rutas de Papelería
    if request.path.startswith('/papeleria/'):
        # Verificar stock bajo
        bajo_stock = Articulo.objects.filter(
            seccion='Papelería',
            cantidad__lt=10
        ).exists()
        
        user = request.user
        
        # Verificar permisos
        if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_pap', False):
            # Control de visualización única por sesión
            if 'alerta_stock_mostrada' not in request.session:
                context = {
                    'mostrar_alerta': bajo_stock,
                    'bajo_stock': bajo_stock
                }
                request.session['alerta_stock_mostrada'] = True

    return context