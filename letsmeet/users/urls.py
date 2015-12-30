from django.conf.urls import url

from .views import UserProfileView, UserSocialAuthChangeView, UserChangeView, UserPasswordChangeView


urlpatterns = (
    url(r'^profile/$', UserProfileView.as_view(), name="profile"),
    url(r'^profile/remove_social/$', UserSocialAuthChangeView.as_view(), name="socialauth_remove"),
    url(r'^profile/edit/$', UserChangeView.as_view(), name="profile_edit"),
    url(r'^profile/edit/password/$', UserPasswordChangeView.as_view(), name="profile_edit_password"),
)
