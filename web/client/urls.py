from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users/(?P<pk>\d+)/$', views.user_detail),
    url(r'^users/$', views.list_users),
]	
