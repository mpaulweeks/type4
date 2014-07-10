from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^type4/', include('type4.urls', namespace="type4")),
    url(r'^admin/', include(admin.site.urls)),
)
