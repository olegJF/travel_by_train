from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^(?P<page_number>\d+)/$', views.home, name='home'),
    url(r'^detail/(?P<pk>\d+)/$', views.CityDetail.as_view(), name='detail'),
    url(r'add/$', views.CityCreate.as_view(), name='add'),
    url(r'update/(?P<pk>\d+)/$', views.CityUpdate.as_view(), name='update'),
    url(r'delete/(?P<pk>\d+)/$', views.CityDelete.as_view(), name='delete'),
    url(r'^$', views.home, name='home'),


]