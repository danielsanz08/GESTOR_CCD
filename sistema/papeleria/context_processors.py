from .models import Articulo

from datetime import datetime, timedelta
from .models import Articulo

def bajo_stock_alert(request):
    bajo_stock = Articulo.objects.filter(cantidad__lt=10).exists()

    mostrar_alerta = False

    if request.user.is_authenticated and request.user.role == 'Administrador' and request.user.module == 'Papeleria':
        ultima_alerta = request.session.get('ultima_alerta_stock')

        ahora = datetime.now()
        if not ultima_alerta:
            mostrar_alerta = True
        else:
            ultima_alerta_dt = datetime.fromisoformat(ultima_alerta)
            if ahora - ultima_alerta_dt > timedelta(hours=24):
                mostrar_alerta = True

        if mostrar_alerta:
            # Actualiza el tiempo de la última alerta en sesión
            request.session['ultima_alerta_stock'] = ahora.isoformat()

    return {
        'bajo_stock': bajo_stock,
        'mostrar_alerta_stock': mostrar_alerta
    }
