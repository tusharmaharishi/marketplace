from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^api/v1/session/login/$', views.login_user),
    url(r'^api/v1/session/logout/$', views.logout_user),
    url(r'^api/v1/users/$', views.register_new_user),
    url(r'^api/v1/users/$', views.get_users),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/$', views.get_user_detail),
    url(r'^api/v1/latest/$', views.get_latest_data, name='latest_data')
]
