from .models import Productos

def bajo_stock_cafeteria_alert(request):
    """
    Procesador de contexto EXCLUSIVO para alertas de Cafetería
    Compatible con tu template actual que usa:
    - mostrar_alerta_caf
    - bajo_stock_caf
    """
    # Valores por defecto
    context = {
        'mostrar_alerta_caf': False,
        'bajo_stock_caf': False
    }

    # Solo activar en rutas de Cafetería
    if request.path.startswith('/cafeteria/'):
        # Verificar stock bajo para productos de Cafetería
        bajo_stock_caf = Productos.objects.filter(
            tipo='CAFETERIA',  # Campo que diferencia el tipo de producto
            cantidad__lt=10    # Umbral de stock bajo
        ).exists()
        
        user = request.user
        
        # Verificar permisos del usuario
        if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_caf', False):
            # Control para mostrar solo una vez por sesión
            if 'alerta_stock_caf_mostrada' not in request.session:
                context = {
                    'mostrar_alerta_caf': bajo_stock_caf,
                    'bajo_stock_caf': bajo_stock_caf
                }
                request.session['alerta_stock_caf_mostrada'] = True

    return context