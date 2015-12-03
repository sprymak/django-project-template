import os
import sys
import multiprocessing

if __name__ == '__main__' or __package__ is None:
    sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf.base import *


RUN_PATH = os.path.join(BASE_DIR, 'var', 'run')

if not os.path.isdir(CACHE_PATH):
    os.makedirs(CACHE_PATH)
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)
if not os.path.isdir(RUN_PATH):
    os.makedirs(RUN_PATH)


bind = 'unix://%s' % os.path.join(RUN_PATH, 'gunicorn.sock')
chdir = APPLICATION_PATH
workers = multiprocessing.cpu_count() * 2 + 1
pidfile = os.path.join(RUN_PATH, 'gunicorn.pid')
accesslog = os.path.join(LOG_PATH, 'access.log')
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = os.path.join(LOG_PATH, 'gunicorn.log')
proc_name = PROJECT_NAME

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    raw_env = (
        'DJANGO_SETTINGS_MODULE=conf.production',
    )
