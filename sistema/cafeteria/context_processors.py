from .models import Productos

from django.urls import resolve

def bajo_stock_alert_caf(request):
    bajo_stock_caf = Productos.objects.filter(cantidad__lt=10).exists()
    mostrar_alerta_caf = False

    user = request.user
    # Verifica si la URL es la de index_caf (ajusta '/index_caf/' según tu ruta real)
    if (user.is_authenticated 
        and user.role == 'Administrador' 
        and getattr(user, 'acceso_caf', False)
        and request.path == '/index_caf/'):  # 🔥 Solo se activa en esta ruta
        
        if 'alerta_stock_caf_mostrada' not in request.session:
            mostrar_alerta_caf = True
            request.session['alerta_stock_caf_mostrada'] = True

    return {
        'bajo_stock_caf': bajo_stock_caf,
        'mostrar_alerta_caf': mostrar_alerta_caf
    }