from .models import Articulo

def bajo_stock_alert(request):
    """
    Context processor para mostrar alerta si hay artículos con stock bajo (cantidad < 10).
    La alerta se muestra UNA VEZ por sesión al iniciar sesión, solo para Administradores.
    """
    bajo_stock = Articulo.objects.filter(cantidad__lt=10).exists()
    mostrar_alerta = False

    user = request.user
    if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_pap', False):
        # Verificar si ya se mostró la alerta en esta sesión
        if 'alerta_stock_mostrada' not in request.session:
            mostrar_alerta = True
            request.session['alerta_stock_mostrada'] = True  # Marcar como mostrada

    return {
        'bajo_stock': bajo_stock,
        'mostrar_alerta': mostrar_alerta  # Nombre simplificado para el template
    }