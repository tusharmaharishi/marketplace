from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.get_home_page),
    url(r'^users/(?P<pk>\d+)/$', views.get_user_detail),
    url(r'^users/$', views.get_users),
]	
