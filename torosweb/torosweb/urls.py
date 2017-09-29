from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include("winnow.urls", namespace='winnow')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^rb/', include('rbmanager.urls', namespace='rbmanager')),
    url(r'^broker/', include('broker.urls', namespace='broker')),
    url(r'^wiki/notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
