from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('marketplace.urls')), # redirects anything from http://localhost:8000/ to 'marketplace.urls' and look for further instructions
]
