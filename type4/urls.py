from django.conf.urls import patterns, url

from type4 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.all_cards, name='all_cards'),
    url(r'^filter/$', views.filter, name='filter'),
    url(r'^add_cards/$', views.add_cards, name='add_cards'),
    url(r'^update/$', views.update, name='update'),
    url(r'^changes/$', views.changes, name='changes'),
)