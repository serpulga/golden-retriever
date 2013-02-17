from django.conf.urls import patterns, url

from retrieve.views import retrieve, home

urlpatterns = patterns('',
    url(r'^home/$', home),
    url(r'^retrieve/', retrieve),
)
