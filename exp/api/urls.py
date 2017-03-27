from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/login/$', views.login_user),
    url(r'^v1/logout/$', views.logout_user),
    url(r'^v1/registration/$', views.register_new_user),
    url(r'^v1/users/$', views.get_users),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', views.get_user_detail),
    url(r'^v1/latest/$', views.get_latest_data, name='latest_data')
]
