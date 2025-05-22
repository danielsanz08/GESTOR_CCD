from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
class SessionExpiryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Usuario activo, marca la sesión como "logueada"
            request.session['user_logged_in'] = True
            return None
        else:
            # Si la sesión indica que estuvo logueado, pero ya no lo está -> sesión expirada
            if request.session.get('user_logged_in'):
                request.session.flush()
                return redirect('libreria:sesion_expirada')
            # Caso primera visita sin login previo, no hace nada especial
            return None
