from django.conf.urls import url, patterns
from winnow import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^rank/$', views.rank, name='rank'),
                       url(r'^thumb/$', views.generateTransientThumbnail, name='thumb'),
)