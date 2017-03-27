from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.get_carpools_latest, name='index'),
    url(r'^users/(?P<pk>\d+)/$', views.get_user_detail, name="get_user_detail"),
    url(r'^users/$', views.get_users, name="get_users"),
    url(r'^login/$', views.login_user, name="auth_login"),
    url(r'^logout/$', views.logout_user, name="auth_logout"),
    url(r'^create_carpool/$', views.create_carpool, name="create_carpool"),
    url(r'^registration/$', views.register_user, name="register_user"),
]	
