from django.conf.urls import url

from .views import (
    HomeView,
    UserProfileView,
    UserSocialAuthChangeView,
    UserSocialAuthRemoveView,
    UserChangeView,
    UserPasswordChangeView,
)


urlpatterns = (
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^profile/$', UserProfileView.as_view(), name="profile"),
    url(r'^profile/change-notification/$', UserSocialAuthChangeView.as_view(), name="change_notification"),
    url(r'^profile/remove-social/$', UserSocialAuthRemoveView.as_view(), name="socialauth_remove"),
    url(r'^profile/edit/$', UserChangeView.as_view(), name="profile_edit"),
    url(r'^profile/edit/password/$', UserPasswordChangeView.as_view(), name="profile_edit_password"),
)
