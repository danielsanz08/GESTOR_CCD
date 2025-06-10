from .models import Articulo

def bajo_stock_alert(request):
    """
    Solo muestra alerta si el usuario está en rutas de Papelería.
    """
    mostrar_alerta = False
    bajo_stock = False

    # Verificar si la ruta actual es de Papelería
    if request.path.startswith('/papeleria/'):  # Ajusta según tus URLs
        bajo_stock = Articulo.objects.filter(cantidad__lt=10).exists()
        
        user = request.user
        if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_pap', False):
            if 'alerta_stock_mostrada' not in request.session:
                mostrar_alerta = bajo_stock  # Solo mostrar si hay stock bajo
                request.session['alerta_stock_mostrada'] = True

    return {
        'bajo_stock': bajo_stock,
        'mostrar_alerta': mostrar_alerta,
    }