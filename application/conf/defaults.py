import os
import sys
from django.utils.translation import ugettext_lazy as _
from .base import *

DEBUG = IS_DEV
TEMPLATE_DEBUG = DEBUG

if LIB_PATH not in sys.path:
    sys.path.insert(1, LIB_PATH)
if APPS_PATH not in sys.path:
    sys.path.insert(1, APPS_PATH)
if APPLICATION_PATH not in sys.path:
    sys.path.insert(1, APPLICATION_PATH)

FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'var', 'tmp')
FILE_UPLOAD_PERMISSIONS = 0644
SESSION_FILE_PATH = os.path.join(BASE_DIR, 'var', 'tmp')
MEDIA_ROOT = os.path.join(BASE_DIR, 'var/lib/uploads/')

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# if not IS_DEV:
#     STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'dev@metacorus.com'
if IS_DEV:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = (
    ('Developers', 'dev@metacorus.com'),
)
MANAGERS = ADMINS

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

#ASSETS_DEBUG = DEBUG

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'django_assets.finders.AssetsFinder',
)

TEMPLATE_DIRS = (
    os.path.join(APPLICATION_PATH, 'templates'),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
)

SECRET_KEY = '{{ secret_key }}'
ALLOWED_HOSTS = []
# AUTH_PROFILE_MODULE = "{{ project_name }}.UserProfile"

AUTH_USER_MODEL = '{{ project_name }}.User'
ANONYMOUS_USER_ID = -1
LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/logout'
LOGIN_REDIRECT_URL = '/'
# for django.contrib.auth.decorators.login_required() decorator
# from django.contrib import auth
# auth.REDIRECT_FIELD_NAME = 'continue'

CSRF_COOKIE_NAME = 'token'
SESSION_COOKIE_NAME = 'sid'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

ACCOUNT_INVITATION_DAYS = 7

AUTHENTICATION_BACKENDS = (
    # 'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'django_assets',
    'django_filters',
    'gunicorn',
    'oauth2_provider',
    # 'registration',
    # 'rest_framework',
    # 'taggit',
    # 'taggit_templatetags',
    # 'guardian',
)

if IS_DEV:
    INSTALLED_APPS += (
        'debug_toolbar',
        'template_debug',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'
APPEND_SLASH = False

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'var', 'db', PROJECT_NAME + '.db'),
        'DUMP_PATH': os.path.join(BASE_DIR, 'var', 'db'),
    }
}

if IS_DEV:
    CACHE_BACKEND = 'django.core.cache.backends.dummy.DummyCache'
else:
    CACHE_BACKEND = 'django.core.cache.backends.filebased.FileBasedCache'

CACHE_TIMEOUT = 60 * 5
CACHES = {
    'default': {
        'BACKEND': CACHE_BACKEND,
        'LOCATION': CACHE_PATH,
        'TIMEOUT': CACHE_TIMEOUT,
    }
}


ASSETS_CACHE = os.path.join(CACHE_PATH, 'webassets')

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ('en', _('English')),
    # ('ru', _('Russian')),
)
LANGUAGE_COOKIE_NAME = 'hl'

# See 'How Django discovers translations' at official Django documentation site
# http://goo.gl/W6lFTo
LOCALE_PATHS = (
    os.path.join(APPLICATION_PATH, 'locale'),
)

import djcelery
djcelery.setup_loader()


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
VERBOSE_FORMAT = (
    '%(levelname)s %(asctime)s %(name)s: '
    '[%(process)d] %(funcName)s: %(message)s')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': VERBOSE_FORMAT
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        PROJECT_NAME: {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
