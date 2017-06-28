from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url(r'^', include('communities.urls')),
    url(r'^', include('events.urls')),
    url(r'^', include('main.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('locations.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
