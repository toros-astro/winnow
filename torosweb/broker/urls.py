from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^uploadjson$', views.uploadjson, name='uploadjson'),
    url(r'^circular/(?P<alert_name>\w+)$', views.circular, name='circular'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^alert/(?P<alert_name>\w+)$', views.alert_detail,
        name='alert_detail'),
]
