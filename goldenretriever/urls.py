from django.conf.urls import url

from .retrieve.views import retrieve, home

urlpatterns = [
    url(r'^home/$', home),
    url(r'^retrieve/', retrieve),
]
