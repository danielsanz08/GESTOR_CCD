from .models import Productos

def bajo_stock_alert_caf(request):
    """
    Context processor para mostrar alerta si hay productos con stock bajo (cantidad < 10).
    La alerta se muestra UNA VEZ por sesión al iniciar sesión, solo para Administradores.
    """
    productos_existentes = Productos.objects.exists()
    bajo_stock_caf = productos_existentes and Productos.objects.filter(cantidad__lt=10).exists()
    mostrar_alerta_caf = False

    user = request.user
    if (user.is_authenticated 
        and user.role == 'Administrador' 
        and getattr(user, 'acceso_caf', False)
        and request.path == '/index_caf/'):
        
        # Verificar si ya se mostró la alerta en esta sesión
        if 'alerta_stock_caf_mostrada' not in request.session and bajo_stock_caf:
            mostrar_alerta_caf = True
            request.session['alerta_stock_caf_mostrada'] = True  # Marcar como mostrada

    return {
        'bajo_stock_caf': bajo_stock_caf,
        'mostrar_alerta_caf': mostrar_alerta_caf
    }
