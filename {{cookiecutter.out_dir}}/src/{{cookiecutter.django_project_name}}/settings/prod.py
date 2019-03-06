# -*- coding: utf-8 -*-
from .base import *  # noqa

# SECURITY #

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = {% if cookiecutter.settings_csrf_cookie_httponly%}True{%else%}False{%endif%}
DEBUG = False
CORS_ORIGIN_ALLOW_ALL = False

# Suppose we are using HTTPS
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = '{{cookiecutter.settings_account_default_http_protocol}}'
SECURE_SSL_REDIRECT = {% if cookiecutter.settings_secure_ssl_redirect%}True{%else%}False{%endif%}

MEDIA_ACCEL_REDIRECT = False

locs_, globs_, env = post_process_settings(locals())
globals().update(globs_)
try:
    from .local import *  # noqa
except ImportError:
    pass
