from django.conf.urls import include, url
from django.contrib import admin
from marketplace import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('marketplace.urls')),
    url(r'^v1/users$', views.UserList.as_view()),
]
