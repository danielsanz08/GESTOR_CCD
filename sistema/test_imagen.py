from PIL import Image as PilImage

img_path = r"D:\Users\WILLIAME\Documents\DANIEL SANCHEZ\GESTOR_CCD\sistema\papeleria\static\imagen"  # Cambia esta ruta a la ruta correcta de tu imagen

try:
    img = PilImage.open(img_path)
    img.verify()  # Verifica integridad
    print("La imagen está OK")
except Exception as e:
    print("Error al abrir la imagen:", e)
