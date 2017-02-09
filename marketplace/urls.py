from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^v1/users$', views.UserList.as_view()),
]