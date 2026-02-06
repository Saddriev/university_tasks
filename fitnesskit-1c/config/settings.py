"""
Настраиваемые параметры интеграции с 1С: URL, ClubId, Basic auth.
Читаются из переменных окружения.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-change-in-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
_allowed = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "team",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

_AUTH_PREFIX = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [] if DEBUG else [
    {"NAME": _AUTH_PREFIX + "UserAttributeSimilarityValidator"},
    {"NAME": _AUTH_PREFIX + "MinimumLengthValidator"},
    {"NAME": _AUTH_PREFIX + "CommonPasswordValidator"},
    {"NAME": _AUTH_PREFIX + "NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Интеграция с 1С (настраиваемые параметры из env) ---
ONEC_BASE_URL = os.environ.get(
    "ONEC_BASE_URL",
    "http://176.192.70.122:90/fitnes_t_nfc_mobile/hs/nfc_mobile/v1",
)
ONEC_CLUB_ID = os.environ.get(
    "ONEC_CLUB_ID", "59115d1e-9052-11eb-810c-6eae8b56243b",
)
ONEC_LOGIN = os.environ.get("ONEC_LOGIN", "FitnessKit")
ONEC_PASSWORD = os.environ.get("ONEC_PASSWORD", "vY0xodyg")
ONEC_GET_SPECIALIST_REQUEST_ID = os.environ.get(
    "ONEC_GET_SPECIALIST_REQUEST_ID",
    "e1477272-88d1-4acc-8e03-7008cdedc81e",
)
ONEC_TIMEOUT = float(os.environ.get("ONEC_TIMEOUT", "5.0"))
