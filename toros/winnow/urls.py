from django.conf.urls import url, patterns
from winnow import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^rank/$', views.rank, name='rank'),
                       url(r'^thumb/(?P<trans_candidate_id>\d+)/$', views.thumb, name = 'thumb'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^object/(?P<trans_candidate_id>\d+)/$', views.object_detail, name = 'object_detail'),
                       url(r'^profile/(?P<a_username>.+)/$', views.show_profile, name = 'profile_detail'),
)