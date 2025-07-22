from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class SessionExpiryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # La sesión aún es válida
            return None
        elif request.session.get('has_session'):
            # La sesión ha expirado
            request.session.flush()  # limpia la sesión
            return redirect('sesion_expirada')
        else:
            # Primera vez que accede sin sesión
            request.session['has_session'] = True
        return None
