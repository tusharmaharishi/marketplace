from django.conf.urls import url
from django.views.decorators.http import require_http_methods

from . import views

user_urls = [
    url(r'^v1/users/$', require_http_methods(['GET', 'POST'])(views.UserView.as_view())),
    url(r'^v1/users/(?P<pk>[0-9]+)/$', require_http_methods(['GET', 'PUT', 'DELETE'])(views.UserView.as_view())),
    url(r'^v1/users/(?P<username>[a-z0-9.-]+)/$',
        require_http_methods(['GET', 'PUT', 'DELETE'])(views.UserView.as_view())),
]

carpool_urls = [
    url(r'^v1/carpools/$', require_http_methods(['GET', 'POST'])(views.CarpoolView.as_view())),
    url(r'^v1/carpools/(?P<pk>[0-9]+)/$', require_http_methods(['GET', 'PUT', 'DELETE'])(views.CarpoolView.as_view())),
]

authentication_urls = [
    url(r'^v1/auth/$', require_http_methods(['POST'])(views.AuthenticationView.as_view())),
    url(r'^v1/auth/(?P<auth_token>[A-Fa-f0-9]{64})/$',
        require_http_methods(['GET', 'DELETE'])(views.AuthenticationView.as_view())),
    url(r'^v1/auth/(?P<username>[a-z0-9.-]+)/$',
        require_http_methods(['GET', 'DELETE'])(views.AuthenticationView.as_view())),
]

urlpatterns = [
    url(r'^$', require_http_methods(['GET'])(views.index)),
] + user_urls + carpool_urls + authentication_urls
