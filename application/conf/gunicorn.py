import os
import sys
import multiprocessing

if __name__ == '__main__' or __package__ is None:
    # Add base dir to the Python paths, so we can import the `conf` package.
    sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf.base import *  # noqa


DEBUG = IS_DEV or bool(get_env_var('DEBUG', ''))
RUN_PATH = os.path.join(BASE_DIR, 'var', 'run')

if not os.path.isdir(CACHE_PATH):
    os.makedirs(CACHE_PATH)
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)
if not os.path.isdir(RUN_PATH):
    os.makedirs(RUN_PATH)

bind = 'unix://%s' % os.path.join(RUN_PATH, 'gunicorn.sock')
chdir = APPLICATION_PATH
workers = 1 if DEBUG else 1 + multiprocessing.cpu_count() * 2
pidfile = os.path.join(RUN_PATH, 'gunicorn.pid')
accesslog = os.path.join(LOG_PATH, 'access.log')
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = os.path.join(LOG_PATH, 'gunicorn.log')
loglevel = 'debug' if DEBUG else 'warning'
proc_name = PROJECT_NAME

# Directory to store temporary request data as they are read
tmp_upload_dir = TEMP_PATH

# The maxium number of requests a worker will process before restarting
max_requests = 1 if DEBUG else 0

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    raw_env = (
        'DJANGO_SETTINGS_MODULE=conf.production',
    )
