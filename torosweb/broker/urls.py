from django.conf.urls import url

#from views import *

#from views import index

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^update$', views.update, name='update'),
]
