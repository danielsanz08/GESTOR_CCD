from .models import Productos

def bajo_stock_cafeteria_alert(request):
    """
    Muestra alerta solo en rutas de Cafetería para administradores con acceso
    """
    contexto = {
        'bajo_stock_caf': False,
        'mostrar_alerta_caf': False
    }

    if request.path.startswith('/cafeteria/'):
        bajo_stock = Productos.objects.filter(cantidad__lt=10).exists()
        user = request.user
        
        if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_caf', False):
            if bajo_stock and 'alerta_stock_caf_mostrada' not in request.session:
                contexto.update({
                    'bajo_stock_caf': True,
                    'mostrar_alerta_caf': True
                })
                request.session['alerta_stock_caf_mostrada'] = True

    return contexto