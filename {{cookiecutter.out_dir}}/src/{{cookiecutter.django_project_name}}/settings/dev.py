# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import os

try:
    from django.utils import six
except ImportError:
    import six


from .base import *  # noqa

os.environ['RELATIVE_SETTINGS_MODULE'] = '.dev'

INSTALLED_APPS += tuple([  # noqa
    {% if cookiecutter.with_toolbar %}'debug_toolbar',{%endif%}
    {% if cookiecutter.with_djextensions %}'django_extensions',{%endif%}
])
SECRET_KEY = os.environ.get('SECRET_KEY', 'secretkey-superhot-12345678')
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
# INTERNAL_IPS = ('127.0.0.1',)  # Used by app debug_toolbar
DEBUG = True

# Force every loggers to use console handler only. Note that using 'root'
# logger is not enough if children don't propage.
for logger in six.itervalues(LOGGING['loggers']):  # noqa
    logger['handlers'] = ['console']
# Log every level.
LOGGING['handlers']['console']['level'] = logging.NOTSET  # noqa

MIDDLEWARE += tuple([
    {% if cookiecutter.with_toolbar %}'debug_toolbar.middleware.DebugToolbarMiddleware',{%endif %}
])
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}
{% if cookiecutter.cache_only_in_prod %}
# deactivate cache except if we have set either:
# - ENABLE_CACHE_IN_DEV
# - DJANGO__ENABLE_CACHE_IN_DEV=true (envvar)
try:
    ENABLE_CACHE_IN_DEV  # noqa
except NameError:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
{% endif %}
USE_DJANGO_EXTENSIONS = True

locs_, globs_, env = post_process_settings(locals())
globals().update(globs_)
try:
    from .local import *  # noqa
except ImportError:
    pass
