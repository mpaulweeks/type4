from django.conf.urls import patterns, url

from type4 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)