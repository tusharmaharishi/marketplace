from django.conf.urls import url
from django.views.decorators.http import require_http_methods
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/auth/$', require_http_methods(['POST'])(views.Authentication.as_view())),
    url(r'^v1/auth/(?P<auth_token>[A-Fa-f0-9]{64})/$', require_http_methods(['GET', 'DELETE'])(views.Authentication.as_view())),
    url(r'^v1/auth/(?P<username>[a-z0-9.-]+)/$', require_http_methods(['GET', 'DELETE'])(views.Authentication.as_view())),
    url(r'^v1/users/$', views.UserList.as_view()),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^v1/users/(?P<username>[a-z0-9.-]+)/$', views.UserDetail.as_view()),
    url(r'^v1/carpools/$', views.CarpoolList.as_view()),
    # url(r'^v1/carpools/?location_start=(?P<location_start>[0-9.]+)&location_end=(?P<location_end>[0-9.]+)$', views.CarpoolList.as_view()),
    url(r'^v1/carpools/(?P<pk>[0-9]+)/$', views.CarpoolDetail.as_view()),
]
