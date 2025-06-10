from .models import Productos

def bajo_stock_cafeteria_alert(request):
    """
    Solo muestra alerta si el usuario está en rutas de Cafetería.
    """
    mostrar_alerta_caf = False
    bajo_stock_caf = False

    # Verificar si la ruta actual es de Cafetería
    if request.path.startswith('/cafeteria/'):  # Ajusta según tus URLs
        bajo_stock_caf = Productos.objects.filter(cantidad__lt=10).exists()
        
        user = request.user
        if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_caf', False):
            if 'alerta_stock_caf_mostrada' not in request.session:
                mostrar_alerta_caf = bajo_stock_caf  # Solo mostrar si hay stock bajo
                request.session['alerta_stock_caf_mostrada'] = True

    return {
        'bajo_stock_caf': bajo_stock_caf,
        'mostrar_alerta_caf': mostrar_alerta_caf,
    }