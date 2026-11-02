"""
Django settings for omilife_backend project.
"""

import os
import pymysql
from pathlib import Path

pymysql.install_as_MySQLdb()

# ===========================
# PATHS
# ===========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# SECURITY
# ===========================
SECRET_KEY = os.environ.get('SECRET_KEY', 'development-secret-key')

# IMPORTANT: Production must set DEBUG=False
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "omilife.co.ke",
    "www.omilife.co.ke",
    "localhost",
    "127.0.0.1",
]

# ===========================
# INSTALLED APPS
# ===========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "pharmacy",
]

# ===========================
# MIDDLEWARE
# ===========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "omilife_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "omilife_backend.wsgi.application"

# ===========================
# DATABASE
# ===========================
if os.environ.get("USE_MYSQL") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME", "omilife_db"),
            "USER": os.environ.get("DB_USER", "root"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "3306"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ===========================
# PASSWORD VALIDATION
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===========================
# INTERNATIONALIZATION
# ===========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===========================
# STATIC FILES
# ===========================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===========================
# CORS
# ===========================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8082",
    "http://127.0.0.1:8082",
    "https://omilife.co.ke",
    "https://www.omilife.co.ke",
]

CORS_ALLOW_ALL_ORIGINS = False

# ===========================
# REST FRAMEWORK
# ===========================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# ===========================
# EMAIL SETTINGS (HostPinnacle SMTP - Production SSL)
# ===========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "mail.omilife.co.ke"
EMAIL_PORT = 465       # **CHANGE to 465 (SSL Port)**
EMAIL_USE_TLS = False  # **CHANGE to False**
EMAIL_USE_SSL = True   # **CHANGE to True**

EMAIL_HOST_USER = "sales@omilife.co.ke"
EMAIL_HOST_PASSWORD = "sales@omilife"  # Your real password

DEFAULT_FROM_EMAIL = "sales@omilife.co.ke"
ADMIN_EMAIL = "sales@omilife.co.ke"

# ===========================
# LOGGING
# ===========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_error.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
}

# ===========================
# DEBUG MODE EMAIL OVERRIDE REMOVED ❗
# ===========================
# DO NOT override EMAIL_BACKEND in DEBUG mode.
# It was blocking your emails from being delivered.
# In production, consider setting EMAIL_HOST_PASSWORD via environment variables for security.
