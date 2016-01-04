from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='main/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='main/about.html'), name='about'),
    url(r'^legal/$', TemplateView.as_view(template_name='main/legal.html'), name='legal'),
    url(r'^login/$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
