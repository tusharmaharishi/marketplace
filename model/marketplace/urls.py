from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/auth/(?P<authenticator>[A-Fa-f0-9]{64})/$', views.Authentication.as_view(), name='auth_by_authenticator'),
    url(r'^v1/auth/(?P<username>[a-z0-9.-]+)/$', views.Authentication.as_view(), name='auth_by_username'),
    url(r'^v1/users/$', views.UserList.as_view(), name='user_list'),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user_detail_by_pk'),
    url(r'^v1/users/(?P<username>[a-z0-9.-]+)/$', views.UserDetail.as_view(), name='user_detail_py_username'),
    url(r'^v1/carpools/$', views.CarpoolList.as_view(), name='carpool_list'),
    # url(r'^v1/carpools/?location_start=(?P<location_start>[0-9.]+)&location_end=(?P<location_end>[0-9.]+)$', views.CarpoolList.as_view()),
    url(r'^v1/carpools/(?P<pk>[0-9]+)/$', views.CarpoolDetail.as_view(), name='carpool_detail'),
]
