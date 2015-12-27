from django.db import transaction
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from braces.views import LoginRequiredMixin

from .models import Community, CommunitySubscription


class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    fields = ['name']
    template_name = 'communities/community_create.html'

    def form_valid(self, form):
        with transaction.atomic():
            out = super().form_valid(form)
            CommunitySubscription.objects.create(
                community=self.object,
                user=self.request.user,
                role='owner'
            )

        return out


class CommunityDetailView(DetailView):
    model = Community


class MyCommunitySubscriptionListView(LoginRequiredMixin, ListView):
    model = CommunitySubscription

    def get_queryset(self):
        return self.request.user.community_subscriptions.all()
