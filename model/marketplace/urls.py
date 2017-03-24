from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/auth/$', views.Authentication.as_view(), name='auth'),
    url(r'^v1/users/$', views.UserList.as_view(), name='user_list'),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user_detail'),
    url(r'^v1/carpools/$', views.CarpoolList.as_view(), name='carpool_list'),
    # url(r'^v1/carpools/?location_start=(?P<location_start>[0-9.]+)&location_end=(?P<location_end>[0-9.]+)$', views.CarpoolList.as_view()),
    url(r'^v1/carpools/(?P<pk>[0-9]+)/$', views.CarpoolDetail.as_view(), name='carpool_detail'),
]
