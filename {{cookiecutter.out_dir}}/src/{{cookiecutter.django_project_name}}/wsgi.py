"""
WSGI config for {{cookiecutter.django_project_name}} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/{{cookiecutter.django_ver_1}}/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
{% if cookiecutter.with_sentry %}from raven.contrib.django.raven_compat.middleware.wsgi import Sentry{%-endif %}

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.django_settings}}.prod")

{% if cookiecutter.with_sentry
%}application = Sentry(get_wsgi_application()){% else
%}application = get_wsgi_application(){% endif %}
