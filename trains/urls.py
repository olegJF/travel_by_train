from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^(?P<page_number>\d+)/$', views.home, name='home'),
    url(r'^detail/(?P<pk>\d+)/$', views.TrainDetail.as_view(), name='detail'),
    url(r'add/$', views.TrainCreate.as_view(), name='add'),
    url(r'update/(?P<pk>\d+)/$', views.TrainUpdate.as_view(), name='update'),
    url(r'delete/(?P<pk>\d+)/$', views.TrainDelete.as_view(), name='delete'),
    url(r'^$', views.home, name='home'),


]