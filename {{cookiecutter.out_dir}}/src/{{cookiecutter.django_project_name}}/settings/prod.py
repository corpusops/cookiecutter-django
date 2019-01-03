# -*- coding: utf-8 -*-
from .base import *  # noqa

# SECURITY #

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
DEBUG = False
CORS_ORIGIN_ALLOW_ALL = False

# Suppose we are using HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False

MEDIA_ACCEL_REDIRECT = False

locs_, globs_, env = post_process_settings(locals())
globals().update(globs_)
try:
    from .local import *  # noqa
except ImportError:
    pass
