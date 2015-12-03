import logging
import os
import sys
from conf.base import *
if IS_TEST:
    from conf.test import *
elif IS_DEV:
    from conf.defaults import *
else:
    from conf.production import *

logging.basicConfig(
    format=VERBOSE_FORMAT,
    filename=os.path.join(LOG_PATH, LOG_FILENAME),
    level=logging.DEBUG,
)

logger = logging.getLogger(PROJECT_NAME)
logger.debug('\nPython path:\n\t%s' % '\n\t'.join(sys.path),)
logger.debug(
    '\nPython environment:\n\t%s' %
    "\n\t".join(["=".join(e) for e in os.environ.items()]),)

try:
    from local_settings import *
except ImportError, e:
    pass
