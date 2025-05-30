# context_processors.py

from datetime import datetime, timedelta
from .models import Articulo

def bajo_stock_alert(request):
    """
    Context processor para mostrar alerta si hay artículos con stock bajo (cantidad < 10).
    La alerta solo se muestra a usuarios Administradores con acceso al módulo Papelería,
    y no se muestra más de una vez cada 24 horas por sesión.
    """
    bajo_stock = Articulo.objects.filter(cantidad__lt=10).exists()
    mostrar_alerta = False

    user = request.user
    if user.is_authenticated and user.role == 'Administrador' and getattr(user, 'acceso_pap', False):
        ultima_alerta = request.session.get('ultima_alerta_stock')
        ahora = datetime.now()

        if not ultima_alerta:
            mostrar_alerta = True
        else:
            try:
                ultima_alerta_dt = datetime.fromisoformat(ultima_alerta)
                if ahora - ultima_alerta_dt > timedelta(hours=24):
                    mostrar_alerta = True
            except Exception:
                mostrar_alerta = True

        if mostrar_alerta:
            request.session['ultima_alerta_stock'] = ahora.isoformat()

    return {
        'bajo_stock': bajo_stock,
        'mostrar_alerta_stock': mostrar_alerta
    }
