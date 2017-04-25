from django.conf.urls import url
from django.views.decorators.http import require_http_methods

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/auth/registration/$', require_http_methods(['POST'])(views.create_user)),
    url(r'^v1/auth/login/$', require_http_methods(['POST'])(views.create_authenticator)),
    url(r'^v1/auth/logout/(?P<auth_token>[A-Fa-f0-9]{64})/$', require_http_methods(['DELETE'])(views.delete_authenticator)),
    url(r'^v1/users/drivers/$', require_http_methods(['GET'])(views.get_driver_by_carpool)),
    url(r'^v1/users/passengers/$', require_http_methods(['GET'])(views.get_passengers_by_carpool)),
    url(r'^v1/carpools/$', require_http_methods(['GET', 'POST'])(views.dispatch_carpools)),
    url(r'^v1/search/$', require_http_methods(['GET'])(views.search_carpools_by_query))
]
