"""
Django settings for proyecto_tesis project.
Django 5.x
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ==============================================================
# PATHS & ENV
# ==============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ==============================================================
# SEGURIDAD
# ==============================================================
SECRET_KEY = os.getenv("SECRET_KEY", "debug-secret")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Hosts básicos desde .env (separados por coma)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# IPs locales extra (para pruebas en red local / emulador)
ALLOWED_HOSTS += [
    "10.0.2.2",
    "192.168.0.103",
]

# Orígenes de confianza para CSRF (ajusta si usas HTTPS / dominio público)
# Se recomienda usar HTTPS para Render en producción.
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "http://10.0.2.2",
    "http://192.168.0.103:8000",
    # Agregue su dominio de Render si usa HTTPS: 'https://su-app.onrender.com'
]

# ==============================================================
# APPS
# ==============================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps del proyecto
    "core.apps.CoreConfig",
    "usuarios",
    "reuniones",
    "talleres",
    "votaciones",
    "foro",
    "anuncios",
    "recursos",
    "datamart",

    # Terceros
    "widget_tweaks",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    # 'channels', # Deshabilitado para Free Tier de Render
    "storages", 
    'cloudinary_storage', # Usado para el almacenamiento gratuito de media files
]

# ==============================================================
# MIDDLEWARE
# ==============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "core.middleware.ForcePasswordChangeMiddleware",
    # "core.middleware.MonitorRendimientoMiddleware",
]

ROOT_URLCONF = "proyecto_tesis.urls"

# ==============================================================
# TEMPLATES
# ==============================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ASGI_APPLICATION = "proyecto_tesis.asgi.application" # Deshabilitado, ya que Channels usa Redis
WSGI_APPLICATION = "proyecto_tesis.wsgi.application"

# ==============================================================
# BASE DE DATOS (MySQL)
# ==============================================================
# ... (Bloque de base de datos sin cambios)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE", "prueba"),
        "USER": os.getenv("MYSQL_USER", "root"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD", ""),
        "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "CONN_MAX_AGE": 0 if DEBUG else 60,
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "connect_timeout": 10,
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ==============================================================
# AUTH / PASSWORD / LOGIN
# ==============================================================
# ... (Bloque de autenticación sin cambios)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 14},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/home"
LOGOUT_REDIRECT_URL = "/accounts/login/"

AUTHENTICATION_BACKENDS = [
    "core.authentication.LoginConCorreo",
    "django.contrib.auth.backends.ModelBackend",
]

# ==============================================================
# I18N / ZONA HORARIA
# ==============================================================
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ==============================================================
# STATICFILES
# ==============================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================================================
# MEDIA (CLOUD STORAGE GRATUITO)
# --------------------------------------------------------------
# Se usa Cloudinary para almacenamiento persistente de media files (audios, imágenes).
# Las variables CLOUDINARY_* deben estar en el entorno de Render.
# ==============================================================

# 1. Obtener variables de entorno para Cloudinary
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# 2. Configurar el almacenamiento predeterminado para archivos de medios
# Esto anula la lógica anterior de S3/Cellar y usa Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# 3. Definir la URL base
MEDIA_URL = '/media/'

# Límite de subida (50 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

# ==============================================================
# FIREBASE (Admin SDK)
# ==============================================================
# ... (Bloque de Firebase sin cambios)
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY")
FIREBASE_PRIVATE_KEY_ID = os.getenv("FIREBASE_PRIVATE_KEY_ID", "")

# ==============================================================
# DRF
# ==============================================================
# ... (Bloque de DRF sin cambios)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

# ==============================================================
# EMAIL (SMTP)
# ==============================================================
# ... (Bloque de Email sin cambios)
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "465"))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# ==============================================================
# REDIS / CELERY (DESHABILITADO PARA PLAN GRATUITO DE RENDER)
# ==============================================================
# REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")

# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
# CELERY_TIMEZONE = TIME_ZONE

# ==============================================================
# CHANNELS (DESHABILITADO PARA PLAN GRATUITO DE RENDER)
# ==============================================================
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
#         "CONFIG": {
#             "hosts": [REDIS_URL],
#         },
#     }
# }

# ==============================================================
# MODELO VOSK
# --------------------------------------------------------------
# ATENCIÓN: La lógica que usa Vosk debe ejecutarse SÍNCRONAMENTE en el proceso 
# web único (si es muy rápida) o deshabilitarse por completo, ya que Celery
# está deshabilitado.
# ==============================================================
MODEL_PATH_RELATIVO = Path("vosk-model-small-es-0.42")
MODEL_PATH = BASE_DIR / MODEL_PATH_RELATIVO

# ==============================================================
# VARIOS
# ==============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"