from .defaults import *
SECRET_KEY = '{{ secret_key }}'

ALLOWED_HOSTS = []

CACHES['default'].update({
    'BACKEND': 'redis_cache.RedisCache',
    'LOCATION': '127.0.0.1:6379',
})

DATABASES['default'].update({
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': '{{ project_name }}',
    'USER': '',
})

if 'gunicorn' not in INSTALLED_APPS:
    INSTALLED_APPS = INSTALLED_APPS + ('gunicorn',)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
