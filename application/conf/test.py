import os
from .defaults import *

#TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = APPLICATION_PATH
TEST_DISCOVER_ROOT = APPLICATION_PATH
TEST_DISCOVER_PATTERN = 'test_*.py'
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(BASE_DIR, 'var/audit/coverage')

TEST_APPS = (
    'django_coverage',
)
INSTALLED_APPS = INSTALLED_APPS + TEST_APPS

DATABASES['default'].update(NAME=':memory:')
