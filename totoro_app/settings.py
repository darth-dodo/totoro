"""
Django settings for totoro_app project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import logging.config
import os

from configurations import Configuration, values
from django.utils.log import DEFAULT_LOGGING


class Base(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

    SECRET_KEY = values.SecretValue()
    LOG_LEVEL = values.Value(environ_prefix="", default="ERROR")

    DEBUG = values.BooleanValue(environ_prefix="", default=False)

    ALLOWED_HOSTS = values.ListValue(
        environ_prefix="", default=["127.0.0.1", "localhost"]
    )

    # Application definition

    SYSTEM_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # third party apps
        "rest_framework",
        "django_extensions",
    ]

    PROJECT_APPS = [
        "movies",
        "external_services"
    ]

    INSTALLED_APPS = SYSTEM_APPS + PROJECT_APPS

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "totoro_app.urls"

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

    WSGI_APPLICATION = "totoro_app.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/

    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }

    # django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/

    # lazy eval for env based config
    # https://django-configurations.readthedocs.io/en/stable/patterns/#property-settings
    @property
    def REST_FRAMEWORK(self):
        return {
            "DEFAULT_AUTHENTICATION_CLASSES": (
                "rest_framework.authentication.SessionAuthentication",
                "rest_framework.authentication.TokenAuthentication",
            ),
            "DEFAULT_PERMISSION_CLASSES": (
                "rest_framework.permissions.IsAuthenticated",
            ),
            "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
        }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL"),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "KEY_PREFIX": "totoro_app",
        }
    }

    CACHE_TTL = values.PositiveIntegerValue(environ_prefix="", default=(0))


class Dev(Base):

    DEBUG = values.BooleanValue(environ_prefix="", default=True)
    INTERNAL_IPS = values.ListValue(environ_prefix="", default=["127.0.0.1"])
    EXPOSE_SWAGGER_INTERFACE = values.BooleanValue(environ_prefix="", default=True)
    LOG_LEVEL = "DEBUG"

    DEV_APPS = [
        "debug_toolbar",
        "drf_yasg",
    ]

    DEV_MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INSTALLED_APPS = Base.INSTALLED_APPS + DEV_APPS
    MIDDLEWARE = Base.MIDDLEWARE + DEV_MIDDLEWARE

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    # exact format is not important, this is the minimum information
                    "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                },
                "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
            },
            "handlers": {
                # console logs to stderr
                "console": {"class": "logging.StreamHandler", "formatter": "default", },
                "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
            },
            "loggers": {
                # default for all undefined Python modules
                "": {"level": "WARNING", "handlers": ["console"], },
                # Our application code
                "movies": {
                    "level": LOG_LEVEL,
                    "handlers": ["console"],
                    # Avoid double logging because of root logger
                    "propagate": False,
                },
                "external_services": {
                    "level": LOG_LEVEL,
                    "handlers": ["console"],
                    # Avoid double logging because of root logger
                    "propagate": False,
                },
                # Default runserver request logging
                "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
            },
        }
    )


class Test(Dev):
    pass
