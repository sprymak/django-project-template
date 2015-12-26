import os
from django.core.handlers.wsgi import WSGIHandler as _WSGIHandler
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


class WSGIHandler(_WSGIHandler):
    def __init__(self, application, base_dir=None):
        self.application = application
        super(WSGIHandler, self).__init__()

    def __call__(self, environ, start_response):
        os.environ['wsgi.url_scheme'] = environ.get('wsgi.url_scheme', '')
        os.environ['HTTP_HOST'] = environ.get('HTTP_HOST', '')
        os.environ['SERVER_PORT'] = environ.get('SERVER_PORT', '')
        return self.application(environ, start_response)


application = WSGIHandler(get_wsgi_application())
