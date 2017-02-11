from django.conf.urls import include, url
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^v1/users/$', views.UserList.as_view()),
    url(r'^v1/users/(?P<id_user>[\-0-9a-z]+)/$', views.UserDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)