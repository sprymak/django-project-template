from .production import *

DATABASES['default'].update({
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': '{{ project_name }}_staging',
    'USER': '',
})
