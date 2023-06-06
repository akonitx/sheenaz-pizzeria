from pathlib import Path
from logging import getLogger
from pprint import pp
from django.urls import reverse_lazy
from os import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRETKEY")


# DEBUG = True
DEBUG = False if getenv("DJANGO_DEBUG") == "0" else True


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "3.214.143.59",
    "ec2-3-214-143-59.compute-1.amazonaws.com",
]
INTERNAL_IPS = ["127.0.0.1", "127.0.0.2"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "menu.apps.MenuConfig",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #  "Lime.middleware.ContentSecurityPolicyMiddleware",
    #  "Lime.middleware.AccessControlAllowOriginMiddleware",
]

ROOT_URLCONF = "Lime.urls"

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

WSGI_APPLICATION = "Lime.wsgi.application"


DB_POSTGRES_HOST = getenv("DB_POSTGRES_HOST")
if DB_POSTGRES_HOST is None:
    raise ValueError("DB_POSTGRES_HOST environemt variable should be configured")

DB_POSTGRES_PORT = getenv("DB_POSTGRES_PORT")
if DB_POSTGRES_PORT is None:
    raise ValueError("DB_POSTGRES_PORT environemt variable should be configured")

DB_POSTGRES_USER_PASSWORD = getenv("DB_POSTGRES_USER_PASSWORD")
if DB_POSTGRES_USER_PASSWORD is None:
    raise ValueError("DB_POSTGRES_USER_PASSWORD environemt variable should be configured")

DB_POSTGRES_USER = getenv("DB_POSTGRES_USER")
if DB_POSTGRES_USER is None:
    raise ValueError("DB_POSTGRES_USER environemt variable should be configured")

CONN_MAX_AGE = 1200
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "lime",
        "USER": "sheenaz",
        "PASSWORD": "10052008taras",
        "HOST": DB_POSTGRES_HOST,
        "PORT": DB_POSTGRES_PORT,
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Kiev"

USE_I18N = True

USE_TZ = True

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / "static/",
    ]
    STATIC_ROOT = BASE_DIR / "staticdev/"
    STATIC_URL = "static/"
else:
    STATIC_URL = "https://s3.eu-central-1.amazonaws.com/lime-static-files.django/static/"


LOGGING_HANDLER_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING_FILE_PATH = "../logs/debug.log" if DEBUG else "../logs/info.log"
LOGGING_CONSOLE_FORMATTER = "precise" if DEBUG else "brief"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "precise": {
            "style": "{",
            "datefmt": "%d %B, %Y — %H:%M:%S",
            "format": "{levelname:<7}  {asctime}  {module}-->{funcName}:{lineno:<6}  {message:>31}",
        },
        "brief": {
            "style": "{",
            "datefmt": "%y %B %d - %H:%M:%S",
            "format": "{levelname}  {asctime}  {message}",
        },
    },
    "handlers": {
        "console": {
            "level": LOGGING_HANDLER_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": LOGGING_CONSOLE_FORMATTER,
        },
        "file": {
            "level": LOGGING_HANDLER_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "precise",
            "filename": LOGGING_FILE_PATH,
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "main_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        }
    },
}

mainlog = getLogger("main_logger")


LOGIN_URL = reverse_lazy("login")
SUCCESS_LOGIN_URL = "main-page"
SUCCESS_CHANGING_PROFILE_ATTRIBUTES_URL = reverse_lazy("main-page")
