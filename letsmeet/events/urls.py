"""letsmeet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url

from .views import (
    EventUpdateView,
    EventDetailView,
    EventRSVPView,
)

urlpatterns = [
    url(r'^c/(?P<community_slug>[\w-]+)/(?P<slug>[\w-]+)/$', EventDetailView.as_view(), name='event_detail'),
    url(r'^c/(?P<community_slug>[\w-]+)/(?P<slug>[\w-]+)/edit/$', EventUpdateView.as_view(), name='event_update'),
    url(r'^c/(?P<community_slug>[\w-]+)/(?P<slug>[\w-]+)/rsvp/(?P<answer>(yes|no|reset))/$', EventRSVPView.as_view(), name='event_rsvp'),
]
