from django.conf.urls import url

from .views import (
    LocationSearchView,
)

urlpatterns = [
    url(r'^create-location/$', LocationSearchView.as_view(), name='location_create'),
]
