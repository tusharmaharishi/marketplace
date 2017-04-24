from django.conf.urls import url
from django.views.decorators.http import require_http_methods

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/registration/$', views.create_user),
    url(r'^v1/login/$', views.create_authenticator),
    url(r'^v1/logout/(?P<auth_token>[A-Fa-f0-9]{64})/$', views.delete_authenticator),
    url(r'^v1/users/$', views.UsersFilter.as_view()),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^v1/users/(?P<username>[a-z0-9.-]+)/$', views.UserDetail.as_view()),
    url(r'^v1/carpools/(?P<pk>[0-9]+)/$', views.CarpoolDetail.as_view()),
    url(r'^v1/carpools/$', views.CarpoolList.as_view()),
    url(r'^v1/search$', views.search_carpools)
]
