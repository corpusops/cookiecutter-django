# -*- coding: utf-8 -*-
import logging
import os

import six

from .base import *  # noqa

os.environ['RELATIVE_SETTINGS_MODULE'] = '.dev'

INSTALLED_APPS += (  # noqa
    'debug_toolbar',
    'django_extensions',
)
SECRET_KEY = os.environ.get('SECRET_KEY', 'secretkey-superhot-12345678')
ALLOWED_HOSTS = ['*']
# INTERNAL_IPS = ('127.0.0.1',)  # Used by app debug_toolbar
DEBUG = True

# Force every loggers to use console handler only. Note that using 'root'
# logger is not enough if children don't propage.
for logger in six.itervalues(LOGGING['loggers']):  # noqa
    logger['handlers'] = ['console']
# Log every level.
LOGGING['handlers']['console']['level'] = logging.NOTSET  # noqa

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

post_process_settings(locals())
try:
    from .local import *  # noqa
except ImportError:
    pass
