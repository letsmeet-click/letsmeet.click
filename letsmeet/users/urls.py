from django.conf.urls import url

from .views import UserProfileView, UserSocialAuthChangeView


urlpatterns = (
    url(r'^profile/$', UserProfileView.as_view(), name="profile"),
    url(r'^profile/remove_social/$', UserSocialAuthChangeView.as_view(), name="socialauth_remove")
)