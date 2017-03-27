from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/login/$', views.UserLogin.as_view()),
    url(r'^v1/logout/$', views.UserLogout.as_view()),
    url(r'^v1/registration/$', views.UserRegistration.as_view()),
    url(r'^v1/users/$', views.UsersFilter.as_view()),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user_detail_by_pk'),
    url(r'^v1/users/(?P<username>[a-z0-9.-]+)/$', views.UserDetail.as_view(), name='user_detail_py_username'),
    url(r'^v1/carpools/(?P<pk>[0-9]+)/$', views.CarpoolDetail.as_view(), name='carpool_detail'),
    url(r'^v1/latest/$', views.CarpoolsFilter.as_view(), name='latest_data'),
]
