from .models import Articulo

def bajo_stock_alert(request):
    """
    Muestra alerta solo en rutas de Papelería para administradores con acceso
    """
    contexto = {
        'bajo_stock': False,
        'mostrar_alerta': False
    }

    if request.path.startswith('/papeleria/'):
        bajo_stock = Articulo.objects.filter(cantidad__lt=10).exists()
        user = request.user
        
        if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_pap', False):
            if bajo_stock and 'alerta_stock_mostrada' not in request.session:
                contexto.update({
                    'bajo_stock': True,
                    'mostrar_alerta': True
                })
                request.session['alerta_stock_mostrada'] = True

    return contexto