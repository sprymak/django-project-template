from __future__ import absolute_import, unicode_literals
import os
import site
import sys
from django.utils.translation import ugettext_lazy as _
from .base import *

DEBUG = IS_DEV
ASSETS_DEBUG = DEBUG

sys.path.insert(1, LIB_PATH)
sys.path.insert(1, APPS_PATH)
sys.path.insert(1, APPLICATION_PATH)
site.removeduppaths()

FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'var', 'tmp')
FILE_UPLOAD_PERMISSIONS = 0o644
SESSION_FILE_PATH = os.path.join(BASE_DIR, 'var', 'tmp')
MEDIA_ROOT = os.path.join(BASE_DIR, 'var/lib/uploads/')

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# if not IS_DEV:
#     STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = SERVER_EMAIL = '%s+dev@metacorus.com' % PROJECT_NAME
if IS_DEV:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = (
    ('Developers', '%s+dev@metacorus.com' % PROJECT_NAME),
)
MANAGERS = ADMINS

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'django_assets.finders.AssetsFinder',
)

# https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-TEMPLATES
TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APPLICATION_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.i18n',
                'django.core.context_processors.csrf',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.debug',
            ),
            'debug': DEBUG,
        }
    },
)

SECRET_KEY = '{{ secret_key }}'
ALLOWED_HOSTS = []

# ACCOUNT_INVITATION_DAYS = 7
AUTH_USER_MODEL = '{{ project_name }}.User'
ANONYMOUS_USER_ID = -1
LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/logout'
LOGIN_REDIRECT_URL = '/'
# for django.contrib.auth.decorators.login_required() decorator
# from django.contrib import auth
# auth.REDIRECT_FIELD_NAME = 'continue'

AUTHENTICATION_BACKENDS = (
    # 'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
)

CSRF_COOKIE_NAME = 'token'
SESSION_COOKIE_NAME = 'sid'
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

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
    'corsheaders',
    'rest_framework',
    'rest_framework_swagger',
    # 'registration',
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
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_NAME
# This is where django_assets will store its artifacts.
# https://goo.gl/W3P5GB#django_assets.settings.ASSETS_CACHE
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

# API
# http://www.django-rest-framework.org/api-guide/settings/
# https://github.com/ottoyiu/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': '1',
    'URL_FIELD_NAME': 'self',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

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
