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
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "http://10.0.2.2",
    "http://192.168.0.103:8000",
    # ej: "https://pruebanube-xcmk.onrender.com",
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
    "channels",
    "storages",  # (queda instalado por si a futuro vuelves a S3)
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

ASGI_APPLICATION = "proyecto_tesis.asgi.application"
WSGI_APPLICATION = "proyecto_tesis.wsgi.application"

# ==============================================================
# BASE DE DATOS (MySQL)
# ==============================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"), 
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
# MEDIA → almacenamiento local en Render
# ==============================================================
# Dejamos S3/Cellar desactivado. Si algún día quieres volver,
# puedes setear USE_S3_MEDIA=True en el entorno.
USE_S3_MEDIA = os.getenv("USE_S3_MEDIA", "False").lower() == "true"

if USE_S3_MEDIA:
    AWS_ACCESS_KEY_ID = os.getenv("CELLAR_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("CELLAR_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("CELLAR_BUCKET_NAME")
    AWS_S3_REGION_NAME = "US"
    AWS_S3_ENDPOINT_URL = f"https://{os.getenv('CELLAR_HOST')}"

    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {
        "ACL": "public-read",
        "CacheControl": "max-age=86400",
    }

    AWS_S3_USE_SSL = True
    AWS_S3_VERIFY = True

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# Límite de subida (50 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

# ==============================================================
# FIREBASE (Admin SDK)
# ==============================================================
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY")
FIREBASE_PRIVATE_KEY_ID = os.getenv("FIREBASE_PRIVATE_KEY_ID", "")

# ==============================================================
# DRF
# ==============================================================
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
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "465"))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# ==============================================================
# REDIS / CELERY
# ==============================================================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# ==============================================================
# CHANNELS
# ==============================================================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    }
}

# ==============================================================
# MODELO VOSK
# ==============================================================
MODEL_PATH_RELATIVO = Path("vosk-model-small-es-0.42")
MODEL_PATH = BASE_DIR / MODEL_PATH_RELATIVO

# ==============================================================
# VARIOS
# ==============================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
