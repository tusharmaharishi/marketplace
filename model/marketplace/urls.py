from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/users/$', views.UserList.as_view()),
    url(r'^v1/users/(?P<id>[\-0-9a-z]+)/$', views.UserDetailById.as_view()),
    url(r'^v1/carpools/$', views.CarpoolList.as_view()),
    url(r'^v1/carpools/(?P<id>[\-0-9a-z]+)/$', views.CarpoolDetailById.as_view()),
    # url(r'^v1/carpools/(?P<location_start>[0-9.]+)&(?P<location_end>[0-9.]+)/$', views.CarpoolDetailById.as_view())
]
