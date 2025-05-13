from .models import Articulo

def bajo_stock_alert(request):
    bajo_stock = Articulo.objects.filter(cantidad__lt=10).exists()
    return {'bajo_stock': bajo_stock}
