from django.conf.urls import url
from django.views.decorators.http import require_http_methods

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/auth/registration/$', views.create_user),
    url(r'^v1/auth/login/$', views.create_authenticator),
    url(r'^v1/auth/logout/(?P<username>[a-z0-9.-]+)/$', views.delete_authenticator),
    url(r'^v1/users/drivers/$', views.get_driver_by_carpool),
    url(r'^v1/users/passengers/$', views.get_passengers_by_carpool),
    url(r'^v1/carpools/$', views.get_carpools_by_params),
    url(r'^v1/search/$', views.search_carpools_by_query)
]
