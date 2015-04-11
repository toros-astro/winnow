from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^training/', include("winnow.urls")),
    url(r'^accounts/', include("registration.backends.simple.urls"))
)
