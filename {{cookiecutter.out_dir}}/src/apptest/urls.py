from django.conf.urls import url

from . import views

app_name = 'apptest'

urlpatterns = [
    url(r'^$', views.helloworld, name='helloworld'),
]
