import logging
import os
import sys
from conf.base import *
if IS_TEST:
    from conf.test import *
elif IS_DEV:
    try:
        from conf.develop import *
    except ImportError:
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

# Give a last chance to override some settings on the current host.
# This is a good place to configure the settings specific to the staging server.
try:
    from local_settings import *
except ImportError:
    pass
