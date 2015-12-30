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
    CommunityCreateView,
    CommunityDetailView,
    CommunityEventCreateView,
    CommunityListView,
    CommunityUpdateView,
    CommunitySubscribeView,
    CommunityUnsubscribeView,
    CommunityRedirectView,
    MyCommunityListView,
    SubscriptionChangeRoleView,
)

urlpatterns = [
    url(r'^c/$', CommunityListView.as_view(), name='community_list'),
    url(r'^c/change-role/(?P<pk>\d+)/(?P<role>(owner|admin|subscriber))/$',
        SubscriptionChangeRoleView.as_view(), name='subscription_change_role'),
    url(r'^c/(?P<slug>[\w-]+)/$', CommunityDetailView.as_view(), name='community_detail'),
    url(r'^c/(?P<slug>[\w-]+)/create-event/$', CommunityEventCreateView.as_view(), name='community_event_create'),
    url(r'^c/(?P<slug>[\w-]+)/edit/$', CommunityUpdateView.as_view(), name='community_update'),
    url(r'^c/(?P<slug>[\w-]+)/subscribe/$', CommunitySubscribeView.as_view(), name='community_subscribe'),
    url(r'^c/(?P<slug>[\w-]+)/unsubscribe/$', CommunityUnsubscribeView.as_view(), name='community_unsubscribe'),
    url(r'^cname/(?P<cname>[^/]+)/$', CommunityRedirectView.as_view(), name='community_cname'),
    url(r'^create-community/$', CommunityCreateView.as_view(), name='community_create'),
    url(r'^my-communities/$', MyCommunityListView.as_view(), name='my_communities'),
]
