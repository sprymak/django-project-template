import os
import sys

PROJECT_NAME = '{{ project_name }}'

__all__ = (
    'PROJECT_NAME', 'IS_DEV', 'IS_TEST', 'APPLICATION_PATH', 'BASE_DIR',
    'APPS_PATH', 'LIB_PATH', 'CACHE_PATH', 'LOG_PATH', 'LOG_FILENAME',
    'PYTHON_EGG_CACHE', 'get_env_var',
)


def get_env_var(setting, default=None):
    try:
        return os.environ[setting]
    except KeyError:
        if default is not None:
            return default

        # Normally you should not import ANYTHING from Django directly
        # into your settings, but ImproperlyConfigured is an exception.
        from django.core.exceptions import ImproperlyConfigured
        error_msg = "Environment variable '%s' is not set" % setting
        raise ImproperlyConfigured(error_msg)


_server_software = get_env_var('SERVER_SOFTWARE', '')
IS_DEV = (
    (map(os.path.basename, sys.argv[:2]) == ['manage.py', 'runserver']) or
    _server_software.startswith('Dev') or
    _server_software.startswith('WSGIServer'))

IS_TEST = 'test' in sys.argv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
APPLICATION_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(APPLICATION_PATH)
APPS_PATH = os.path.join(APPLICATION_PATH, 'apps')
LIB_PATH = os.path.join(APPLICATION_PATH, 'lib')
CACHE_PATH = os.path.join(BASE_DIR, 'var', 'cache')
LOG_PATH = os.path.join(BASE_DIR, 'var', 'log')

LOG_FILENAME = '.'.join([PROJECT_NAME, 'log'])

PYTHON_EGG_CACHE = os.path.join(CACHE_PATH, 'eggs')

CELERY_ENABLED = False
