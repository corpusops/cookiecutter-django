# -*- coding: utf-8 -*-
"""
Django settings for {{cookiecutter.django_project_name}} project.

Generated by 'django-admin startproject' using Django {{cookiecutter.django_ver}}.

For more information on this file, see
https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/ref/settings/
"""
from __future__ import absolute_import, division, print_function

import copy
import os
from datetime import timedelta
from importlib import import_module

import django
import six
from django.utils.log import DEFAULT_LOGGING

try:
    import raven  # noqa
    HAS_SENTRY = True
except ImportError:
    HAS_SENTRY = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
{{cookiecutter.lname.upper()}}_DIR = PROJECT_DIR
SRC_DIR = os.path.dirname(PROJECT_DIR)
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(DATA_DIR, 'data')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
PRIVATE_DIR = os.path.join(BASE_DIR, 'private')
PROJECT_NAME = os.path.basename(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []
USE_X_FORWARDED_HOST = {% if cookiecutter.settings_use_x_forwarded_host%}True{%else%}False{%endif%}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    {% if cookiecutter.with_celery -%}'django_celery_beat',
    'django_celery_results',{%- endif %}
    #{% if cookiecutter.with_apptest %}
    'apptest'
{%endif%}
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
{%- if cookiecutter.django_ver[0]|int < 2 %}
# django 1/2 compat
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
{%- endif %}
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join({{cookiecutter.lname.upper()}}_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'

# Database
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': {%- if 'postgis' in cookiecutter.db_mode.lower() %}
            'django.contrib.gis.db.backends.postgis'
            {%- elif 'postgres' in cookiecutter.db_mode.lower() %}
            'django.db.backends.postgresql_psycopg2'
            {%- else %}
            'django.db.backends.{{cookiecutter.db_mode.lower()}}'
            {%- endif %}
    }
}
DEFAULT_DB = DATABASES['default']
db_opts = (
    ('mysql', {
        'NAME': ('MYSQL_DATABASE',),
        'USER': ('MYSQL_USER',),
        'PASSWORD': ('MYSQL_PASSWORD',),
        'HOST': ('MYSQL_HOST',),
        'PORT': ('MYSQL_PORT',),
    }),
    ('post', {
        'NAME': ('POSTGRES_DB',),
        'USER': ('POSTGRES_USER',),
        'PASSWORD': ('POSTGRES_PASSWORD',),
        'HOST': ('POSTGRES_HOST',),
        'PORT': ('POSTGRES_PORT',),
    }),
    ('general', {
        'NAME': ('DATABASE_NAME', 'DB_NAME',),
        'USER': ('DATABASE_USER', 'DB_USER',),
        'HOST': ('DATABASE_HOST', 'DB_HOST',),
        'PORT': ('DATABASE_PORT', 'DB_PORT',),
        'PASSWORD': ('DATABASE_PASSWORD', 'DB_PASSWORD',),
    }),
)
db_opts_dict = dict(db_opts)
db_opts_k = 'general'
for knob, values in db_opts:
    if knob in DEFAULT_DB['ENGINE']:
        db_opts_k = knob
        break
for v, envvars in db_opts_dict[db_opts_k].items():
    for envvar in envvars + db_opts_dict['general'][v]:
        try:
            DEFAULT_DB.setdefault(v,  os.environ[envvar])
            break
        except KeyError:
            pass

DEFAULT_DB.setdefault('HOST', 'db')
DEFAULT_DB.setdefault('PORT', '')

# Password validation
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
{% if cookiecutter.user_model %}
AUTH_USER_MODEL = '{{cookiecutter.user_model}}'
{% endif %}
# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_URL = 'logout'

# Internationalization
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/topics/i18n/
LANGUAGE_CODE = '{{cookiecutter.language_code}}'
TIME_ZONE = '{{cookiecutter.tz}}'
USE_I18N = {{ cookiecutter['use_i18n'] and 'True' or 'False'}}
USE_L10N = {{ cookiecutter['use_l10n'] and 'True' or 'False'}}
USE_TZ = {{ cookiecutter['use_tz'] and 'True' or 'False'}}
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locales'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/howto/static-files/
STATIC_URL = '{{cookiecutter.statics_uri}}/'
STATICFILES_DIRS = (
    os.path.join({{cookiecutter.lname.upper()}}_DIR, 'static'),
)
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')
MEDIA_URL = '{{cookiecutter.media_uri}}/'
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')

# Just to be easily override by children conf files.
LOGGING = copy.deepcopy(DEFAULT_LOGGING)

# Cache settings
CACHES = {
    "default": {
{% if cookiecutter.cache_system %}
        "BACKEND": "{% if cookiecutter.cache_system == 'redis'%}django_redis.cache.RedisCache{% elif cookiecutter.cache_system=='memcached'%}django.core.cache.backends.memcached.MemcachedCache{%endif%}",
        "LOCATION": {% if cookiecutter.cache_system == 'redis'%}"redis://redis:6379/1"{% elif cookiecutter.cache_system=='memcached'%}os.getenv(
            'MEMCACHED_URL',
                '{}:{}'.format(
                    os.getenv('MEMCACHE_HOST', 'memcached'),
                    os.getenv('MEMCACHE_PORT', '11211'))){%endif%},
        {% if cookiecutter.cache_system == 'redis'%}"OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },{%endif%}
        {% if cookiecutter.cache_system == 'memcached'%}"KEY_PREFIX": '{{cookiecutter.memcached_key_prefix}}',{%endif%}
    }
{% else %}
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
{%endif %}
}

SESSION_ENGINE = "{{cookiecutter.session_engine_base}}"

# Mail
EMAIL_HOST = 'mailcatcher'
EMAIL_PORT = 1025

{% if cookiecutter.with_celery %}
# Celery settings
CELERY_BROKER_URL = 'amqp://celery-broker//'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
{% endif %}

DEBUG = False
CORS_ORIGIN_ALLOW_ALL = False

###############################################################################
# Environment settings routines, compliant with 12Factor: https://12factor.net/
#  The settings are loaded (first has more priority):
#  - maybe from: .instances.<env>
#  - maybe from: .local
#  - one of: .{prod, dev, test}
#  - environ: Most of the base variables can be redefined
#    via environment variables
#  - this file: .base
###############################################################################

# Make django configurable via environment
SETTINGS_ENV_PREFIX = 'DJANGO__'
# Those settings will throw a launch failure in deploy envs
# if they are not explicitly set
EXPLICIT_ENV_VARS = ['SECRET_KEY']
ENV_VARS = EXPLICIT_ENV_VARS + [
    'EMAIL_HOST',
    'EMAIL_PORT',
    'EMAIL_USE_TLS',
    'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD',
    'DEFAULT_FROM_EMAIL']
DJANGO_ENV_VARS = {}

# Scan environ for django configuration items
for cenvvar, value in os.environ.items():
    # Bring back prefixed env vars
    # eg DJANGO__SECRET_KEY to SECRET_KEY form.
    if cenvvar.startswith(SETTINGS_ENV_PREFIX):
        setting = SETTINGS_ENV_PREFIX.join(
            cenvvar.split(SETTINGS_ENV_PREFIX)[1:])
        DJANGO_ENV_VARS[setting] = value
    #
    # Look also at the environ Root for explicit env vars
    #  Please note that prefixed value will always have
    #  the higher priority (DJANGO__FOO vs FOO)
    for setting in ENV_VARS:
        if setting not in DJANGO_ENV_VARS:
            try:
                DJANGO_ENV_VARS[setting] = os.environ[setting]
            except KeyError:
                pass

# export back DJANGO_ENV_VARS dict as django settings
globs = globals()
for setting, value in six.iteritems(DJANGO_ENV_VARS):
    globs[setting] = value


def as_col(value, separators=None, final_type=None, **kw):
    if final_type is None:
        final_type = list
    if separators is None:
        separators = ['-|_', '_|-', '___', ',', ';', '|']
    if isinstance(value, six.string_types):
        assert(len(separators))
        while separators:
            try:
                separator = separators.pop(0)
            except IndexError:
                break
            if separator in value:
                break
        value = final_type(value.split(separator))
        if final_type is not list:
            value = final_type(value)
    return value


def as_int(value, **kw):
    if value not in ['', None]:
        value = int(value)
    return value


def as_bool(value, asbool=True):
    if isinstance(value, six.string_types):
        if value and asbool:
            low = value.lower().strip()
            if low in [
                'false', 'non', 'no', 'n', 'off', '0', '',
            ]:
                return False
            if low in [
                'true', 'oui', 'yes', 'y', 'on', '1',
            ]:
                return True
    return bool(value)


def locals_settings_update(_locals, mapping=None):
    '''
    Update _locals dict with mapping dict filtering module special variables.
    mapping: any dict, and potentially a globals/locals __dict__

    return:
        _locals: updated with mapping vars/vals
        __name__ if any: most of the cases, it's use to determine the environment (name)
    '''
    if mapping is None:
        mapping = {}
    for var, value in six.iteritems(mapping):
        if var in [
            '__name__', '__doc__', '__package__',
            '__loader__', '__spec__', '__file__',
            '__cached__', '__builtins__'
        ]:
            continue
        _locals[var] = value
    return _locals, mapping.get('__name__', '').split('.')[-1]


def filter_globals():
    '''
    Shortcut helper to locals_settings_update() to only get
    the filtered globals from this current module without special variables
    '''
    return locals_settings_update({}, globals())[0]


def check_explicit_settings(_locals):
    '''
    verify that some vars are explicitly defined
    '''
    for setting in EXPLICIT_ENV_VARS:
        try:
            _ = _locals[setting]  #noqa
        except KeyError:
            raise Exception('{0} django settings is not defined')


def post_process_settings(globs=None):
    '''
    Make intermediary processing on settings like:
        - checking explicit vars
        - tranforming vars which can come from system environment as strings
          in their final values as django settings
    '''
    _locals, env = locals_settings_update(locals(), globs)
    check_explicit_settings(_locals)
    for setting, func, fkwargs in (
        ('DEBUG', as_bool, {}),
        ('EMAIL_PORT', as_int, {}),
        ('EMAIL_USE_TLS', as_bool, {}),
        ('CORS_ORIGIN_ALLOW_ALL', as_bool, {}),
        ('CORS_ORIGIN_WHITELIST', as_col, {'final_type': tuple}),
        ('ALLOWED_HOSTS', as_col, {}),
    ):
        try:
            _locals[setting]
        except KeyError:
            continue
        _locals[setting] = func(_locals[setting], **fkwargs)
    try:
        cache_url = _locals['{{cookiecutter.cache_system.upper()}}_URL']
        _locals['CACHES']['default']['LOCATION'] = cache_url
    except KeyError:
        pass
    {% if cookiecutter.with_sentry -%}SENTRY_DSN = _locals.setdefault('SENTRY_DSN', '')
    SENTRY_RELEASE = _locals.setdefault('SENTRY_RELEASE', 'prod')
    INSTALLED_APPS = _locals.setdefault('INSTALLED_APPS', tuple())
    SENTRY_TAGS = _locals.pop('SENTRY_TAGS', None)
    if SENTRY_DSN or HAS_SENTRY:
        if 'raven.contrib.django.raven_compat' not in INSTALLED_APPS:
            # type is used to handle both INSTALLED_APPS setted as a tuple or a list
            _locals['INSTALLED_APPS'] = (
                type(
                    _locals['INSTALLED_APPS']
                )(['raven.contrib.django.raven_compat']) +
                _locals['INSTALLED_APPS'])
        RAVEN_CONFIG = _locals.setdefault('RAVEN_CONFIG', {})
        RAVEN_CONFIG.setdefault('release', SENTRY_RELEASE)
        RAVEN_CONFIG['dsn'] = SENTRY_DSN
        RAVEN_CONFIG.setdefault(
            'transport',
            'raven.transport.requests.RequestsHTTPTransport')
        # If you are using git, you can also automatically
        # configure the release based on the git info.
        LOGGING = _locals.setdefault('LOGGING', copy.deepcopy(DEFAULT_LOGGING))
        LOGGING['disable_existing_loggers'] = True
        LOGGING.setdefault('handlers', {}).update({
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',  #noqa
            }})
        root = LOGGING.setdefault('root', {})
        root['handlers'] = ['sentry']
        if SENTRY_TAGS and isinstance(SENTRY_TAGS, six.string_types):
            _locals['SENTRY_TAGS'] = {}
            for tagentry in SENTRY_TAGS.split(','):
                tag = tagentry.split(':')[0]
                value = ':'.join(tagentry.split(':')[1:])
                if not value:
                    value = tag
                    tag = 'general'
                _locals['SENTRY_TAGS'][tag] = value
        if 'DEPLOY_ENV' in _locals:
            _locals['RAVEN_CONFIG']['environment'] = _locals['DEPLOY_ENV']
    {%- endif %}
    globals().update(_locals)
    return _locals, filter_globals(), env


def set_prod_settings(globs):
    '''
    Additional post processing of settings only ran on hosted environments
    '''
    _locals, env = locals_settings_update(locals(), globs)
    default_mail = (
        '{env}-{{cookiecutter.lname}}@{{cookiecutter.tld_domain}}'.format(
            env=env))
    DEFAULT_FROM_EMAIL = _locals.setdefault('DEFAULT_FROM_EMAIL', default_mail)
    SERVER_EMAIL = _locals.setdefault('SERVER_EMAIL', default_mail)
    _locals.setdefault('ADMINS', [('root', SERVER_EMAIL)])
    _locals.setdefault('EMAIL_HOST', 'localhost')
    _locals.setdefault('DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
    ALLOWED_HOSTS = _locals.setdefault('ALLOWED_HOSTS', [])
    CORS_ORIGIN_WHITELIST = _locals.setdefault(
        'CORS_ORIGIN_WHITELIST', tuple())
    # those settings by default are empty, we need to handle this case
    if not CORS_ORIGIN_WHITELIST:
        _locals['CORS_ORIGIN_WHITELIST'] = (
            '{env}-{{cookiecutter.lname}}.{{cookiecutter.tld_domain}}'.format(env=env),  #noqa
            '.{{cookiecutter.tld_domain}}')
    if not ALLOWED_HOSTS:
        _locals['ALLOWED_HOSTS'] = [
            '{env}-{{cookiecutter.lname}}.{{cookiecutter.tld_domain}}'.format(env=env),  # noqa
            '.{{cookiecutter.tld_domain}}']
    globals().update(_locals)
    return _locals, filter_globals(), env
