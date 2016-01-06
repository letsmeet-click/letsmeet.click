import rules
from rules.contrib.views import PermissionRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from events.models import Event, EventRSVP
from .forms import EventCreateForm, CommunityUpdateForm
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
    template_name = 'communities/community_update.html'
    permission_required = 'community.can_edit'
    form_class = CommunityUpdateForm


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
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.get_object().subscribe_user(request.user)
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

    @transaction.atomic
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

        EventRSVP.objects.filter(
            event__pk__in=Event.objects.upcoming().filter(community=community).values_list('pk', flat=True),
            user=request.user).delete()
        user_subscription.delete()
        messages.success(request, 'Successfully unsubscribed from "{}"'.format(community.name))
        return redirect(community)


class SubscriptionChangeRoleView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = CommunitySubscription
    allowed_methods = ['post']

    def get_permission_object(self):
        return self.get_object().community

    def get_permission_required(self):
        role = self.kwargs.get('role')
        if role == CommunitySubscription.ROLE_OWNER:
            return ['community.can_set_owner']
        elif role == CommunitySubscription.ROLE_ADMIN:
            return ['community.can_set_admin']
        elif role == CommunitySubscription.ROLE_SUBSCRIBER:
            return ['community.can_set_subscriber']
        else:
            raise ValueError('Unknown role type {}'.format(role))

    def post(self, request, *args, **kwargs):
        subscription = self.get_object()
        if rules.test_rule('is_last_owner', request.user, subscription):
            messages.error(request, 'You cannot change your role when you are the last owner')
            return redirect(subscription.community)

        subscription.role = kwargs['role']
        subscription.save()
        return redirect(subscription.community)


class CommunityRedirectView(RedirectView):
    permanent = False
    pattern_name = 'community_detail'

    def get_redirect_url(self, *args, **kwargs):
        cname_parameter = kwargs.pop('cname')
        for community in Community.objects.filter(cname__icontains=cname_parameter):
            for cname in community.cname.split(' '):
                if cname.lower() == cname_parameter:
                    kwargs['slug'] = community.slug
                    return super().get_redirect_url(*args, **kwargs)
        raise Http404
