"""
WSGI config for metacorus-dev project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
from twod.wsgi.handler import DjangoApplication
from conf.base import *

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"


class Application(DjangoApplication):
    def __call__(self, environ, start_response):
        if 'PYTHON_EGG_CACHE' in environ:
            os.environ['PYTHON_EGG_CACHE'] = environ['PYTHON_EGG_CACHE']
        else:
            os.environ['PYTHON_EGG_CACHE'] = PYTHON_EGG_CACHE
        os.environ['wsgi.url_scheme'] = environ.get('wsgi.url_scheme', '')
        os.environ['HTTP_HOST'] = environ.get('HTTP_HOST', '')
        os.environ['SERVER_PORT'] = environ.get('SERVER_PORT', '')
        return super(Application, self).__call__(environ, start_response)


application = Application()
