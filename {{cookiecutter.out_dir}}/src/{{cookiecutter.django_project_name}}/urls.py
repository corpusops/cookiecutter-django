# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
try:
    from django.urls import path
except ImportError:
    pass

try:
    from django.views.i18n import javascript_catalog
    jstrans = url(r'^jsi18n/$', javascript_catalog,
                  name='javascript-catalog')
except ImportError:
    from django.views.i18n import JavaScriptCatalog
    jstrans = path("jsi18n/",
                   JavaScriptCatalog.as_view(packages=['socialhome']),
                   name="javascript-catalog")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    jstrans,
]

if 'apptest' in settings.INSTALLED_APPS:  # pragma: nobranch
    urlpatterns += [
        url(r'^test', include('apptest.urls')),
    ]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

admin.site.site_header = '{{cookiecutter.django_project_name}}' 
