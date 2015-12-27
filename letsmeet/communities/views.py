from django.views.generic import (
    DetailView,
    CreateView,
)

from .models import Community


class CommunityCreateView(CreateView):
    model = Community
    fields = ['name']
    template_name = 'communities/community_create.html'


class CommunityDetailView(DetailView):
    model = Community
