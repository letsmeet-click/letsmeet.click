import rules
from rules.contrib.views import PermissionRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from events.models import Event
from .forms import EventCreateForm
from .models import Community, CommunitySubscription


class CommunityListView(ListView):
    model = Community


class CommunityCreateView(LoginRequiredMixin, CreateView):
    model = Community
    fields = ['name', ]
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


class CommunityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Community
    fields = ['name', 'slug', 'cname', 'twitter', 'github', 'homepage', 'irc_channel', 'irc_network', 'slack', ]
    template_name = 'communities/community_update.html'
    permission_required = 'community.can_edit'


class CommunityDetailView(DetailView):
    model = Community


class CommunityEventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = 'communities/community_event_create.html'
    form_class = EventCreateForm
    permission_required = 'community.can_create_event'

    def get_permission_object(self):
        return self.get_community()

    def get_community(self):
        return get_object_or_404(Community, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community'] = self.get_community()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.community = self.get_community()
        self.object.save()
        return redirect(self.get_success_url())


class CommunitySubscribeView(LoginRequiredMixin, DetailView):
    model = Community
    template_name = 'communities/community_subscribe.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        community = self.object
        try:
            CommunitySubscription.objects.get(user=request.user, community=community)
            messages.warning(request, 'You are already subscribed to "{}"'.format(community.name))
            return redirect(community)
        except CommunitySubscription.DoesNotExist:
            pass
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        CommunitySubscription.objects.get_or_create(
            user=request.user, community=self.get_object(),
        )
        return redirect(self.get_object())


class CommunityUnsubscribeView(LoginRequiredMixin, DetailView):
    model = Community
    template_name = 'communities/community_unsubscribe.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        community = self.object
        try:
            user_subscription = CommunitySubscription.objects.get(
                user=request.user, community=community)
        except CommunitySubscription.DoesNotExist:
            messages.warning(request, 'You cannot unsubscribe when you are not subscribed')
            return redirect(community)

        if not rules.test_rule('can_unsubscribe', request.user, user_subscription):
            messages.error(request, 'You cannot unsubscribe when you are the last owner')
            return redirect(community)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        community = self.object
        try:
            user_subscription = CommunitySubscription.objects.get(
                user=request.user, community=community)
        except CommunitySubscription.DoesNotExist:
            messages.warning(request, 'You cannot unsubscribe when you are not subscribed')
            return redirect(community)

        if not rules.test_rule('can_unsubscribe', request.user, user_subscription):
            messages.error(request, 'You cannot unsubscribe when you are the last owner')
            return redirect(community)

        messages.success(request, 'Successfully unsubscribed from "{}"'.format(community.name))
        user_subscription.delete()
        return redirect(community)


class MyCommunitySubscriptionListView(LoginRequiredMixin, ListView):
    model = CommunitySubscription

    def get_queryset(self):
        return self.request.user.community_subscriptions.all()


class CommunityRedirectView(RedirectView):

    permanent = False
    pattern_name = 'community_detail'

    def get_redirect_url(self, *args, **kwargs):
        community = get_object_or_404(Community, cname=kwargs.pop('cname'))
        kwargs['slug'] = community.slug
        return super().get_redirect_url(*args, **kwargs)
