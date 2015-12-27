from django.views.generic import (
    DetailView,
    CreateView,
)

from braces.views import LoginRequiredMixin

from .models import Community


class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    fields = ['name']
    template_name = 'communities/community_create.html'


class CommunityDetailView(DetailView):
    model = Community
