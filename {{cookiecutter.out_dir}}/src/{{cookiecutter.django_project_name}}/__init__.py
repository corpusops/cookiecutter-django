from __future__ import absolute_import, unicode_literals
{% if cookiecutter.with_celery %}from .celery import app as celery_app
__all__ = ('celery_app',){% endif %}
