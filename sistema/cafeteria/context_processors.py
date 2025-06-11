from .models import Productos

def bajo_stock_alert_caf(request):
    bajo_stock_caf = Productos.objects.filter(cantidad__lt=10).exists()
    mostrar_alerta_caf = False

    user = request.user
    if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_caf', False):
        if 'alerta_stock_caf_mostrada' not in request.session:
            mostrar_alerta_caf = True
            request.session['alerta_stock_caf_mostrada'] = True

    return {
        'bajo_stock_caf': bajo_stock_caf,
        'mostrar_alerta_caf': mostrar_alerta_caf
    }
