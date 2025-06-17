from pathlib import Path
import os
import smtplib

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w=vb@dyxyk30)xbk52m@kx1q9)aj5s685fma)a+zh9jc0!1jy2'

# SECURITY WARNING: don't run with debug turned on in production!
# Durante el desarrollo:
DEBUG = True
# DEBUG = False  # ← lo dejas comentado

# Para el despliegue, cambias así:
# DEBUG = True
#DEBUG = False


ALLOWED_HOSTS = ['192.168.1.10', 'localhost', '127.0.0.1']




STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # asegúrate de importar os
AUTH_USER_MODEL = 'libreria.CustomUser'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 600  # La sesión expira después de 10 minutos

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "gestorccd@gmail.com"
EMAIL_HOST_PASSWORD = "utdf dxyn btiz dgjv"  # tu contraseña de aplicación
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
PASSWORD_RESET_TIMEOUT = 300  # 5 minutos


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'libreria', 
    'papeleria',
    'cafeteria',
    'cde',
    'django.contrib.humanize',
     'backup',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'libreria.middleware.SessionExpiryMiddleware',
]

ROOT_URLCONF = 'sistema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'papeleria.context_processors.bajo_stock_alert',
                'cafeteria.context_processors.bajo_stock_alert_caf',
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ccd',
        'USER': 'root',
        'PASSWORD': '',  # Cambia esto si tienes una contraseña
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        },
    }
}

AUTHENTICATION_BACKENDS = [
    'libreria.backends.EmailBackend',              # Tu backend personalizado
    'django.contrib.auth.backends.ModelBackend',   # El backend por defecto de Django
]


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True
 # Nombre de la vista en lugar de una ruta directa
LOGIN_URL = '/accounts/login/'

# Static files
STATIC_URL = '/static/'  # URL donde se accederán los archivos estáticos en el navegador
STATICFILES_DIRS = [BASE_DIR/'static']
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
BACKUP_ROOT = os.path.join(BASE_DIR, 'backups')

# Asegúrate de que el directorio exista
if not os.path.exists(BACKUP_ROOT):
    os.makedirs(BACKUP_ROOT)